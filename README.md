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
# Install system dependencies
sudo apt-get install python nmap

# Install python dependencies
cd pinkwave
pip install -r requirements.txt
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

Use pinkwave.py to show options for exploits or execute a single test.
```
./pinkwave.py --help 
```

Use [automate.py](https://github.com/PinkRoccadeLG/pinkwave/blob/master/docs/administrators/automate-tests.markdown) to execute multiple tests with a [JSON file](https://github.com/PinkRoccadeLG/pinkwave/blob/master/docs/administrators/automate-tests.markdown).
```
./automate.py [pathToTestfile]
```

## Examples
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
