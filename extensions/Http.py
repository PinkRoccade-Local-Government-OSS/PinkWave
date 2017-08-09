#!/usr/bin/python
"""
Http Extension
Verify status_codes/headers and make HEAD,POST,GET,PUT,DELETE requests
"""

import requests
from requests.exceptions import ConnectionError

from Util import Util

# If ssl-verify is false disable insecure request warnings
if Util.getConfig("ssl-verify") != True:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
Verify if status is 200/201 (OK) with HEAD request
"""
def is_ok(url):
    result = False
    try:
        response = head(url)
        result = response.status_code == 200 or response.status_code == 201
    except ConnectionError:pass
    return result

"""
Verify if status is 200/201 (OK) with GET request
"""
def is_ok_get(url):
    result = False
    try:
        response = get(url)
        result = response.status_code == 200 or response.status_code == 201
    except ConnectionError:pass
    return result

"""
Verify if status is 404 (Not Found)
"""
def is_not_found(url):
    result = False
    try:
        response = head(url)
        result = response.status_code == 404
    except ConnectionError:
        result = True

    return result

"""
Verify if a header is present
"""
def has_header(url,header):
    return header in headers(url)

"""
Get headers with HEAD request
"""
def headers(url):
    response = head(url)
    return response.headers

"""
Get request
"""
def get(url,auth = None):
    verify = Util.getConfig("ssl-verify") == True
    return requests.get(url, verify=verify,auth=auth)

"""
Get request
"""
def post(url,dataDict):
    verify = Util.getConfig("ssl-verify") == True
    return requests.post(url,verify=verify,data=dataDict)

"""
Get request
"""
def delete(url,dataDict):
    verify = Util.getConfig("ssl-verify") == True
    return requests.delete(url, verify=verify,data=dataDict)

"""
Get request
"""
def put(url,dataDict):
    verify = Util.getConfig("ssl-verify") == True
    return requests.put(url, verify=verify,data=dataDict)

"""
Head request
"""
def head(url):
    verify = Util.getConfig("ssl-verify") == True
    return requests.head(url, verify=verify)

"""
Options request
"""
def options(url):
    verify = Util.getConfig("ssl-verify") == True
    return requests.options(url, verify=verify)

if __name__ == '__main__':
    from unittest import TestCase
    from unittest import main

    class testCalc(TestCase):
        def test_ExistingUrl(self):
            url = "https://badssl.com"
            self.assertTrue(is_ok(url))
            self.assertFalse(is_not_found(url))

        def test_hasHSTSHeaders(self):
            url = "https://hsts.badssl.com/"
            result = has_header(url, "Strict-Transport-Security")
            self.assertTrue(result)

        def test_NonExistingSite(self):
            url = "http://someweirdurlthatnotexists.com"
            self.assertTrue(is_not_found(url))
            self.assertFalse(is_ok(url))

        def test_NonExistingUrl(self):
            url = "https://reddit.com/iuadhiuadshuadsihi"
            self.assertFalse(is_ok(url))

        def test_has_headers(self):
            url = "https://badssl.com"
            result = has_header(url,"Content-Type")
            self.assertTrue(result)

        def test_hasNoHSTSHeaders(self):
            url = "https://subdomain.preloaded-hsts.badssl.com/"
            result = has_header(url, "Strict-Transport-Security")
            self.assertFalse(result)
    main()
