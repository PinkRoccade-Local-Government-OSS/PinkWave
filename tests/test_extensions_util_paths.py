import sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from unittest import TestCase
from unittest import main

from extensions.Util import Util


class TestUtilCount(TestCase):

    def test_getAppDir(self):
        appDir = dirname(dirname(abspath(__file__)))
        result = Util.getAppDir()
        self.assertEquals(appDir,result)

    def test_getReportDir(self):
        appDir = dirname(dirname(abspath(__file__))) + "/private/hosts/test.com"
        result = Util.getReportDir("https://test.com")
        self.assertEquals(appDir,result)


    def test_getReportDir2(self):
        appDir = dirname(dirname(abspath(__file__))) + "/private/hosts/testy.com"
        result = Util.getReportDir("testy.com")
        self.assertEquals(appDir,result)

if __name__ == '__main__':
    main()
