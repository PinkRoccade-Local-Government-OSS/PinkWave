### For developers/administrators

<h1 align="">Writing your first macro</h1>

 **Macros** are python scripts that can be used to perform an action before executing an **exploit**. A macro must contain a ***start*** function.

## Example macro to login:

```
import sys,os
from os.path import dirname,abspath

# Importing PinkWave extensions
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
import extensions.Request as Request

def start():
    print "Logging in as admin before performing action"
    Request.post("http://learnvuln.loc/?vuln=login.php",["user","pass"],["admin","admin"])
    print "Logged in!"
```


## Execute macro
You can use macros with the -m or -macros parameter in pinkwave.py and you can use them in your testfile.

#### Using pinkwave.py:
```
python pinkwave.py -m private/macros/logmein.py
```

## Execute macro before test:
By using the 'macros' parameter, you can specify, comma seperated, the paths to the macro's you want to execute. Macro's will execute in order and wait for completion of the previous macro.
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

