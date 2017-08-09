#!/usr/bin/python

"""
TestParse can read JSON files and converts it to lists of dictionaries which can be used by ShellParse
"""

import json
from os.path import isfile
from lib.ShellParse import ShellParse

class TestParse:
    def __init__(self,jsonFile):
        d = loadJsonFile(jsonFile)
        self.tests = transformTests(d)

def transformTests(d):
    tests = []
    for test in d["tests"]:
        target = test["target"]
        for exploits in test["exploits"]:
            exploitTests = {}
            exploitTests["target"] = target

            for key in exploits.iterkeys():
                exploitTests[str(key)] = exploits[key]
            tests.append(exploitTests)

    return tests

def loadJsonFile(f):
    if not isfile(f):
        raise Exception("Test file not found: %s" % f)

    with open(f,"r") as f:
        d = json.loads("".join(f.readlines()))
        if len(d) == 0:
            raise Exception("Empty Test file: %s" % f)

        return d
