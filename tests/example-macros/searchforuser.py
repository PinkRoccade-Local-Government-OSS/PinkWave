import sys,os
from os.path import dirname,abspath

# Importing PinkWave extensions
sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
import extensions.Request as Request

def start():
    print "Searching for user Iron Man(1)..."
    r1 = Request.post("http://learnvuln.loc/?vuln=sql.php",["id"],["1"])
    text = r1.text
    table = text.split("<tbody>")[1].split("</tbody>")[0].replace(" ","")
    print table
