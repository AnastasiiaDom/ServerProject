# Send a GET request::
#     curl http://localhost
# Send a HEAD request::
#     curl -I http://localhost
# Send a POST request::
#     curl -d "foo=bar&bin=baz" http://localhost

import uuid
import re
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler,HTTPServer

PORT = 8080
testurl= 'https://github.com/tomas-mm/demo_python_server/blob/master/urls.py'

class LoginView(object):
    users = {}

    def __init__(self, userId, params):
        self.userId = userId
        self.params = params

    def get(self):
        if  self.userId not in self.users:
            self.users[self.userId] = str(uuid.uuid4())
        else:
            print('This user is on DB, go away stupid squirl', flush=True)

        return self.users[self.userId]

class ScoreView(object):

    def __init__(self, userId, params):
        self.userId = userId
        self.params = params

class HighscorelView(object):

    def __init__(self, userId, params):
        self.userId = userId
        self.params = params

class Urls(object):

    def __init__(self):
        urls = [
            ('^/(?P<userId>\d+)/login/?$', LoginView),
            ('^/(?P<levelid>\d+)/score/?$', ScoreView),
            ('^/(?P<levelid>\d+)/highscorelist/?$', HighscorelView)
        ]
        self.urls = [(re.compile(url), klass) for url, klass in urls]

    def matchView(self, url):
        parsed = urlparse(url)

        for regex, klass in self.urls:
            res = regex.match(parsed.path)
            if res:
                kwargs = res.groupdict()
                kwargs['params'] = parse_qs(parsed.query)

                return klass(**kwargs)

        return None

class MyServer(BaseHTTPRequestHandler):
    urls = Urls()

    def do_GET(self):
        view = self.urls.matchView(self.path)
        try:
            if view:
                username = view.get()
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                self.wfile.write(("username : " + username).encode())
            else:
                self.send_error(400)

        except Exception as e:
            print(e, flush=True)
            self.send_response(400)

    def do_POST(self):
        print( "incomming http: ", self.path, flush=True)
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print( "post_data: ", post_data, flush=True)
        self.send_response(200)
        client.close()
        #import pdb; pdb.set_trace()

# Start server on port 8080
def run():
    print('starting server...',  flush=True)
    httpd = HTTPServer(("localhost", PORT), MyServer)
    print("serving at port", PORT,  flush=True)
    httpd.serve_forever()

run()
