__author__ = 'brian-emery'

import os
import re
from flask import Flask, render_template
from create_post import read_file, md_to_html, get_file_date
from ConfigParser import SafeConfigParser
from datetime import date

app = Flask(__name__)

# Read the config file
parser = SafeConfigParser()
parser.read('config.txt')
posts = "posts"
the_title = parser.get('config', 'BLOG_TITLE')
author = parser.get('config', 'AUTHOR')
the_year = date.today().year


@app.route("/")
def index():

    post_list = []
    html_list = []
    
    # Find files with md/txt file extensions and add them to the post_list
    for post in os.listdir(posts):
        if post.endswith(".txt") or post.endswith(".md"):
            post_path = os.path.join(posts, post)
            post_list.append(post_path)
    
    # Process each post on the post_list
    for post in post_list:
        the_file = read_file(post)
        the_html = md_to_html(the_file)
        filename = os.path.basename(post)
        find_date = re.match("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", filename)
        if find_date is not None:
            file_date = find_date.group(0)
        else:
            file_date = None
        post_date = get_file_date(post, file_date)
        final = {"date": post_date, "html": the_html}
        html_list.append(final)

    return render_template('index.html', my_title=the_title, the_author=author, my_posts=html_list,
                           year=the_year)
