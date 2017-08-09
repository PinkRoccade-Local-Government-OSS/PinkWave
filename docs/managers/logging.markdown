
<h2>For managers</h2>

<h1 align="">Logging</h1>

Logs will be kept separately for each host in the private directory. If your scanning a page from yoursite.com the logs will be kept in private/hosts/yoursite.com. Automate.py will also assign an incremental reportid for each execution.

### Logging Tree (Example)
 * private
   * hosts
      * yoursite.com
        * report-1.csv
        * report-2.csv
      * othersite.com
        * report-0.csv

### Filename format
- The file format for a log file is "report-{id}.csv". A report id is automaticly generated when testing with automate.py and start at 1. 
- A report-0.csv is created when using the CLI interface manually.

### CSV logging format
Each test will be logged in one line containing the following data fields:

|   |   |
|---|---|
| **Date**  | Finishing time of test in Y-m-d H:i:s format   |
| **Flagged** | Yes/No, Yes when report(msg) is executed
 **Labels** (optional) | Label(s) for the test, comma seperated, for example: 'Cross site scriping (XSS),Javascript'.
| **Script** | Executed exploit script path
| **Target** | Target URL
| **Request Type** | Last request type initiated by the browser (**GET**,**POST**, or **POST/DIRECT**)
| **Parameters** | Shell/JSON parameters for the test, excluding target and exploits. 
| **Comment** | Contains either '**OK**', when not flagged  or the **reason** why this log is flagged.
| **Time** | Duration of test in seconds
| **Length** | Size of response in bytes
| **Cookies** | Cookies for this session

