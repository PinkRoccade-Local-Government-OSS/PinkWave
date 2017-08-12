import sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from unittest import TestCase
from unittest import main

from extensions.Util import Util

assetFolder = dirname(abspath(__file__)) + "/assets/utils"

class TestUtilCount(TestCase):

    def test_countUtil(self):
        result = Util.countExtensions(folder=assetFolder,ext="xls")
        self.assertEquals(2,result)


    def test_countUtil2(self):
        result = Util.countExtensions(folder=assetFolder,ext="docx")
        self.assertEquals(3,result)

    def test_countUtil3(self):
        result = Util.countExtensions(folder=assetFolder,ext="txt")
        self.assertEquals(1,result)

    def test_countUtilEmpty(self):
        result = Util.countExtensions(folder=assetFolder + "/0files",ext="xls")
        self.assertEquals(0,result)

if __name__ == '__main__':
    main()
