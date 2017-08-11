
<h2>For system administrator</h2>

<h1 align="">Automate Tests (automate.py)</h1>
  <p align="">
    Use automate.py to run exploit scripts via a JSON file. Make sure your installation is complete before using automate.py.

## Usage
```
./automate.py [testfile]
```

## Example of JSON test file:
A test file has a list targets each with their own list of exploits and parameters. Parameters for exploits can be found using pinkwave.py -e [exploitPath].

```
{
	"tests": [{
			"target": "learnvuln.loc",
			"exploits": [{
					"exploits": "exploits/sword/xsslogger.py",
					"requestNames": "vuln"
				},
				{
					"exploits": "exploits/sword/linuxpathtraversal.py",
					"requestNames": "vuln"
				},
				{
					"exploits": "exploits/sword/commonfiles.py"
				},
				{
					"exploits": "exploits/sword/cookiesecureflag.py"
				},
				{
					"exploits": "exploits/sword/cookiehttponlyflag.py"
				},
				{
					"exploits": "exploits/sword/sslstripping.py"
				}
			]
		},
		{
			"target": "learnvuln.loc?vuln=login.php",
			"exploits": [{
					"exploits": "exploits/sword/bruteforce.py",
					"requestNames": ["user", "pass"]
				},
				{
					"exploits": "exploits/sword/csrflogin.py",
					"requestNames": ["user", "pass"],
					"creds": ["admin", "admin"]
				},
				{
					"exploits": "exploits/sword/sessionregeneration.py",
					"requestNames": ["user", "pass"],
					"creds": ["admin", "admin"]
				},
				{
					"exploits": "exploits/sword/csrftokenscan.py"
				}
			]
		}

	]
}
```

## Getting parameters
View the parameters for each exploit by executing pinkwave.py with the -e parameter with the path to the exploit.

For example:
```
cd ~/PinkWave
./pinkwave.py -e exploits/sword/xsslogger.py

## Will output:
# [exploits/sword/xsslogger.py] > show parameters
#
# Exploit options (exploits/sword/xsslogger.py)
#
# [--target] Remote target host
# [--requestNames] POST/GET names, comma seperated (GET or POST required)
# [--request] Select request (GET or POST)
```

## Running test JSON file
Place your test JSON file in the private directory and specify the path when executing automate.py.

```
cd ~/PinkWave
./automate.py tests/testfile.json
```


## Logging
Logs will be kept separately for each host in the private directory. If your scanning a page from yoursite.com the logs will be kept in private/hosts/yoursite.com. Automate.py will also assign an incremental reportid for each execution.

### Logging Tree
 * private
   * hosts
      * yoursite.com
        * report-1.csv
        * report-2.csv

