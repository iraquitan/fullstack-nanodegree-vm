# -*- coding: utf-8 -*-
"""
 * Project: puppy-shelter
 * Author name: Iraquitan Cordeiro Filho
 * Author login: iraquitan
 * File: webserver
 * Date: 2/4/16
 * Time: 12:04 AM
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='/" \
                          "hello'><h2>What would you like me to say?</h2><input name='message'" \
                          " type='text'><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "&#161Hola! <a href = '/hello'>Back to Hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/" \
                          "hello'><h2>What would you like me to say?</h2><input name='message'" \
                          " type='text'><input type='submit' value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
        except IOError:
            self.send_error(404, "File Not Found {}".format(self.path))

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader(
                'content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += "<h2> Ok, how about this: </h2>"
            output += "<h1> {} </h1>".format(messagecontent[0])
            output += "<form method='POST' enctype='multipart/form-data' action='/" \
                      "hello'><h2>What would you like me to say?</h2><input name='message'" \
                      " type='text'><input type='submit' value='Submit'> </form>"
            output += "</body></html>"
            self.wfile.write(output)
            print(output)
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web server running on port {}".format(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping the server...")
        server.socket.close()


if __name__ == "__main__":
    main()
