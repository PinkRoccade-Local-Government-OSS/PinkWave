import sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from unittest import TestCase
from unittest import main

from extensions.Util import Util

class TestUtilConfig(TestCase):

    def test_getConfigbrowser(self):
        result = Util.getConfig("browser")
        expected = "phantomjs"
        self.assertEquals(expected,result)

    def test_getConfighttpport(self):
        result = Util.getConfig("http-port")
        expected = 9000
        self.assertEquals(expected,result)

    def test_getConfigtimeout(self):
        result = Util.getConfig("timeout")
        expected = 7
        self.assertEquals(expected,result)

    def test_getBouncer(self):
        result = Util.getBouncer()
        expected = "http://localhost:9000/bouncer"
        self.assertEquals(expected,result)

    def test_getLogger(self):
        result = Util.getLogger()
        expected = "http://localhost:9000/logger"
        self.assertEquals(expected,result)


if __name__ == '__main__':
    main()
