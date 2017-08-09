### For developers/administrators

<h1 align="">Writing your first macro</h1>

 **Macro's** are python scripts that can be used to perform an action before executing an **exploit**. A macro must contain a ***start*** function with a ***browser*** parameter.

For example:
```
def start(browser):
    print "Logging in as admin before performing action"
    browser.nav("http://learnvuln.loc/?vuln=login.php")
    browser.post(["user","pass"],["admin","admin"])
    print "Logged in!"
```

You can use macros with the -m or -macros parameter in pinkwave.py and you can use them in your testfile.

Example with pinkwave.py:
```
python pinkwave.py -m private/macros/logmein.py
```

Example with a testfile:
```
{
    "tests" : [
        "target" : "http://learnvuln.loc",
        "exploits" : [
            {
                "exploits" : "exploits/sword/commonfiles.py",
                "macros" : "private/macros/logmein.py"
            }
        ]
    ]
}
```

