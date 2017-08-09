import os,urlparse,sys
from os.path import abspath,dirname
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading
import hashlib

# Import PinkWave extensions
appDir = dirname(dirname(abspath(__file__ )))
sys.path.append(appDir)
from extensions.Util import Util

class MyHandler(BaseHTTPRequestHandler):

    def log_request(self, code=None, size=None):
        # Silence is golden
        pass

    def do_GET(self):

        # Set headers
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Handle params
        path = self.path
        params = {}
        paths = path.split('?', 1)
        page = paths[0].strip("/")
        query = None
        if len(paths) > 1:
            tmp = paths[1]
            qs = urlparse.parse_qs(tmp)
            if len(qs) != 0:
                for key in qs.iterkeys():
                    params[key] = qs[key]

        # Handle pages
        content = "PinkServer"
        currentDir = dirname(abspath(__file__))
        if page == "logger":
            token = params.get("token")
            if token is not None:
                token = token[0]
                with open(currentDir + "/logger.hbs","r") as f:
                    content = "".join(f.readlines())
                with open(dirname(currentDir) + "/private/secret","r") as f:
                    secret = "".join(f.readlines()).strip()

                hash = hashlib.sha256("%s%s" % (secret,token)).hexdigest()
                content = content.replace("{{hash}}",hash)
        elif page == "bouncer":
            url = params.get("url")
            values = params.get("values")
            if url is not None and values is not None:
                with open(currentDir + "/bouncer.hbs","r") as f:
                    content = "".join(f.readlines())

                url = url[0]
                values = values[0].split(",")
                content = content.replace("{{url}}",url)
                inputs = ""
                for value in values:
                    inputs += "<input type=\"text\" name=\"%s\" />" % value

                content = content.replace("{{inputs}}",inputs)
        if content == "PinkServer":
            with open(currentDir + "/default.hbs","r") as f:
                content = "".join(f.readlines())

        self.wfile.write(content)
        return

server = None
def start(port):
    t = threading.Thread(target=startForever, args = (port,))
    t.daemon = True
    t.start()

def startForever(port):
    try:
        global server
        server = HTTPServer(('localhost', port), MyHandler)
        print('[*] PinkServer (HTTP server) starting on port: %s' % str(port))
        server.serve_forever()
    except Exception as e:
        if "Address already in use" in e:
            print "Address already in use (port %s)" % str(port)
def stop():
    global server
    server.socket.close()

if __name__ == "__main__":
    start(Util.getConfig("http-port"))
    while 1==1:pass
