#
# Database access functions for the web forum.
# 

import time
import bleach
import psycopg2

# Database connection
# DB = []


# Get posts from database.
def get_all_posts():
    """Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    """
    db = psycopg2.connect('dbname=forum')
    c = db.cursor()
    query = "SELECT time, content FROM posts ORDER BY time DESC;"
    c.execute(query)
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in
             c.fetchall()]
    db.close()
    # posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    # posts.sort(key=lambda row: row['time'], reverse=True)
    return posts


# Add a post to the database.
def add_post(content):
    """Add a new post to the database.

    Args:
      content: The text content of the new post.
    """
    db = psycopg2.connect('dbname=forum')
    c = db.cursor()
    query = "INSERT INTO posts (content) VALUES (%s);"
    c.execute(query, (bleach.clean(content),))  # Secure query execute
    db.commit()
    db.close()
    # t = time.strftime('%c', time.localtime())
    # DB.append((t, content))
