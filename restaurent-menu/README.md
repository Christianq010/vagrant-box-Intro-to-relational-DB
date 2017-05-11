# Performing CRUD Operations in Full Stack Foundations

## How to install SQLAlchemy (Python ORM)
* Download and extract (http://www.sqlalchemy.org/download.html).
* Open Gitbash from the extracted download and run `python setup.py install`

```
C:\> C:\Python27\python.exe .\setup.py install
running install
running build
running build_py
   ......
Plain-Python build succeeded.
*********************************

```

### 1.CRUD create ( Add data to a Database)
* Log into the Vagrant and `cd` into the `/vagrant` folder
* Run a python shell (`python`) and import the following statements -

```
ubuntu@ubuntu-xenial:/vagrant$ cd /vagrant/restaurent-menu
ubuntu@ubuntu-xenial:/vagrant/restaurent-menu$ python
Python 2.7.12 (default, Nov 19 2016, 06:48:10)
[GCC 5.4.0 20160609] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> from sqlalchemy import create_engine
>>> from sqlalchemy.orm import sessionmaker
>>> from database_setup import Base,Restaurant,MenuItem
```

* Remain in the python shell and create the functions below to configure our communication with the database
* We create an engine configured to our code execution
```
>>> engine = create_engine ('sqlite:///restaurantmenu.db')
>>> Base.metadata.bind = engine
>>> DBSession = sessionmaker(bind = engine)
```
* We create a session, the purpose of this ensures no changes are made to the database until the data added has been staged and committed from the session.
```
>>> session = DBSession()
```
* Our first entry into the database (Restaurant)
```
>>> myFirstRestaurant = Restaurant(name = "Pizza Place")
>>> session.add(myFirstRestaurant)
>>> session.commit()
```
* We can use session to return all restaurants we created in a list
```
>>> session.query(Restaurant).all()
[<database_setup.Restaurant object at 0xb6ab2fcc>]
```
* Our second entry is a MenuItem
```
>>> cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with cheese", course = "Entree", price = "$6.00", restaurant = myFirstRestaurant)
>>> session.add(cheesepizza)
>>> session.commit()
>>> session.query(MenuItem).all()
[<database_setup.MenuItem object at 0xb696bcec>]
>>>
```

### 2.CRUD Read (Reading our data in the database)
* We can save our session query into a variable and reference it
```
>>> firstResult = session.query(Restaurant).first()
>>> firstResult.name
u'Pizza Place'
>>>
```
* Execute the `lotsofmenus.py` file by running it in vagrant via `python lotsofmenus.py`
* Return all added entries by running the following -
```
>>> session.query(Restaurant).all()
```
* Return results with column info for each item as well ( using Python Loop)
```
>>> items = session.query(MenuItems).all()
>>> for item in items:
        print item.name

```
* Look up the query documentation for SQLAlchemy here - http://docs.sqlalchemy.org/en/rel_0_9/orm/query.html

### 3.CRUD Update (Update existing data in our database to new values)
* Create a variable to return the value we would like to update
```
>>> veggieburgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')
```
* Create a for-loop to return each veggie burger
```
>>> for veggieBurger in veggieBurgers:
        print veggieBurger.id
        print veggieBurger.price
        prine veggieBurger.restaurant.name
        print "\n"
```
* Select a specific Result from our results (.one chooses that item instead of a list)
```
>>> UrbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()
```
* Check if we selected the right item
` >>> print UrbanVeggieBurger.price`
* Change the price of our selected item
```
>>> UrbanVeggieBurger.price = '$2.99'
>>> session.add(urbanVeggieBurger)
>>> session.commit()
```
* Run the for-loop above to check each Veggie burger and if our update has been made.
* Use a for-loop to change price on all veggie Burgers burgers in our database.
```
>>> for veggieBurger in veggieBurgers:
        if veggieBurger.price != '$2.99':
            veggieBurger.price = '$2.99'
            session.add(veggieBurger)
            session.commit()
```
* Run a for-loop to return all veggie burgers and check their price.
* Check documentation for more info - http://docs.sqlalchemy.org/en/rel_0_9/orm/query.html

### 4.CRUD Delete (Delete a selected entry in our database)
* Create a variable to return the value to delete
`>>> spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()`
* Check if we selected the correct variable
`>>> print spinach.restaurant.name`
* Delete the selected entry
```
>>> session.delete(spinach)
>>> session.commit()
```
* Search for value to check if it still exists
`>>> spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()`