#!/usr/bin/python

"""
Browser.py Providing easy and extended control to the Selenium Webdriver API
This enables to use a selenium webdriver object in an exploit
"""
import os,sys,time,json
from os.path import isfile,isdir,abspath,dirname
import hashlib
import urllib
import platform
from urllib2 import URLError
import requests

# Import Selenium framework
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

# Import PinkWave extensions
appDir = dirname(dirname(__file__ ))
sys.path.append(appDir)
from extensions.Util import Util,vdkException
import extensions.Http as Http
from extensions.Request import Request
"""
Exception classes for quering the DOM
"""
class ElementNotFoundException(NoSuchElementException):pass

"""
Browser Class
Providing easy and extended control to the Selenium Webdriver API
"""
class Browser:

    def __init__(self,browser,verifySsl = True, timeoutInSeconds=8,debugMode = False):
        self.driver = None
        self.browser = browser
        self.verifySsl = verifySsl
        self.request = "GET"
        self.timeoutInSeconds = timeoutInSeconds
        self.debugMode = debugMode
        if "64" in platform.architecture()[0]:
            self.architecture = 64
        else:
            self.architecture = 32
        self.driverPath = self.getDriverPath(self.browser)
        if self.browser.lower() == "firefox":
            fprofile = None
            if not verifySsl:
                fprofile = webdriver.FirefoxProfile()
                fprofile.accept_untrusted_certs = True

            self.driver = webdriver.Firefox(executable_path=self.driverPath,firefox_profile=fprofile)
        elif self.browser.lower() == "chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-xss-auditor')
            if not verifySsl:
                chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])

            self.driver = webdriver.Chrome(executable_path=self.driverPath,chrome_options=chrome_options)
        elif self.browser.lower() == "phantomjs":
            sargs = []
            if not verifySsl:
                sargs = ['--ignore-ssl-errors=true', '--ssl-protocol=any']

            self.driver = webdriver.PhantomJS(executable_path=self.driverPath, service_log_path=os.path.devnull,service_args=sargs)
        else:
            raise Exception("Browser %s not supported" % browser)

        self.driver.set_page_load_timeout(self.timeoutInSeconds)
        Request.setBrowser(self)

    """
    Searches for submit button, else submits element
    """
    def hitSubmit(self,element):
        try:
            self.driver.find_element_by_xpath("//input[@type='submit']").click()
        except (NoSuchElementException, ElementNotVisibleException,UnexpectedAlertPresentException):
            try:
                element.submit()
            # Sometimes previous elements are cached and therefore not to be found, try again a few times to be sure...
            except StaleElementReferenceException as sr:
                print "retrying to find cached element (StaleElementReferenceException)..."
                for i in range(0,5):
                    if i == 5:
                        raise sr

                    # Enter copy of hitSubmit function, to prevent recursion
                    try:
                        self.driver.find_element_by_xpath("//input[@type='submit']").click()
                    except (NoSuchElementException, ElementNotVisibleException,UnexpectedAlertPresentException):
                        try:
                            element.submit()
                        except:pass

    """
    Get Driver path based on browserName and architecture
    """
    def getDriverPath(self,browserName):
        root = dirname(dirname(abspath(__file__))) + "/drivers"
        if isdir(root) == False:
            raise Exception("Pinkwave Drivers Root not found: %s" % root)
        root += "/" + str(self.architecture)
        root += "/" + browserName.lower()
        if isdir(root) == False:
            raise Exception("Pinkwave Drivers Root not found: %s" % root)
        for filename in os.listdir(root):
            root += "/" + filename
            break
        if isfile(root) == False:
            raise Exception("Can't load Pinkwave Driver File: %s" % root)
        return root



    """
    Navigate to URL into browser
    """
    def nav(self,url):
        self.driver.set_page_load_timeout(self.timeoutInSeconds)
        if "://" not in url:
            url = "http://" + url

        if not Http.is_ok_get(url):
            raise Exception("Failed to establish connection to url %s" % url)

        if self.debugMode:
            print "%sNavigating to %s%s" % ('\033[1;35m',url,'\033[0m')

        try:
            self.request = "GET"
            self.driver.get(url)
        except UnexpectedAlertPresentException:
            #  Double exception handling because Selenium might close alert automaticly and might not (on Chrome for example)
            self.request = "GET"
            try:
                self.driver.get(url)
            except UnexpectedAlertPresentException:
                alert = self.driver.switch_to_alert()
                alert.accept()
                self.driver.get(url)
        except TimeoutException as t:
            raise vdkException("timeout triggered by webdriver");

    """
    Submits POST form to remote URL via bouncer
    """
    def directPost(self,url,requestNames,values):
        bouncer = Util.getBouncer()
        newUrl = Util.transformUrl(bouncer,["values",'url'],[",".join(requestNames),url])
        self.nav(newUrl)
        self.post(requestNames,values)
        self.request = "POST/DIRECT"

    """
    Enter and submit POST form to current url
    """
    def post(self, requestNames, values):
        if requestNames is None or len(requestNames) == 0:
            raise Exception("requestNames is empty")

        if values is None or len(values) == 0:
            raise Exception("values is empty")

        try:
            self.driver.set_page_load_timeout(self.timeoutInSeconds)
            e = None

            self.request = "POST"
            if self.debugMode:
                print "Posting to %s, fields: [%s], data: [%s]" % (self.url(), requestNames, values)

            if not isinstance(values,list):
                for post in requestNames:
                    e = self.driver.find_element_by_name(post)
                    e.clear()
                    values = values.strip(os.linesep)
                    e.send_keys(values)
            else:
                if len(requestNames) != len(values):
                    raise Exception("requestNames length does not match with values length")

                postIndex = 0
                for val in values:
                    e = self.driver.find_element_by_name(requestNames[postIndex])
                    e.clear()
                    val = val.strip(os.linesep)
                    e.send_keys(val)
                    postIndex = postIndex + 1

            self.hitSubmit(e)
        except TimeoutException as t:
            raise vdkTimeoutException("Timeout triggered by WebDriver");
        except NoSuchElementException as nse:
            print "Element not found by POST names: %s" % ",".join(requestNames)
            raise nse
        except UnicodeDecodeError as u:
            if isinstance(values,list):
                for val in values:
                    val = unicode(val, errors='replace')
            else:
                values = unicode(values,errors='replace')
            return self.post(requestNames,values)
        except WebDriverException as we:
            self.nav(self.url())
            self.post(requestNames,values)

    """
    Api for querying elements by name
    """
    def getElementByName(self,name):
        return self.driver.find_element_by_name(name)

    """
    Get text from current browser window
    """
    def text(self):
        try:
            text = self.driver.page_source
        except UnexpectedAlertPresentException:
            #  Double exception handling because Selenium might close alert automaticly and might not (on Chrome for example)
            self.request = "GET"
            try:
                text = self.driver.page_source
            except UnexpectedAlertPresentException:
                alert = self.driver.switch_to_alert()
                alert.accept()
                text = self.driver.page_source
        except URLError:
            print "Connection refused for url: %s" % self.url()
            raise
        return text

    """
    Get size in bytes of browser text
    """
    def byteSize(self):
        return len(self.text())

    """
    Get current URL from browser
    """
    def url(self):
        url = self.driver.current_url
        return url.strip("/").encode("utf8")

    """
    Save current window as screenshot in given path
    """
    def saveScreenshot(self,path):
        self.driver.save_screenshot(path)

    """
    Kill the webdriver process
    """
    def close(self):
        self.driver.quit()

    """
    Get all cookies from current session
    """
    def cookies(self):
        cookies = self.driver.get_cookies()
        if len(cookies) == 0:
            cookies = []
        else:
            for cookie in cookies:
                if cookie.get('httpOnly') is None:
                    cookie['httpOnly'] = False
                if cookie.get('secure') is None:
                    cookie['secure'] = False
        return cookies

    """
    Get title of current URL
    """
    def title(self):
        return self.driver.title

    """
    Calculate and return request time
    """
    def time(self):
        return self.timeEnd - self.timeStart

    """
    Get sha256 hash of the current URL text
    """
    def hash(self):
        m = hashlib.sha256()
        m.update(self.text().encode("utf8"))
        return m.digest().encode("hex")

    """
    Disable logging of all Browser functions
    """
    def disableLogging(self):
        self.logging = False
