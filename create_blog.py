__author__ = 'brian-emery'

import os
import re
from flask import Flask, render_template, redirect, url_for
from create_post import read_file, md_to_html, get_file_date
from ConfigParser import SafeConfigParser
from datetime import date, datetime

app = Flask(__name__)

parser = SafeConfigParser()
parser.read('config.txt')
posts = "posts"
the_title = parser.get('config', 'BLOG_TITLE')
author = parser.get('config', 'AUTHOR')
posts_per_page = int(parser.get('config', 'POSTS_PER_PAGE'))
the_year = date.today().year


def create_post_list(page_id):
    time_format = "%Y-%m-%d"
    regex = re.compile("^([0-9]{4}\-[0-9]{2}\-[0-9]{2})")

    def gettimestamp(the_file):
        match = regex.search(os.path.basename(the_file))
        return datetime.strptime(match.group(0), time_format)

    post_list = []
    sorted_post_list = []

    for post in os.listdir(posts):
        if post.endswith(".txt") or post.endswith(".md"):
            post_path = os.path.join(posts, post)
            filename = os.path.basename(post)
            find_date = regex.match(filename)
            if find_date is not None:
                file_date = find_date.group(0)
            else:
                file_date = None
            get_file_date(post, file_date)
            post_list.append(post_path)

    for post in sorted(post_list, key=gettimestamp, reverse=True):
        sorted_post_list.append(post)

    post_count = len(sorted_post_list)
    first_post = posts_per_page * page_id
    last_post = first_post + posts_per_page
    if last_post > post_count:
        last_post = post_count
    cut_list = sorted_post_list[first_post:last_post]
    return cut_list


def generate_page(page_id):

    post_list = create_post_list(page_id)
    html_list = []

    for post in post_list:
        the_file = read_file(post)
        the_html = md_to_html(the_file)
        filename = os.path.basename(post)
        post_date = get_file_date(post, filename[0:10])
        final = {"date": post_date, "html": the_html}
        html_list.append(final)
    return html_list


@app.route("/")
def index():
    page_id = 0
    return redirect(url_for('page', page_id=page_id))


@app.route('/<int:page_id>')
def page(page_id):
    html_list = generate_page(page_id)
    list_length = len(html_list)
    next_page = True

    if list_length < 1:
        page_id = 0
        return redirect(url_for('page', page_id=page_id))
    if list_length < posts_per_page:
        next_page = False
    return render_template('index.html', my_title=the_title, the_author=author,
                           my_posts=html_list, year=the_year, page_id=page_id,
                           next_page=next_page)