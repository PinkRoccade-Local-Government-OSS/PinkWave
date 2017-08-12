#!/usr/bin/python
"""
automate.py can execute multiple tests based on a JSON file

usage ./automate.py [testfile]

Please read to the docs/ to see the format of the test file.

example:

./automate.py private/tests/mytest.json
"""

import pinkwave
import server.pinkserver as pinkserver
from pinkwave import pinkwave_shell
import sys,time

from os.path import isdir,isfile

from lib.TestParse import TestParse
from extensions.Util import Util,vdkException

def usage():
    print "usage: python automate.py [testfile]"
    exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()

    pinkserver.start(9000)
    pinkwave.status()

    testFile = sys.argv[1]
    if not isfile(testFile):
        print "is not a file: %s" % testFile
        usage()

    timeStart = time.time()
    parser = TestParse(testFile)
    reportId = None
    vulnsFound = False;

    for test in parser.tests:
        if reportId is None:
            reportFolder = Util.getReportDir(test["target"])
            if isdir(reportFolder):
                reportId = Util.countExtensions(folder=reportFolder,ext="csv")
                reportId += 1
            else:
                reportId = 1

            pinkwave.displayLogging(test["target"],reportId)

            time.sleep(2)
        test["reportId"] = str(reportId)
        secure = pinkwave_shell(test,False)
        if secure != True:
            vulnsFound = True

    pinkwave.browser.close()
    if vulnsFound:
        print ""
        print "\033[1;91m[!] Vulnerabilities found\033[1;m"
    print "automate.py execution time: %d seconds" % (time.time() - timeStart)
    if vulnsFound:
        exit(1)
