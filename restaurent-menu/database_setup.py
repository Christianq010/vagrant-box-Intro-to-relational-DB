# Creating a Database with SQLAlchemy ( our ORM for python - database mapping)
# Step 1 - Configuration
# Step 2 - Class

import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class Restaurent(Base):
    __tablename__ = 'restaurent'

class MenuItem(Base):
    __table__ = 'menu_item'



# Insert at end of file

engine = create_engine('sqlite:///restaurentmenu.db')

Base.metadata.create_all(engine)


