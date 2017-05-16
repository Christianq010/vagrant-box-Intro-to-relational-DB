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

            # Look for /edit in our URL
            if self.path.endswith("/edit"):
                # 3rd Value of this array contains our ID Number
                restaurantIDPath = self.path.split("/")[2]
                # Grab the restaurant entry equal to the ID in the URL
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
            # If we find the query generate a response in the page
            if myRestaurantQuery != [] :
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>"
                output += myRestaurantQuery.name
                output += "</h1>"
                # Create a form with one field for restaurant name
                # pass the ID as URL for the edit
                output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
                output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                output += "<input type = 'submit' value = 'Rename'>"
                output += "</form>"
                output += "</body></html>"

                self.wfile.write(output)


            if self.path.endswith("/restaurants"):
                # Our query to list out all restaurants in the DB
                restaurants = session.query(Restaurant).all()
                # Add New Restaurants Page link
                output = ""
                output += "<a href='/restaurants/new'>Make a New Restaurant </a></br></br>"
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
                    output += "<a href='/restaurants/%s/edit'>Edit</a>"
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
            # POST response for our edit form
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    # Perform query to find the object with our matching ID
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    # Reset name to our edit and commit session to DB
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        # Add re-direct to restaurants page after edit
                        self.send_header('Location', '/restaurants')
                        self.end_headers()


            # if statement looking for restaurants/new
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('newRestaurantName')

                # Create new Restaurant Class
                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                # Instead of print we re-direct to /restaurants homepage
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

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
