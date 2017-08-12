import sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from unittest import TestCase
from unittest import main

from lib.TestParse import TestParse

class TestTestParse(TestCase):

    def test_execute(self):
        testFile = dirname(abspath(__file__)) + "/assets/test.json"
        parser = TestParse(testFile)

        test1 = parser.tests[0]
        self.assertEquals("exploits/sword/portscantcp.py",test1['exploits'])
        self.assertEquals([80,443,22],test1['ports'])

        test2 = parser.tests[1]
        self.assertEquals("exploits/sword/portscanudp.py",test2['exploits'])
        self.assertEquals([53],test2['ports'])

        test3 = parser.tests[2]
        self.assertEquals("exploits/sword/cookiesecureflag.py",test3['exploits'])

        test4 = parser.tests[3]
        self.assertEquals("exploits/sword/cookiehttponlyflag.py",test4['exploits'])

        test5 = parser.tests[4]
        self.assertEquals("exploits/sword/sslstripping.py",test5['exploits'])



if __name__ == '__main__':
    main()
