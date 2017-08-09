import sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from unittest import TestCase
from unittest import main

from extensions.Util import payloads

class TestUtilPayloads(TestCase):

    def test_getPayloads(self):
        currentDir = dirname(abspath(__file__))
        currentFile = abspath(currentDir + "/assets/tester.dat")
        result = payloads("tester",currentFile)
        expected = ["test1","test2","test3"]
        self.assertEquals(expected,result)

if __name__ == '__main__':
    main()
