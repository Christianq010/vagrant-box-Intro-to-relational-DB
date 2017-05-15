# Building a Web Server with HTTPBaseServer

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Handler indicates what code to execute depending on what type of HTTP request it gets
class webserverHandler(BaseHTTPRequestHandler):
    # Handle get requests the web server receives
    def do_GET(self):
        try:
            # if statement looks for the URL with /hello
            if self.path.endswith("/hello"):
                # webserver then sends response code of 200 (successful get request)
                self.send_response(200)
                # Indicate we are replying with text in the form of html to client
                self.send_header('Content-type', 'text/html')
                # Send a blank line to indicate the end of out http header
                self.end_headers()

                # Create empty string (output), add msg to it
                output = ""
                output += "<html><body>Hello, world!</body></html>"
                # send our msg(output) back to the client
                self.wfile.write(output)
                # Add print to see output on our terminal
                print output
                # exit if statement with return
                return

        except IOError:
            # our exception to indicate us of IO errors
            self.send_error(404, "File Not Found %s" % self.path)


# Instantiate our Server and specify what port we wil listen on
def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    # Trigger when user types ctrl+c on keyboard
    except KeyboardInterrupt:
        print " ^C entered, stopping web server... "
        server.socket.close()

# Immediately run main() when python executes Script
if __name__ == '__main__':
    main()
