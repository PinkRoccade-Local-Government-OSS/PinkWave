#!/usr/bin/python

"""
The Util class contains a couple of static string/util functions
"""
import urllib
import os
from os.path import dirname,abspath,isfile,splitext,basename
import fnmatch
import json
import binascii
import subprocess

"""
raise the following exception within a pentest to generate a report
"""
class vdkException(Exception):pass

"""
Use report(msg) to generate report and exit pentest
"""
def report(msg):
    raise vdkException(msg)

"""
Read payloads from payload directory
"""
def payloads(name,file):
    payloads = []
    payloadDir = dirname(abspath(file))
    with open(payloadDir + "/payloads/" + name + ".dat","r") as f:
        for line in f:
            if len(line.strip()) == 0:
                continue
            payloads.append(line.strip())

    return payloads

class Util:

    """
    Get key value from config/localhost.json
    """
    @staticmethod
    def getConfig(key):
        configFile = abspath(Util.getAppDir() + "/config/config.json")
        with open(configFile, 'r') as json_file:
            d = json.load(json_file)
            return d[key]

    """
    Get random hex value of n characters
    """
    @staticmethod
    def getRandomHex(size):
        token = os.urandom(size/2)
        return token.encode('hex')

    """
    Get logger url based on config
    """
    @staticmethod
    def getLogger():
        port = Util.getConfig("http-port")
        return "http://localhost:%s/logger" % str(port)

    """
    Get bouncer url based on config
    """
    @staticmethod
    def getBouncer():
        port = Util.getConfig("http-port")
        return "http://localhost:%s/bouncer" % str(port)

    """
    Count files in folder with specific extension
    """
    @staticmethod
    def countExtensions(folder,ext):
        return len(fnmatch.filter(os.listdir(folder), '*.%s' % ext))

    """
    Get root of PinkWave path
    """
    @staticmethod
    def getAppDir():
        return abspath(dirname(dirname(__file__ )))


    """
    Get report directory for pentest
    """
    @staticmethod
    def getReportDir(target):
        host = Util.getHost(target)
        if len(host.strip()) == 0:
            raise Exception("No host specified")

        return Util.getAppDir() + "/private/hosts/" + host

    """
    Get secret value for logger
    """
    @staticmethod
    def getSecret():
        file = Util.getAppDir() + "/private/secret"
        if not isfile(file):
            with open(file,"a+") as f:
                f.write(Util.getRandomHex(64))

        with open(file,"r+") as f:
            return "".join(f.readlines()).strip()

    """
    Escape double quotes for report csv values
    """
    @staticmethod
    def escapeQuotes(s):
        if isinstance(s, unicode):
            s = s.encode('utf8')
        s = str(s)
        s = s.replace('"', '\\"')
        return s

    """
    Create url with parameters
    """
    @staticmethod
    def transformUrl(url, get_fields, values):
        tup = []

        if type(get_fields) is not list:
            raise TypeError("get_fields needs to be a list")

        if type(values) is list:
            if len(get_fields) != len(values):
                raise TypeError("Values length not equal to get_fields length")
            else:
                for i in range(0, len(values)):
                    tup.append((get_fields[i], values[i]))
        else:
            for gf in get_fields:
                tup.append((gf, values))

        return "%s?%s" % (url, urllib.urlencode(tup))

    """
    Seperate comma values into list if not a list already
    """
    @staticmethod
    def strToArray(s):
        if isinstance(s,list):
            return s

        sArr = []
        if s:
            for ss in s.split(","):
                sArr.append(ss.strip())
        return sArr

    """Get current hosts"""
    @staticmethod
    def getHost(url):
        url = url.split("?")[0]
        return url.split("//")[-1].split("/")[0]

    """Execute shell command """
    @staticmethod
    def shell(command,ignoreShellErrors=False):
        end = ""
        if ignoreShellErrors:
            end = ";exit 0"
        return subprocess.check_output(command + end, shell=True)

    """Create dir if not exists"""
    @staticmethod
    def createDir(path):
        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise

    """Create file if not exists"""
    @staticmethod
    def makeFileIfNotExists(path,content=""):
        if not os.path.isfile(path):
            with open(path,"a+") as f:
                f.write(content)
