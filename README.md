PinkWave
==========
PinkWave is a pentesting tool for linux which can be used to test (web)servers
with Python scripts. 


## Features
### Automated pentests using Python + Browsers
Using the Seleniun Webdriver, PinkWave can use browsers
like Firefox, Chrome or PhantomJS to perform automated pentests. 

### Use your favorite Python libraries
Python scripts, called exploits, can control the browser with an easy to use [API](docs/devleopers/extensions/Request.py) to perform actions and report vulnerabilities. You're also free to use any other Python libraries.


### Define user flows 
PinkWave acts as a legitimate browser user and can optionally execute a user flow before performing each **exploit** using other python scripts called **macros**, for example you can use a **macro** to login before performing an **exploit**.


### Logging
All events will be logged in the private/ directory separately for each **target**.




## Installing
Clone this repository to your home directory and follow the following steps:

### 1\. Install dependencies
```
# Install python dependencies
cd PinkWave
pip install -r requirements.tx

# (optional) Install cipherscan if you want to use /exploits/sword/cipherscan.py
cd pw_modules
git clone https://github.com/mozilla/cipherscan/
```

### 2\. Install webdriver
Read more in [drivers/README.md](https://github.com/PinkRoccadeLG/pinkwave/tree/master/drivers)

### 3\. Allow NMAP as sudo for current user
```
# Open sudoers file to allow sudo nmap
sudo visudo

# Append this line and replace [YOURUSERNAME] with your username
[YOURUSERNAME] ALL = NOPASSWD: /usr/bin/nmap
```

## Usage

#### 1\. Execute manual test
Use pinkwave.py to execute a single test. Use the exploit interface to view parameters for individuel scripts.  
```
./pinkwave.py -t [target] -e [exploit] [params]
```

#### 2\. Execute tests via JSON
Use [automate.py](docs/administrators/automate-tests.markdown) to execute multiple tests with a [JSON file](docs/administrators/automate-tests.markdown).
```/
./automate.py [pathToTestfile]
```

#### 3\. Status interface (s)
View status of the PinkWave tool and test the http-port for XSS audits and POST form generators: 
```
./pinkwave.py --status
[*] PinkServer (HTTP server) starting on port: 9000


             oo          dP                                             
                         88                                             
    88d888b. dP 88d888b. 88  .dP  dP  dP  dP .d8888b. dP   .dP .d8888b. 
    88'  `88 88 88'  `88 88888"   88  88  88 88'  `88 88   d8' 88ooood8 
    88.  .88 88 88    88 88  `8b. 88.88b.88' 88.  .88 88 .88'  88.  ... 
    88Y888P' dP dP    dP dP   `YP 8888P Y8P  `88888P8 8888P'   `88888P' 
    88                                                                  
    dP                                                                  

              -- -- +=[ 322 Payloads 
              -- -- +=[ 17 Python Scripts 
            [W] Make sure your current directory (pwd) is the same as pinkwave.py .
            
[^] Logger is up. http://localhost:9000/logger
[^] Bouncer is up. http://localhost:9000/bouncer
```

#### 4\.  Exploit interface (-e)
Use the -e parameter with a path to an exploit to display the parameters.

```
./pinkwave.py -e exploits/sword/sslstripping.py

[exploits/sword/sqlinjection.py] > show parameters

Exploit options (exploits/sword/sqlinjection.py)

[--target] (Required) Remote target host
[--requestNames] POST/GET names, comma seperated
[--request] (optional) Specify request type (GET,POST or POST/DIRECT)
```

#### 5\. Macro interface (-m)
```
/pinkwave.py -m tests/example-macros/logmein.py,tests/example-macros/searchforuser.py
[*] PinkServer (HTTP server) starting on port: 9000
Logging in as admin before performing action
Logged in!
Searching for user Iron Man(1)...


<tr>
<td>1</td>
<td>Iron</td>
<td>Man</td>
</tr>

```



## Examples of manual testing
**Testing for SSL stripping**:
```
./pinkwave.py -t localhost -e exploits/sword/sslstripping.py
# [!] Exploit detected! (exploits/sword/sslstripping.py)
# [!] No HSTS header to prevent sslstripping
```

**Testing expected open TCP ports**:
```
./pinkwave.py -t localhost -e exploits/sword/portscantcp.py --ports=80,443
# [!] Exploit detected! (exploits/sword/portscantcp.py)
# [!] Unexpected open/closed ports: 9000, 443, 53

```



## Documentation
Read [docs/](https://github.com/PinkRoccadeLG/pinkwave/tree/master/docs) for documentation.

## Contributing
You can fork this repository and add your own **exploit** directory, which we can add to this repository. Include the \_\_author\_\_ headers in your python scripts.



## Credits, copyright and license

PinkWave is developed for PinkRoccade Local Government and developed by [Maarten Schermer](https://github.com/maartensch) during his security internship in 2016.

Code and documentation copyright 2017 PinkRoccade Local Government. Code released under the [Apache 2 License](https://github.com/PinkRoccadeLG/pinkwave/blob/master/LICENSE). Docs released under [Creative Commons](https://github.com/PinkRoccadeLG/pinkwave/blob/master/docs/LICENSE).
