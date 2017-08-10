
<h2>For managers</h2>

<h1 align="">Configure setting</h1>
You can configure your settings in a JSON file in the config/config.json file.


### Config settings
These values will be used in the application:

|   |   |
|---|---|
| **browser** (string) | Choose '**firefox**','**chrome**' or '**phantomjs**'  |
| **http-port** (int) | Recommended: **9000**, http-port is the port that is used for the XSS logging audit tool and the bouncer tool (detecting XSS and directly submitting POST requests).
 **timeout** (int) | Recommended: **7**, timeout time for browser, used for logging timeouts.
| **debug** (boolean) | Recommended: **false**, displays extra debug information when executing scripts, such as GET/POST request logs.
| **ssl-verify** (boolean) | Recommended: **true**, force to verify SSL certificates before connecting to https targets. **false** can be usefull if you're testing a self signed application, but ***keep in mind that someone could manipulate the response if you accept all certificates***.

