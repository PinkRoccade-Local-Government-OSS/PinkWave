#!/usr/bin/python

"""
The Macro class can be used to load macro scripts written in Python
"""
import os
from os.path import isfile
import importlib
from time import sleep

import sys,os
from os.path import dirname,abspath
from os import walk

# Importing PinkWave extensions
sys.path.append(dirname(dirname(abspath(__file__))))
from extensions.Util import Util

class Macro:

    def __init__(self,macroPath):
        self.macroPath = macroPath
        if not isfile(self.macroPath):
            raise Exception("Macro not found in path: %s" % macroPath)

    def start(self):
        macroName = self.macroPath.replace(Util.getAppDir(),"")
        macroName = macroName.strip("/")
        macroName = macroName.replace(".py", "")
        macroName = macroName.replace("/",".")
        mod = importlib.import_module(macroName)
        try:
            mod.start()
        except AttributeError:
            print "Macro %s has no 'start()' function" % macroName
            raise
        sleep(3)
