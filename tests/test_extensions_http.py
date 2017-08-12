#!/usr/bin/python
import sys
from os.path import dirname,abspath
sys.path.append(dirname(dirname(abspath(__file__))))
import extensions.Http as Http

from unittest import TestCase
from unittest import main

class testExtensionHttp(TestCase):

    def test_get(self):
        h = Http.get("https://httpbin.org/get")
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_post(self):
        h = Http.post("https://httpbin.org/post")
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_put(self):
        h = Http.put("https://httpbin.org/put")
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_delete(self):
        h = Http.delete("https://httpbin.org/delete")
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_get_with_auth(self):
        h = Http.get("https://httpbin.org/get",auth=('admin','admin'))
        self.assertTrue('"Authorization": "Basic YWRtaW46YWRtaW4="' in h.text)
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_post_with_auth(self):
        h = Http.post("https://httpbin.org/post",auth=('admin','admin'))
        self.assertTrue('"Authorization": "Basic YWRtaW46YWRtaW4="' in h.text)
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_put_with_auth(self):
        h = Http.put("https://httpbin.org/put",auth=('admin','admin'))
        self.assertTrue('"Authorization": "Basic YWRtaW46YWRtaW4="' in h.text)
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_delete_with_auth(self):
        h = Http.delete("https://httpbin.org/delete",auth=('admin','admin'))
        self.assertTrue('"Authorization": "Basic YWRtaW46YWRtaW4="' in h.text)
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_post_with_data(self):
        h = Http.post("https://httpbin.org/post",data={"hello":"world","is":"awesome"})
        self.assertTrue('"hello": "world"' in h.text)
        self.assertTrue('"is": "awesome"' in h.text)
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_put_with_data(self):
        h = Http.put("https://httpbin.org/put",data={"hello":"world","is":"awesome"})
        self.assertTrue('"hello": "world"' in h.text)
        self.assertTrue('"is": "awesome"' in h.text)
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

    def test_delete_with_data(self):
        h = Http.delete("https://httpbin.org/delete",data={"hello":"world","is":"awesome"})
        self.assertTrue('"hello": "world"' in h.text)
        self.assertTrue('"is": "awesome"' in h.text)
        self.assertTrue(0 < len(h.text))
        self.assertEquals(200,h.status_code)

if __name__ == '__main__':
    main()
