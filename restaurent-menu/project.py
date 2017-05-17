# Creating and Testing out our first Flask application

from flask import Flask
# import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create an instance of this class with __name__ as the running argument
app = Flask(__name__)

# create Session and connect to DB
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# python decorator - when browser uses URL, the function specific to that URL gets executed
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    # Add all restaurants and menu items to page
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'
    return output

# if executed via python interpreter run this function
if __name__ == '__main__':
    # reload server when code change detected and run debug in browser
    app.debug = True
    # use to run local server with our application
    # special config for vagrant machine by making our host publicly available
    app.run(host='0.0.0.0', port=5000)
