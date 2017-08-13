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
Verify if status is 200/201 (OK) with GET request
"""
def is_ok(url,auth=None):
    result = False
    try:
        response = get(url,auth=auth)
        result = response.status_code == 200 or response.status_code == 201
    except ConnectionError:pass
    return result

"""
Verify if status is 200/201 (OK) with HEAD request
"""
def is_ok_head(url,auth=None):
    result = False
    try:
        response = head(url,auth=auth)
        result = response.status_code == 200 or response.status_code == 201
    except ConnectionError:pass
    return result

"""
Verify if status is 404 (Not Found) with GET request
"""
def is_not_found(url,auth=None):
    result = False
    try:
        response = get(url,auth=auth)
        result = response.status_code == 404
    except ConnectionError:
        result = True

    return result
"""
Verify if status is 404 (Not Found) with HEAD request
"""
def is_not_found_head(url,auth=None):
    result = False
    try:
        response = head(url,auth=auth)
        result = response.status_code == 404
    except ConnectionError:
        result = True

    return result

"""
Verify if a header is present with GET request
"""
def has_header(url,header,auth=None):
    return header in headers(url,auth)

"""
Get headers with GET request
"""
def headers(url,auth = None):
    response = get(url,auth=auth)
    return response.headers

"""
Verify if a header is present with HEAD request
"""
def has_header_head(url,header,auth=None):
    return header in headers_head(url,auth)

"""
Get headers with HEAD request
"""
def headers_head(url,auth = None):
    response = head(url,auth)
    return response.headers

"""
Get request
"""
def get(url,auth = None):
    verify = Util.getConfig("ssl-verify") == True
    return requests.get(url, verify=verify,auth=auth,timeout=Util.getConfig("timeout"))

"""
Get request
"""
def post(url,data = {},auth = None):
    verify = Util.getConfig("ssl-verify") == True
    return requests.post(url,verify=verify,data=data,auth=auth,timeout=Util.getConfig("timeout"))

"""
Get request
"""
def delete(url,data = {},auth = None):
    verify = Util.getConfig("ssl-verify") == True
    return requests.delete(url, verify=verify,data=data,auth=auth,timeout=Util.getConfig("timeout"))

"""
Get request
"""
def put(url,data = {},auth = None):
    verify = Util.getConfig("ssl-verify") == True
    return requests.put(url, verify=verify,data=data,auth=auth,timeout=Util.getConfig("timeout"))

"""
Head request
"""
def head(url,auth = None):
    verify = Util.getConfig("ssl-verify") == True
    return requests.head(url, verify=verify,auth=auth,timeout=Util.getConfig("timeout"))
