#!/usr/bin/python

"""
Flags Extension
Compare request with a list of requests to find inconsistenties
"""

from Util import vdkException
import diff

class Flags:
    def __init__(self,request,requestList):
        self.request = request
        self.requestList = requestList

    def timeout(self,maxTime=8):
        if self.request.time >= maxTime:
            raise vdkException("[high] Request took to long: %s" % str(self.request.time))

    def differentContent(self):
        baseHash = self.requestList[0].hash
        sameHash = True
        for o in self.requestList:
            if o.hash != baseHash:
                sameHash = False

        if sameHash:
            if baseHash != self.request.hash:
                raise vdkException("[low] Content is not the same")

    def containsKeyword(self,contains):
        for req in self.requestList:
            differenceStr = diff.diff(req.content,self.request.content)
            if contains.lower() in differenceStr.lower():
                raise vdkException("[medium] Contains keyword: [%s] in diff" % contains)

    def differentUrls(self):
        baseUrl = self.requestList[0].url
        sameUrl = True
        for o in self.requestList:
            if o.url != baseUrl:
                sameUrl = False

        if sameUrl:
            if baseUrl != self.request.url:
                raise vdkException("[medium] Different URL detected")
