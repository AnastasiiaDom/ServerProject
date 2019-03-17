# 4.1 Send a GET request to create new user or login:
#     curl http://localhost:8080/23455/login

# 4.2 Send a POST request to add new score of certain user to certain level:
#     curl -d '{"score" : 1050}' http://localhost:8080/2/score?sessionkey=username

# 4.3 Send a GET request to get a highscore for a level:
# curl http://localhost:8080/3/highscorelist

import json
from urls import Urls

from http.server import BaseHTTPRequestHandler,HTTPServer

PORT = 8080

class MyServer(BaseHTTPRequestHandler):
    urls = Urls()

    def do_GET(self):
        view = self.urls.matchView(self.path)

        if view:
            result = view.get()

            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            self.wfile.write((result).encode())
        else:
            self.send_error(400)

    def do_POST(self):
        view = self.urls.matchView(self.path)

        if view:
            content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
            data = json.loads(self.rfile.read(content_length)) # <--- Gets the data itself
            username = view.post(data)
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
        else:
            self.send_error(400)

# Start server on port 8080
def run():
    print('starting server...',  flush=True)
    httpd = HTTPServer(("localhost", PORT), MyServer)
    print("serving at port", PORT,  flush=True)
    httpd.serve_forever()

run()
