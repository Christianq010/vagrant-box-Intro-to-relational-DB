# Creating a Database with SQLAlchemy ( our ORM for python - database mapping)
# Step 1 - Configuration

import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()
# Insert at end of file

engine = create_engine('sqlite:///restaurentmenu.db')

Base.metadata.create_all(engine)

