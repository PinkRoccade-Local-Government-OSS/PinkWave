HTTP Extension
======

The HTTP extension is an higher level API for the Request.py library. 

Selenium has some limitations, HTTP.py can be used to fetch headers or perform GET/POST/PUT/DELETE requests.

You can also just use requests.py, but keep in mind to use the configuration value "ssl-verify" to either verify ssl certifates or not and do error handling. 

The power of  HTTP.py:
```
>>> import extensions.Http as Http
>>> Http.is_ok('http://google.com')
>>> True
>>> Http.has_header('http://google.com','Content-Type')
>>> True
>>> h = Http.get('https://httpbin.org/get?hello=world',auth=('admin','admin'))
>>> print h.text
"{
  "args": {
    "hello": "world"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Authorization": "Basic YWRtaW46YWRtaW4=", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.12.3"
  }, 
  "origin": "194.171.225.106", 
  "url": "https://httpbin.org/get?hello=world"
}"
>>> h = Http.post('https://httpbin.org/post',data={'hello':'world'})
>>> print h.text
"{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "hello": "world"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Connection": "close", 
    "Content-Length": "11", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.12.3"
  }, 
  "json": null, 
  "origin": "194.171.225.106", 
  "url": "https://httpbin.org/post"
}
"
```

## get(url,auth=None)
Use a GET request to fetch a response from an URL.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |

get request with basic auth:
```
>>> h = Http.get("https://httpbin.org/get",('admin','admin'))
>>> print h.text
{
  "args": {}, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Authorization": "Basic YWRtaW46YWRtaW4=", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.12.3"
  }, 
  "origin": "194.171.225.106", 
  "url": "https://httpbin.org/get"
}
```

## post(url,auth=None,data={})
Use a POST request to fetch a response from an URL.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |
| **data** (dict) | post data | 

post request:
```
>>> h = Http.post("https://httpbin.org/post",{'product':1,'comment':'hello'})
>>> print h.text
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "comment": "hello", 
    "product": "1"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Connection": "close", 
    "Content-Length": "23", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.12.3"
  }, 
  "json": null, 
  "origin": "194.171.225.106", 
  "url": "https://httpbin.org/post"
}
```
## put(url,auth=None,data={})
Use a PUT request to fetch a response from an URL.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |
| **data** (dict) | post data | 

put request:
```
>>> h = Http.put("https://httpbin.org/put",{'product':1,'comment':'updated comment'})
>>> print h.text
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "comment": "updated comment", 
    "product": "1"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Connection": "close", 
    "Content-Length": "33", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.12.3"
  }, 
  "json": null, 
  "origin": "194.171.225.106", 
  "url": "https://httpbin.org/put"
}
```

## delete(url,auth=None,data={})
Use a DELETE request to fetch a response from an URL.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |
| **data** (dict) | post data | 

delete request:
```
>>> h = Http.delete("https://httpbin.org/delete",{'product':'1'})
>>> print h.text
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "product": "1"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Accept-Encoding": "gzip, deflate", 
    "Connection": "close", 
    "Content-Length": "9", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "User-Agent": "python-requests/2.12.3"
  }, 
  "json": null, 
  "origin": "194.171.225.106", 
  "url": "https://httpbin.org/delete"
}
```
## head(url,auth=None)
Use a HEAD request to fetch a response from an URL.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |

head request:
```
>>> h = Http.head('https://httpbin.org/head')
>>> print h.headers
{'Content-Length': '233', 'X-Processed-Time': '0.000776052474976', 'X-Powered-By': 'Flask', 'Server': 'meinheld/0.6.1', 'Connection': 'keep-alive', 'Via': '1.1 vegur', 'Access-Control-Allow-Credentials': 'true', 'Date': 'Sun, 13 Aug 2017 12:50:00 GMT', 'Access-Control-Allow-Origin': '*', 'Content-Type': 'text/html'}
```

# is_ok(url,auth=None)
Verify that GET request to url response with a status code 200 or 201.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |

verify that site is live:
```
>>> Http.is_ok("https://google.com")
True
```

# is_ok_head(url,auth=None)
Verify that HEAD request to url response with a status code 200 or 201. A HEAD request is faster than GET, but some hosts may block it.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |

Hosts may block HEAD requests from requests.py:
```
>>> Http.is_ok_head("https://google.com")
False
```

# is_not_found(url,auth=None)
Verify that GET request to url response with a status code 404 or ConnectionError.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |

Website that does not exists:
```
>>> Http.is_not_found("http://somefakewebsitename.faketld/")
True
```
# is_not_found_head(url,auth=None)
Verify that HEAD request to url response with a status code 404 or ConnectionError. A HEAD request is faster than GET, but some hosts may block it.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |

Website that does not exists:
```
>>> Http.is_not_found("http://somefakewebsitename.faketld/")
True
```

# has_headers(url,header, auth=None)
Verify that GET response contains a specific headers.

|  |  |
|--|--|
| **url** (string) | the target |
| **header** (string) | header name |
| **auth** (tuple of strings) | basic auth credentials |

Verify that website has Content-Type header:
```
>>> Http.has_header('http://google.com','Content-Type')
True
```

# has_headers_head(url,header, auth=None)
Verify that HEAD response contains a specific headers. A HEAD request is faster than GET, but some hosts may block it.

|  |  |
|--|--|
| **url** (string) | the target |
| **header** (string) | header name |
| **auth** (tuple of strings) | basic auth credentials |

Hosts may block HEAD requests from requests.py:

```
>>> Http.has_header_head('http://google.com','Content-Type')
False
```

# headers(url, auth=None)
Get headers from GET response.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |

Headers from host:

```
>>> Http.headers("https://google.com")
{'X-XSS-Protection': '1; mode=block', 'Content-Encoding': 'gzip', 'Transfer-Encoding': 'chunked', 'Set-Cookie': 'NID=109=foWVsRn4zBUTTOw2sjYqexCWKuaUdHpXodtWHl89YcE9ELnh-IBwOBt_YsUKB6a14v3Uh6beQPfVWVWLq5Qm4PKYCv-DvvGEixdyeWwd80MISa4G_nvAA6sT6hfSG3dn; expires=Mon, 12-Feb-2018 12:46:59 GMT; path=/; domain=.google.nl; HttpOnly', 'Expires': '-1', 'Server': 'gws', 'Cache-Control': 'private, max-age=0', 'Date': 'Sun, 13 Aug 2017 12:46:59 GMT', 'P3P': 'CP="This is not a P3P policy! See https://www.google.com/support/accounts/answer/151657?hl=en for more info."', 'Alt-Svc': 'quic=":443"; ma=2592000; v="39,38,37,35"', 'Content-Type': 'text/html; charset=ISO-8859-1', 'X-Frame-Options': 'SAMEORIGIN'}
```

# headers_head(url, auth=None)
Get headers from HEAD response. A HEAD request is faster than GET, but some hosts may block it.

|  |  |
|--|--|
| **url** (string) | the target |
| **auth** (tuple of strings) | basic auth credentials |

Hosts may block/send different HEAD requests from requests.py:

```
>>> Http.headers("https://google.com")
{'Content-Length': '259', 'Alt-Svc': 'quic=":443"; ma=2592000; v="39,38,37,35"', 'Location': 'https://www.google.nl/?gfe_rd=cr&ei=l0qQWdyIEqjc8Af4ioXwCQ', 'Cache-Control': 'private', 'Date': 'Sun, 13 Aug 2017 12:48:23 GMT', 'Referrer-Policy': 'no-referrer', 'Content-Type': 'text/html; charset=UTF-8'}

```
# has_headers_head(url,header, auth=None)
Verify that HEAD response contains a specific headers. A HEAD request is faster than GET, but some hosts may block it.

|  |  |
|--|--|
| **url** (string) | the target |
| **header** (string) | header name |
| **auth** (tuple of strings) | basic auth credentials |

Hosts may block HEAD requests from requests.py:

```
>>> Http.has_header_head('http://google.com','Content-Type')
False
```
