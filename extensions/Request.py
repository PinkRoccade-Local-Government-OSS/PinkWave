#!/usr/bin/python

"""
Request Extension
Execute browser actions by using the Selenium webdriver
"""

from Util import Util

def do(pentest,parameters=[]):
    if pentest.request.lower() == "post":
        return post(pentest.target,pentest.requestNames,parameters)
    elif pentest.request.lower() == "post/direct":
        return directpost(pentest.target,pentest.requestNames,parameters)
    else:
        return get(pentest.target,pentest.requestNames,parameters)

def get(url,requestNames=[], parameters=[]):
    r = Request()
    if len(requestNames) != 0:
        url = Util.transformUrl(url,requestNames, parameters)
        Request.browser.nav(url)
    else:
        Request.browser.nav(url)

    return r.generateObject()

def post(url,requestNames, parameters=[]):
    r = Request()
    Request.browser.nav(url)
    Request.browser.post(requestNames, parameters)
    return r.generateObject()

def directpost(url,requestNames,parameters=[]):
    r = Request()
    Request.browser.directPost(url,requestNames,parameters)
    return r.generateObject()

"""
The Request class can be used in an exploit to make a GET/POST request with the Selenium webdriver
"""

class Request:

    browser = None

    @staticmethod
    def setBrowser(browser):
        Request.browser = browser

    def __init__(self):
        self.hash = None
        self.bytes = None
        self.time = None
        self.text = None
        self.cookies = None
        self.url = None

    """
    Return Request object
    """
    def generateObject(self):
        browser = Request.browser
        if browser is None:
            raise Exception("Browser is not set for Request")

        self.hash = browser.hash()
        self.bytes = len(browser.text())
        self.time = browser.time()
        self.text = browser.text()
        self.cookies = browser.cookies()
        self.url = browser.url()
        self.created = True
        return self
