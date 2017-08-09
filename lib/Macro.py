#!/usr/bin/python

"""
The Macro class can be used to load macro scripts written in Python
"""

from os.path import isfile
import importlib
from time import sleep

class Macro:

    def __init__(self):
        self.folder = "private/macros/"

    def start(self,macroName,browser):
        if self.folder in macroName:
            macroName = macroName.replace(self.folder,"")

        macroName = self.folder + macroName
        macroName = macroName.replace(".py", "")

        if not isfile(macroName + ".py"):
            raise Exception("Macro not found in path: %s" % macroName)

        macroNamePath = macroName
        macroName = macroName.replace("/",".")
        print "importing macro %s" % macroName
        mod = importlib.import_module(macroName)
        try:
            mod.start(browser)
        except AttributeError:
            raise Exception("Macro %s has no 'start(browser)' function" % macroNamePath)
        sleep(3)
