#!/usr/bin/python

"""
pinkwave.py is an interface which can be used to create and execute a pentest with parameters
usage ./pinkwave.py [options]

for a full list, start help:
./pinkwave.py --help

example:

./pinkwave.py -t localhost -e exploits/sword/csrftokenscan.py
"""

# Importing external libs
import os,sys,time,json
from os.path import isfile
import argparse

# Importing own libs
from lib.Browser import Browser
from lib.Pentest import Pentest
from lib.ShellParse import ShellParse
from lib.Macro import Macro
from extensions.Util import Util,vdkException
import extensions.Http as Http
from lib.PyExploit import PyExploit
import lib.colors as colors
from lib.PyExploit import PyExploitException

# Import HTTP server for logger/bouncer
import server.pinkserver as pinkserver

# Start browser based on config.ini settings
browser = None
def get_browser():
    global browser
    if browser is None:
        browser = Browser().createFromConfig()

    return browser

"""Display logo art and exploit info"""
def status():
    exploitsC, pyC = count_exploits()
    print ('''

%s	         oo          dP                                             \033[1;m
%s	                     88                                             \033[1;m
%s	88d888b. dP 88d888b. 88  .dP  dP  dP  dP .d8888b. dP   .dP .d8888b. \033[1;m
%s	88'  `88 88 88'  `88 88888"   88  88  88 88'  `88 88   d8' 88ooood8 \033[1;m
%s	88.  .88 88 88    88 88  `8b. 88.88b.88' 88.  .88 88 .88'  88.  ... \033[1;m
%s	88Y888P' dP dP    dP dP   `YP 8888P Y8P  `88888P8 8888P'   `88888P' \033[1;m
%s	88                                                                  \033[1;m
%s	dP                                                                  \033[1;m

             %s -- -- +=[ %d Payloads \033[1;m
             %s -- -- +=[ %d Python Scripts \033[1;m
            \033[1;91m[W] Make sure your current directory (pwd) is the same as pinkwave.py .\033[1;m
            ''' % (colors.PURPLE,colors.PURPLE,colors.PURPLE, colors.PURPLE, colors.PURPLE, colors.PURPLE, colors.PURPLE, colors.PURPLE, colors.PURPLE, exploitsC, colors.PURPLE, pyC))

    hosts = {
             "Bouncer": Util.getBouncer(),
             "Logger": Util.getLogger()
             }

    for key in hosts.iterkeys():
        if Http.is_ok_get(hosts[key]):
            print "%s[^] %s is up. %s%s" % (colors.GREEN,key,hosts[key],colors.COLOR_END)
        else:
            print "%s[!] %s is down. %s%s" % (colors.RED,key,hosts[key],colors.COLOR_END)
            print "%s[!] Some exploits can't start:\033[1;m" % colors.YELLOW
            print "%s[!] PinkServer offline - bouncer(Direct POST requests) / logger(XSS)%s" % (colors.RED,colors.COLOR_END)
            exit(1)

def argumentParser():
    parser = argparse.ArgumentParser(description='PinkWave is a pentesting tool for linux which can be used to test (web)servers with Python scripts and Selenium. Control the browser with an easy to use API to perform actions and detect vulnerabilities.')
    argeParseData = []
    argeParseData.append({
        "short": "-s",
        "long": "--status",
        "help": "Display status of PinkWave",
        "required": False})
    argeParseData.append({
        "short": "-t",
        "long": "--target",
        "help": "(Required) Remote target host",
        "required": False})
    argeParseData.append({
        "short": "-rn",
        "long": "--requestNames",
        "help": "POST/GET names, comma seperated",
        "required": False})
    argeParseData.append({
        "short": "-r",
        "long": "--request",
        "help": "(optional) Specify request type (GET,POST or POST/DIRECT)",
        "required": False})
    argeParseData.append({
        "short": "-e",
        "long": "--exploits",
        "help": "(Required) Path to python exploit script",
        "required": False})
    argeParseData.append({
        "short": "-m",
        "long": "--macros",
        "help": "(optional) Path(s) to python macro script(s), comma seperated, runs before the exploit",
        "required": False})
    argeParseData.append({
        "short": "-cr",
        "long": "--creds",
        "help": 'User credentials, comma seperated',
        "required": False})
    argeParseData.append({
        "short": "-po",
        "long": "--ports",
        "help": 'Expected ports for port scan',
        "required": False})
    argeParseData.append({
        "short": "-sl",
        "long": "--ssl",
        "help": 'SSL ports for SSL stripping/cipher testing',
        "required": False})
    argeParseData.append({
	"short" : "-wl",
	"long" : "--wordlist",
	"help" : "Provide a path to a line seperated wordlist file",
	"required" : False})
    for apData in argeParseData:
        parser.add_argument(apData['short'], apData['long'], help=apData['help'], required=apData['required'])

    return parser,argeParseData

def displayLogging(target,reportId):
    print "[#] Logging to %s/report-%s.csv" % (Util.getReportDir(target),str(int(reportId)))
    print ""

def pinkwave_shell(argsDict = {},closeBrowser=True):
    # Execute exploit script
    timeStart = time.time()
    pentest = None

    # Single commands
    if isExploitInterface():
        # Displays info about exploit script
        options_shell(sys.argv[2])
    elif isMacroInterface():
        # Execute macros
        browser = get_browser()
        browser.driver.delete_all_cookies()
        macros = Util.strToArray(sys.argv[2])
        for m in macros:
            Macro(m).start()
    # Status command
    elif isStatusInterface():
        # Display pinkwave/server status
        status()
    # Multiple commands
    else:
        # Load parameters via dictionary or parameters
        if len(argsDict) != 0:
            shellParse = ShellParse(argsDict)
        else:
            parser, apData = argumentParser()
            args = vars(parser.parse_args())
            args.pop("status")
            shellParse = ShellParse(args)

        # Display info if not loaded via automate.py
        if closeBrowser:
            status()
            displayLogging(shellParse.target,shellParse.reportId)

        try:
            if shellParse.exploits is not None:
                name = shellParse.exploits
            print ""
            print "[%s]: %s%s%s" % (
                Util.getConfig("browser"), colors.YELLOW,name, colors.COLOR_END)
            v = vars(shellParse)
            print json.dumps(v, sort_keys = False, indent = 4)
            browser = get_browser()
            browser.driver.delete_all_cookies()

            pentest = Pentest().create(browser, shellParse)
            if pentest.macros == [] and pentest.target is None:
                print "(-t) target is missing"
            elif pentest.macros == [] and pentest.exploits == []:
                print "(-e) exploits are required"
            else:
                pentest.start()
        except vdkException as e:
            print "%s[!] %s%s" % (colors.RED,e ,colors.COLOR_END)
            if closeBrowser and browser is not None:
                browser.close()

            return False

        except PyExploitException as e:
            print "%s[!] PyExploitException error: %s%s" % (colors.RED,e ,colors.COLOR_END)
            if closeBrowser and browser is not None:
                browser.close()

            return False

        except Exception as e:
            print "%s[!!!] Unknown error: %s%s" % (colors.RED,e ,colors.COLOR_END)
            if closeBrowser and browser is not None:
                browser.close()

            raise # means an exception triggered the exiting.

        print "test execution time: %d seconds" % (time.time() - timeStart)
        if closeBrowser:
            browser.close()
        return True

"""
Counts exploits per type
"""
def count_exploits():
    exploits = 0
    pyFiles = 0
    for root, subdirs, files in os.walk("exploits"):
        for f in files:
            if f.endswith(".dat"):
                fPath = root + "/" + f
                with open(fPath,"r") as cFile:
                    for line in cFile.readlines():
                        exploits += 1
            elif f.endswith(".py") and not f.startswith('__init__'):
                pyFiles += 1
    return exploits,pyFiles

"""
View options for exploit script
"""
def options_shell(pathToExploit):
    if not isfile(pathToExploit) and not isfile(pathToExploit + ".py"):
        raise Exception("Exploit not found in path: %s" % pathToExploit)

    pye = PyExploit(pathToExploit)
    options = pye.options
    print "%s[%s]%s > %sshow parameters%s" % (colors.GREEN, pathToExploit, colors.COLOR_END, colors.YELLOW, colors.COLOR_END)
    print ""
    print "Exploit options (%s)" % pathToExploit
    print ""
    for option in options:
        parser, dictArray = argumentParser()
        for d in dictArray:
            if d['long'] == "--" + option:
                print "[--%s] %s" % (option,d['help'])
    print ""
    dependencies = pye.dependencies
    if len(dependencies) != 0:
        print "Dependencies:"
        for key in dependencies:
            print "%s (%s)" % (key,dependencies[key])
    print ""
    print ""

def isExploitInterface():
    return len(sys.argv) == 3 and (sys.argv[1] == "-e" or sys.argv[1] == "--exploits")

def isStatusInterface():
    return len(sys.argv) == 2 and (sys.argv[1] == "-s" or sys.argv[1] == "--status")

def isHelpInterface():
    return len(sys.argv) == 2 and (sys.argv[1] == "-h" or sys.argv[1] == "--help")

def isMacroInterface():
    return len(sys.argv) == 3 and (sys.argv[1] == "-m" or sys.argv[1] == "--macros")

if __name__ == '__main__':
    # Do not start server when viewing exploit info
    if not isExploitInterface() and not isHelpInterface():
        pinkserver.start(Util.getConfig("http-port"))
        time.sleep(2)

    # Will exit(1) when vulnerabilities are found
    secure = pinkwave_shell()
    if not secure:
        exit(1)
