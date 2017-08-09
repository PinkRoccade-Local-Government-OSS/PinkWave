#!/usr/bin/python

"""
ShellParse converts allowed dictionary values to defined properties.
This makes is possible to create a Pentest via the pinkwave.py interface using a dictionary object.
"""

import sys
from os.path import dirname

# Import PinkWave extensions
appDir = dirname(dirname(__file__ ))
sys.path.append(appDir)
from extensions.Util import Util

def _getdir(dir,key,valueIfNone):
    if dir.get(key) is None:
        return valueIfNone
    else:
        return dir.get(key)

class ShellParse:

    def __init__(self,dict):
        self.target = None
        self.exploits = None
        self.requestNames = None
        self.request = None
        self.macros = None
        self.creds = None
        self.ports = None
        self.wordlist = None
        self.ssl = None
        self.reportId = None

        # Required
        self.target = dict.get("target")
        self.exploits = dict.get("exploits")

        # With default values
        self.ssl = _getdir(dict,'ssl',"443")
        self.reportId = _getdir(dict,"reportId","0")
        self.request = _getdir(dict,"request","get")
        if dict.get("macros") is None:
            self.macros = []
        else:
            self.macros = Util.strToArray(dict.get("macros"))

        # Optional
        if dict.get("requestNames") is not None:
            self.requestNames = Util.strToArray(dict.get('requestNames'))

        if dict.get('creds') is not None:
            self.creds = Util.strToArray(dict.get('creds'))

        if dict.get('ports') is not None:
            self.ports = Util.strToArray(dict.get('ports'))

        self.wordlist = dict.get("wordlist")


        # Required check
        if self.target is None:
            raise Exception("required parameter missing: target")

        if self.exploits is None:
            raise Exception("required parameter missing: exploits")

    def convertListToString(self,l):
        tmpL = []
        for i in l:
            tmpL.append(str(i))

        return tmpL

    def propsValue(self):
        dict = {}
        properties = self.props()
        for key in properties:
            value = getattr(self, key)
            dict[key] = value

        return dict

    def props(self):
        methods = ["props","propsValue"]
        properties = []
        for key in dir(self):
            if not key.startswith("__") and key not in methods:
                properties.append(key)

        return properties

if __name__ == "__main__":
    obj = ShellParse({"target":"google.com","creds":"test","ports" : "80,433"})
    for o in obj.propsValue().iteritems():
        print o
