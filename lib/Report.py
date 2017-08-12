#!/usr/bin/python

"""
The Report class is used by Pentest to create a report of found vulnerabilities and tests using thread safe file writing.
"""

import sys,os,time,math,threading
from os.path import isfile,abspath,dirname,basename
from datetime import datetime
from urllib2 import URLError

# Import PinkWave extensions
appDir = dirname(dirname(__file__ ))
sys.path.append(appDir)
from extensions.Util import Util,vdkException

class Report:

    def __init__(self, pyExploit,message,totalTime):
        self.pentest = pyExploit.pentest
        self.browser = pyExploit.pentest.browser
        self.exploit = pyExploit.exploitPath
        self.exploitName = basename(self.exploit).split(".")[0]
        self.message = message
        self.totalTime = totalTime
        self.request = pyExploit.pentest.browser.request
        self.requestNames = pyExploit.pentest.requestNames
        self.labels = pyExploit.labels
        if isinstance(self.labels, list):
            self.labels = ",".join(self.labels)

    def export(self):
        # Creating private folder default folder structure
        privateFolder = Util.getAppDir() + "/private"
        defaultDirs = ['hosts','macros','wordlist','tests']
        Util.createDir(privateFolder)
        for defaultDir in defaultDirs:
            Util.createDir(privateFolder + "/" + defaultDir)

        Util.makeFileIfNotExists(privateFolder + "/__init__.py")
        Util.makeFileIfNotExists(privateFolder + "/macros/__init__.py")

        # Creating report folder default folder structure within host
        reportDir = Util.getReportDir(self.pentest.target)
        Util.createDir(reportDir)
        reportFile = "%s/report-%s.csv" % (reportDir, self.pentest.reportId)

        # Generating report data
        today = datetime.today()
        flagged = "Yes"
        if self.message == "OK":
            flagged = "No"

        byteSize = 0
        cookies = []
        try:
            if len(self.browser.url()) != 0:
                byteSize = self.browser.byteSize()
                cookies = self.browser.cookies()
        except URLError:
            print "Setting byteSize=0 and cookies=[] because Browser is not used"

        # Building log file
        my_list = []
        my_list.append(("Date",today.strftime('%Y-%m-%d %H:%M:%S')))
        my_list.append(("Flagged",flagged))
        my_list.append(("Labels",self.labels))
        my_list.append(("Script",self.exploit))
        my_list.append(("Target",self.pentest.target))
        my_list.append(("Request Type",self.browser.request.upper()))
        my_list.append(("Parameters",self.pentest.parameters()))
        my_list.append(("Comment",self.message))
        my_list.append(("Time",self.totalTime))
        my_list.append(("Length",byteSize))
        my_list.append(("Cookies",cookies))

        exists = isfile(reportFile)
        f = open(reportFile,'a+')
        try:
            if not exists:
                header = ""
                for li in my_list:
                    header += '"' + Util.escapeQuotes(li[0]) + '",'

                header = header.strip(",")
                f.write(header + os.linesep)

            log = ""
            for li in my_list:
                log += '"' + Util.escapeQuotes(li[1]) + '",'

            log = log.strip(",")
            f.write(log + os.linesep)
        finally:
            f.close()
