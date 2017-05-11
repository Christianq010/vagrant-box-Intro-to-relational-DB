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
