# "Database code" for the DB Forum.

import bleach
import psycopg2


# Get posts from database

def get_posts():
  # Connect to database.
  db = psycopg2.connect("dbname=forum")
  # Create cursor to sort
  c = db.cursor()
  """Return all posts from the 'database', most recent first."""
  c.execute("SELECT time, content FROM posts order by time DESC")
  posts = c.fetchall()
  db.close()
  return posts

# Add Post to Database

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  db = psycopg2.connect("dbname=forum")
  c = db.cursor()
  # IMPORTANT: When using Insert, use query paramaters instead of String substituition
  # Use bleach to prevent JS code injected into the browser
  c.execute("INSERT INTO posts (content) VALUES (%s)",
            (bleach.clean(content), ))
  db.commit()
  db.close()
