Request Extension
======

Request.py like API for the Selenium browser:

```
>>> from lib.Browser import Browser
>>> import extensions.Request as Request
>>> b = Browser().createFromConfig()
>>> Request.setBrowser(b)
>>> r = Request.get("https://google.com")
>>> r.cookies
"[{u'domain': u'.google.nl', u'name': u'NID', u'expires': u'za, 10 feb. 2018 12:15:07 GMT', u'value': u'109=V-vYRUq028zZzc2HcQjnx7fcfL0xnTFSqwJ9Zgb2xKp7_uutC84Bck1daE5b41A8DhvQQsKaVywL-bUXQ47n38X1llQIupgUeueyK7rFbQYKcbF1txt8xwVNz1t31P0X', u'expiry': 1518264907, 'httpOnly': False, u'path': u'/', u'httponly': True, u'secure': False}]"
>>> r.text
"
...
large html snippet
...
"
```

## get(url,requestNames=[],parameters=[])
Navigate to URL with optional parameters.
|  |  |
|--|--|
| **url** (string) | the target |
| **requestNames** (list of strings) | url parameters |
| **values** (list of strings) | parameter values |

hello world:
```
>>> r = Request.get("https://httpbin.org/get",['hello'],['world'])
>>> r.text
...
"args": {
    "hello": "world"
  }
...
"url": "https://httpbin.org/get?hello=world"
...
```


## post(url,requestNames=[],parameters=[])
Use post if you want to submit a form via Selenium.
|  |  |
|--|--|
| **url** (string) | the target |
| **requestNames** (list of strings) | form names, for example: ['user','pass'] |
| **values** (list of strings) | form values, for example: ['admin','secret'] |

login to website:
```
>>> r = Request.post("https://wordpress.com/log-in",['usernameOrEmail','password'],['myusername','mypassword'])
>>> r.text
...
large html snippet
...

```


## directpost(url,requestNames=[],parameters=[])
Submit a direct post request via Selenium. (for CSRF testing)
|  |  |
|--|--|
| **url** (string) | the target |
| **requestNames** (list of strings) | form names, for example: ['user','pass'] |
| **values** (list of strings) | form values, for example: ['admin','secret'] |

login to website:
```
>>> r = Request.post("http://httpbin.org/post",['usernameOrEmail','password'],['myusername','mypassword'])
>>> r.text
...
large html snippet
...

```

## do(pentest,parameters=[])
Execute request based on pentest configuration.

|  |  |
|--|--|
| **pentest** (Pentest) | Pentest object |
| **values** (list of strings or string) | payload value(s) |

```
>>> r = Request.do(pentest,' or 1=1 -- ')
>>> r.text
...
large html snippet
...
```

## has_element(formname)
Check if element exists in the current browser window. 

|  |  |
|--|--|
| **formname** (string) | name of the form name |

```
>>> r = Request.get("http://google.com")
>>> r = Request.has_element('q')
True
```
