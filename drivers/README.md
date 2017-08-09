Installing webdrivers for Selenium
==========

### 1\. Download your webdriver
Download the webdriver of the browser you want to use:

- Firefox: https://github.com/mozilla/geckodriver/releases
- Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads
- PhantomJS: http://phantomjs.org/download.html

### 2\. Copy your webdriver
PinkWave uses the /drivers folder to look for your binary webdrivers. The binary webdriver file need to be placed in a directory with the the following pattern: 
```
/drivers/[architecture]/[browser]/
```

**For example**: The firefox webdriver should have this location on a 64-bit linux machine:
```
/drivers/64/firefox/geckodriver
```

### 3. Configure your webdriver
Browse to the **/config/config.json** file and set _browser_ to **firefox**.

```
{
  "browser" : "firefox",
  "http-port" : 9000,
  "timeout" : 7
}
```

### Testing/Troubleshoot webdriver

Not all webdrivers are supported with all browser versions. For example, the current Firefox webdriver supports up to version 53 while the latest version of Firefox is currently 54.

Test your webdriver:
```
./pinkwave.py -t localhost
# You should see a browser opening and closing and the following message: (-e) exploits are required
```

If your Chrome/Firefox webdrivers are not working with your browser version you should downgraade to an older version. You can also choose to use PhantomJS, which does not depend on a browser.
