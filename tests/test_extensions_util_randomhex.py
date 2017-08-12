import sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from unittest import TestCase
from unittest import main

from extensions.Util import Util


class TestUtilCount(TestCase):

    def test_getRandomHex(self):
        result = Util.getRandomHex(8)
        print result
        self.assertEquals(8,len(result))

    def test_getRandomHex2(self):
        result = Util.getRandomHex(32)
        print result
        self.assertEquals(32,len(result))


if __name__ == '__main__':
    main()
