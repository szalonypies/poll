#!/usr/bin/env python
"""
Very simple HTTP server in python.

Usage::
    ./dummy-web-server.py [<port>]

Send a GET request::
    curl http://localhost

Send a HEAD request::
    curl -I http://localhost

Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost

"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import cgi
import os.path
import datetime

questions = [
"Q1",
"Q2",
"Q3",
"Q4",
"Q5",
"Q6"]

answers = [
    [-1, "I will not go, even if it wins"], 
    [0, "I might go but not really interested"], 
    [1, "I would go"], 
    [2, "I would love to go"]
]

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>Poll!</h1>\n")
        self.wfile.write("<script>\n")
        self.wfile.write('\n'.join(open('script.js').readlines()))
        self.wfile.write("</script>\n")
        self.wfile.write("<form method='POST' onsubmit='return checkform(this);'>\n")
        self.wfile.write("<p>Name: <input type='text' name='name'/></p>\n")
	i = 1
        for q in questions:
            self.wfile.write("<p>%s<br/><select name='q%s'>" % (q, str(i)))
	    self.wfile.write("<option value='notselected'>--------</option>")
            i += 1
	    for aval, astr in answers:
	        self.wfile.write("<option value='%s'>%s</option>" % (str(aval), astr))
	    self.wfile.write("</select></p>\n")
        self.wfile.write("<input type='submit' value='send' />\n")
        self.wfile.write("</form>\n")
        self.wfile.write("</body></html>\n")

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        if not os.path.isfile('results.csv'):
	    f = open('results.csv', 'w+')
	    f.write('IP,Name,Date,')
	    for q in questions:
	        f.write(q+',')
            f.write('\n')
	    f.close()
        f = open('results.csv', 'a+')
        f.write(self.client_address[0])
	f.write(',')
        f.write(form.list[0].value)
        f.write(',')
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        f.write(',')
        for item in form.list[1:]:
            f.write(item.value)
	    f.write(',')
	f.write('\n')
	f.close()
        self._set_headers()
        self.wfile.write("<html><body><h1>Thanks</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

