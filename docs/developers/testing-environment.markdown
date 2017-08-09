<h3>For developers</h3>

<h1 align="">Testing Environment</h1>
  <p align="">
    When testing exploits you are in need of a vulnerable environment. For all the exploits/scripts in the /exploits/sword directory I have used my own vulnerable environment 'LearnVulnerable'. If you would like to use it too you can follow this tutorial.

### Other examples of vulnerable environments
- **VulnHub**: https://www.vulnhub.com
- **DVWA**: http://www.dvwa.co.uk/
- **XVWA**: https://github.com/s4n7h0/xvwa
- **WebGoat**: https://github.com/WebGoat/WebGoat/


Installing LearnVulnerable
==============

## 1\. Install LAMP stack
The LAMP stack is required to run the LearnVulnerable application, because it's build with PHP and uses a MySQL database.





```
sudo apt-get update
sudo apt-get install apache2 mysql-server php libapache2-mod-php php-mysql
mysql_secure_installation
```

2\. Install LearnVulnerable
=============

```
git clone https://github.com/maartensch/learn-vulnerable
```

- Edit config.php file to set your database username,password,host,name
- (optional) Create a virtual host for learn vulnerable
- (optional) Modify your /etc/hosts file if you want to use a alias to point to your installation

## Example config files

/etc/hosts
```
127.0.0.1   learnvuln.loc

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
/etc/apache2/sites-available/learnvuln.loc.conf 
```
<VirtualHost *:80>
    ServerName learnvuln.loc
    ServerAlias learnvuln.loc
    ServerAdmin webmaster@localhost
    DocumentRoot /home/sword/apache/learnvuln.loc/
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### Don't forget to enable the virtual host!
```
# add virtual host 
cd /etc/apache2/sites-available
a2ensite learnvuln.loc.conf
sudo service apache2 reload
```

3\. Testing your first exploit
=======================
Now you can use pinkwave.py to specify the http://learnvuln.loc target. Always check the options of an exploit by executing it via the pinkwave.py interface like:
```
cd [pinkwavedir]
./pinkwave.py -e exploits/sword/sqlinjection.py
# Will output:
[exploits/sword/sqlinjection.py] > show parameters

Exploit options (exploits/sword/sqlinjection.py)

[--target] Remote target host
[--requestNames] POST/GET names, comma seperated (GET or POST required)
[--request] Select request (GET or POST)
```

**Target** :
You can specify a target here, we choose: **http://learnvuln.loc/?vuln=sql.php**
 
**RequestNames**: Specify here the input name(comma seperated), for this parameter we choose: **id**

**Request**: Specify the request type here, because it's a form with a POST action we select **POST**.


### The final command:
```
./pinkwave.py -e exploits/sword/sqlinjection.py -t http://learnvuln.loc/?vuln=sql.php -rn id -r POST
```
This should have a similar output as the following screenshot:

![Image of test](../images/local-test-output.png)

