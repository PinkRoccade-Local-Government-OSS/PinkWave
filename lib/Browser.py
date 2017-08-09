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

    def __init__(self):
        self.driver = None
        self.timeout = None
        self.browser = None
        self.driverPath = None
        self.logging = True
        self.timeStart = 0
        self.timeEnd = 0
        self.request = "GET"
        bits = platform.architecture()[0]
        if "64" in bits:
            self.architecture = 64
        else:
            self.architecture = 32
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
    Create browser object with all variables
    """
    def create(self, browser):
        driverPath = self.getDriverPath(browser)

        if Util.getConfig("debug"):
            print "loading %s browser (driver:%s)" % (browser, driverPath)

        if browser.lower() == "firefox":
            fprofile = None
            if not Util.getConfig("ssl-verify"):
                fprofile = webdriver.FirefoxProfile()
                fprofile.accept_untrusted_certs = True

            self.driver = webdriver.Firefox(firefox_profile=fprofile)
        elif browser.lower() == "chrome":
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-xss-auditor')
            if not Util.getConfig("ssl-verify"):
                chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])

            self.driver = webdriver.Chrome(executable_path=driverPath,chrome_options=chrome_options)
        elif browser.lower() == "phantomjs":
            sargs = []
            if not Util.getConfig("ssl-verify"):
                sargs = ['--ignore-ssl-errors=true', '--ssl-protocol=any']

            self.driver = webdriver.PhantomJS(driverPath, service_log_path=os.path.devnull,service_args=sargs)

        self.browser = browser
        self.driverPath = driverPath
        self.driver.set_page_load_timeout(Util.getConfig("timeout"))
        return self

    """
    Create browser object with variables based on config file
    """
    def createFromConfig(self):
        browser = Util.getConfig("browser")
        return self.create(browser)

    """
    Navigate to URL into browser
    """
    def nav(self,url):
        self.driver.set_page_load_timeout(Util.getConfig("timeout"))
        if "://" not in url:
            url = "http://" + url

        if not Http.is_ok_get(url):
            raise Exception("Failed to establish connection to url %s" % url)

        if Util.getConfig("debug"):
            print "%sNavigating to %s%s" % ('\033[1;35m',url,'\033[0m')

        try:
            self.request = "GET"
            self.timeStart = time.time()
            self.driver.get(url)
            self.timeEnd = time.time()
        except UnexpectedAlertPresentException:
            #  Double exception handling because Selenium might close alert automaticly and might not (on Chrome for example)
            self.request = "GET"
            try:
                self.timeStart = time.time()
                self.driver.get(url)
                self.timeEnd = time.time()
            except UnexpectedAlertPresentException:
                self.timeStart = time.time()
                alert = self.driver.switch_to_alert()
                alert.accept()
                self.driver.get(url)
                self.timeEnd = time.time()
        except TimeoutException as t:
            self.timeEnd = time.time()
            raise vdkException("timeout triggered by webdriver");

    """
    Submits POST form to remote URL via bouncer
    """
    def directPost(self,url,requestNames,values):
        configFile = abspath(appDir + "/config/localhost.json")
        bouncer = Util.getBouncer()
        newUrl = Util.transformUrl(bouncer,["values",'url'],[",".join(requestNames),url])
        self.nav(newUrl)
        self.timeStart = time.time()
        self.post(requestNames,values)
        self.request = "POST/DIRECT"
        self.timeEnd = time.time()

    """
    Enter and submit POST form to current url
    """
    def post(self, requestNames, values):
        if requestNames is None or len(requestNames) == 0:
            raise Exception("requestNames is empty")

        if values is None or len(values) == 0:
            raise Exception("values is empty")

        try:
            self.driver.set_page_load_timeout(Util.getConfig("timeout"))
            self.timeStart = time.time()
            e = None

            self.request = "POST"
            if Util.getConfig("debug"):
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
            self.timeEnd = time.time()
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
        try:
            return self.driver.find_element_by_name(name)
        except NoSuchElementException:
            raise ElementNotFoundException

    """
    Get content from current browser window
    """
    def content(self):
        try:
            content = self.driver.page_source
        except UnexpectedAlertPresentException:
            #  Double exception handling because Selenium might close alert automaticly and might not (on Chrome for example)
            self.request = "GET"
            try:
                content = self.driver.page_source
            except UnexpectedAlertPresentException:
                alert = self.driver.switch_to_alert()
                alert.accept()
                content = self.driver.page_source
        except URLError:
            print "Connection refused for url: %s" % self.url()
            raise
        return content

    """
    Get size in bytes of current browser window content
    """
    def byteSize(self):
        return len(self.content())

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
    Get sha256 hash of the current URL content
    """
    def hash(self):
        m = hashlib.sha256()
        m.update(self.content().encode("utf8"))
        return m.digest().encode("hex")

    """
    Disable logging of all Browser functions
    """
    def disableLogging(self):
        self.logging = False
