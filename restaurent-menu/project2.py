# Create a Log in System for our Project.py - Restaurant Menu App

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# import CRUD Operations from Lesson 1
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup2 import Base, Restaurant, MenuItem, User
# New imports for Google Log in
from flask import session as login_session
import random, string
# Imports for GConnect
# store OAuth2 parameters
from oauth2client.client import flow_from_clientsecrets
# Catch error in case we run into error during OAuth
from oauth2client.client import FlowExchangeError
# comprehenive python http2 client library
import httplib2
# convert in memory python objects to JSON
import json
# converts our returned function to a real response method sent to our client
from flask import make_response
# apache library written in python
import requests

# Create an instance of this class with __name__ as the running argument
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = 'Restaurant Menu Application'

# create Session and connect to DB
engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create a state token to prevent request
# Store it in the session for later validation
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)for x in xrange(32))
    login_session['state'] = state
    # Show our validation in a string - return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# Server side code accepting token
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token (client sent to server matches server sent to client)
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    response = h.request(url, 'GET')[1]
    str_response = response.decode('utf-8')
    result = json.loads(str_response)

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        login_session['credentials'] = credentials
        response = make_response(json.dumps('Current user is already connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # When you log in via Gmail, create new user_id if does not exist in DB
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Use login_session to create a New User when signed in
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Pass a user.id into this method return a User object with the associated id number from the DB
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Take am email address and return a user.id if the email exists
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['credentials']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['credentials']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Show Restaurant menu Page in JSON
@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    # Return jsonify class and use loop to serialize all our DB entries
    return jsonify(MenuItems=[i.serialize for i in items])


# Show individual menuItems in the URL in JSON
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


# Show all restaurants in JSON
@app.route('/restaurant/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


# app.route('/') - is python decorator - when browser uses URL, the function specific to that URL gets executed

# Show all Restaurants
@app.route('/')
@app.route('/restaurant/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    users = session.query(User).all()
    if 'username' not in login_session:
        return render_template('publicrestaurants.html',restaurants=restaurants, users=users )
    return render_template('restaurants.html', restaurants=restaurants)


# Create new Restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    # If user not logged in return to log in page
    if 'username' not in login_session:
        flash("Please Log In or Sign Up to Add Restaurant")
        return redirect('/login')
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


# Edit an existing Restaurant
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    # If user not logged in return to log in page
    if 'username' not in login_session:
        flash("Please Log In or Sign Up to Edit Restaurant")
        return redirect('/login')
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            return redirect(url_for('showRestaurants'))
    else:
            return render_template('editRestaurant.html', restaurant=editedRestaurant)


# Delete an existing Restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # If user not logged in return to log in page
    if 'username' not in login_session and restaurantToDelete.user_id != login_session:
        flash("Please Log In or Sign Up to Delete Restaurant")
        return redirect('/login')
    if request.method == 'POST':
        session.delete(restaurantToDelete)
        session.commit()
        return redirect(url_for('showRestaurants', restaurant_id=restaurant_id))
    else:
        return render_template('deleteRestaurant.html', restaurant=restaurantToDelete)


# Show a Restaurant Menu
@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    # Add all restaurants and menu items to page
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # Edit by user_id has a bug
    # creator = getUserInfo(restaurant.user_id)
    creator = session.query(User).all()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    # Show Public Page if User not logged in
    #     if 'username' not in login_session or creator.id != login_session['user_id']:
    if 'username' not in login_session:
        return render_template('publicmenu.html', items=items, restaurant=restaurant, creator=creator)
    else:
        return render_template('menu.html', restaurant=restaurant, items=items, creator=creator)


# Add a new Menu Item
@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    # If user not logged in return to log in page
    if 'username' not in login_session:
        flash("Please Log In or Sign Up to Add Menu Item")
        return redirect('/login')
    # Look for POST request
    if request.method == 'POST':
        # extract 'name' from our form using request.form
        newItem = MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        # Our flask message
        flash("New menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    # If a POST request was not received
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Edit an existing Menu Item
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    # If user not logged in return to log in page
    if 'username' not in login_session:
        flash("Please Log In or Sign Up to Edit Menu Item")
        return redirect('/login')
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


# Delete an existing Menu Item
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    # If user not logged in return to log in page
    if 'username' not in login_session:
        flash("Please Log In or Sign Up to Delete Menu Item")
        return redirect('/login')
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=itemToDelete)


# if executed via python interpreter run this function
if __name__ == '__main__':
    # Secret key for flask message flashing (sessions)
    app.secret_key = 'super_secret_key'
    # reload server when code change detected and run debug in browser
    app.debug = True
    # use to run local server with our application
    # special config for vagrant machine by making our host publicly available
    app.run(host='0.0.0.0', port=5000)

