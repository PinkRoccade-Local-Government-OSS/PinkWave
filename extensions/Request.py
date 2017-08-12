#!/usr/bin/python

"""
Request Extension
Execute browser actions by using the Selenium webdriver
"""

from Util import Util
from selenium.common.exceptions import NoSuchElementException
import time

def has_element(formname):
    has_element = False
    try:
        has_element = Request.browser.getElementByName(formname)
    except NoSuchElementException:
        pass

    return has_element

def do(pentest,parameters=[]):
    if pentest.request.lower() == "post":
        return post(pentest.target,pentest.requestNames,parameters)
    elif pentest.request.lower() == "post/direct":
        return directpost(pentest.target,pentest.requestNames,parameters)
    else:
        return get(pentest.target,pentest.requestNames,parameters)

def get(url,requestNames=[], parameters=[]):
    timeStart = time.time()
    r = Request()
    if len(requestNames) != 0:
        url = Util.transformUrl(url,requestNames, parameters)
        Request.browser.nav(url)
    else:
        Request.browser.nav(url)

    return r.generateObject(timeStart)

def post(url,requestNames, parameters=[]):
    timeStart = time.time()
    r = Request()
    Request.browser.nav(url)
    Request.browser.post(requestNames, parameters)
    return r.generateObject(timeStart)

def directpost(url,requestNames,parameters=[]):
    timeStart = time.time()
    r = Request()
    Request.browser.directPost(url,requestNames,parameters)
    return r.generateObject(timeStart)

"""
Set Browser
"""
def setBrowser(browser):
    Request.setBrowser(browser)

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
    def generateObject(self,timeStart):
        endTime = time.time()
        totalTime = endTime-timeStart
        browser = Request.browser
        if browser is None:
            raise Exception("Browser is not set for Request")

        self.hash = browser.hash()
        self.bytes = len(browser.text())
        self.time = totalTime
        self.text = browser.text()
        self.cookies = browser.cookies()
        self.url = browser.url()
        self.created = True
        return self
