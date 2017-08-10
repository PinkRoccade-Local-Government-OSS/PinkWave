import sys,os
from os.path import dirname,abspath

# Importing PinkWave extensions
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
import extensions.Request as Request

def start():
    print "Logging in as admin before performing action"
    Request.post("http://learnvuln.loc/?vuln=login.php",["user","pass"],["admin","admin"])
    print "Logged in!"
