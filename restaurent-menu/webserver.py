# Building a Web Server with HTTPBaseServer

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create Session and connect to DB
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Handler indicates what code to execute depending on what type of HTTP request it gets
class webserverHandler(BaseHTTPRequestHandler):
    # Handle GET requests the web server receives
    def do_GET(self):
        try:
            # Our Add New Restaurants Page
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return


            if self.path.endswith("/restaurants"):
                # Our query to list out all restaurants in the DB
                restaurants = session.query(Restaurant).all()
                # Add New Restaurants Page link
                output = ""
                output += "<a href='/restaurants/new'>Make a New Restaurant </a><br><br>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                # Add a for-loop to list out all restaurants
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "<br>"
                    # Add our edit and delete functionality
                    output += "<a href='#'>Edit</a>"
                    output += "<br>"
                    output += "<a href='#'>Delete</a>"
                    output += "<br>"
                output += "<html><body>"
                self.wfile.write(output)
                return


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
                output = "<html><body>"
                output += "<h2>Hello, world!</h2>"
                # Add form
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                # send our msg(output) back to the client
                self.wfile.write(output)
                # Add print to see output on our terminal
                print output
                # exit if statement with return
                return

            # Add another page(/hola) to our web server for testing
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                # add a tag to redirect to /hello page
                output += "<html><body>&#161Hola, hombre! <a href ='/hello'> back to Hello </a>'</body></html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            # our exception to indicate us of IO errors
            self.send_error(404, "File Not Found %s" % self.path)

    # Handle POST requests the web server receives
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # To read the message sent from the server we use the cgi python library
            # cgi.parse_header to 'content-type'
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

            # Check if this is form data being received
            if ctype == 'multipart/form-data':
                # fields will collect all our fields on a form using cgi.parse_multipart
                fields = cgi.parse_multipart(self.rfile,pdict)
                # get the value of a specific field and store it into an array
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            # return the first value of the array created when the form is submitted
            output += "<h1> %s </h1>" % messagecontent[0]
            # Our form with input name = message
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print
            output

        except:
            pass

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
