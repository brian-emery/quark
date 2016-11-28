import os
import re
from flask import Flask, render_template, redirect, url_for, abort, request
from create_post import read_file, md_to_html, get_file_date
from ConfigParser import SafeConfigParser
from datetime import date, datetime

app = Flask(__name__)

parser = SafeConfigParser()
parser.read('config.txt')
posts = "posts"
the_title = parser.get('config', 'BLOG_TITLE')
subtitle = parser.get('config', 'SUBTITLE')
author = parser.get('config', 'AUTHOR')
posts_per_page = int(parser.get('config', 'POSTS_PER_PAGE'))
text_color = parser.get('style', 'TEXT_COLOR')
back_color = parser.get('style', 'BACKGROUND_COLOR')
the_year = date.today().year
time_format = "%Y-%m-%d"
regex = re.compile("^([0-9]{4}-[0-9]{2}-[0-9]{2})")


def gettimestamp(the_file):
    match = regex.search(os.path.basename(the_file))
    return datetime.strptime(match.group(0), time_format)


def create_post_list(page_id, query):

    post_list = []
    sorted_post_list = []

    for post in os.listdir(posts):
        if post.endswith(".md"):
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

    if not query:
        post_count = len(sorted_post_list)
        first_post = posts_per_page * page_id
        last_post = first_post + posts_per_page
        if last_post > post_count:
            last_post = post_count
        sorted_post_list = sorted_post_list[first_post:last_post]
    else:
        sorted_post_list = [x for x in sorted_post_list if query in x]

    return sorted_post_list


def generate_page(page_id, query):

    post_list = create_post_list(page_id, query)
    html_list = []

    for post in post_list:
        link = os.path.splitext(os.path.basename(post))[0]
        the_file = read_file(post)
        the_html = md_to_html(the_file)
        filename = os.path.basename(post)
        post_date = get_file_date(post, filename[0:10])
        final = {"date": post_date, "html": the_html, "link": link}
        html_list.append(final)
    return html_list


@app.route("/")
def index():
    page_id = 0
    return redirect(url_for('page', page_id=page_id))


@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form['search']
    page_id = 0
    html_list = generate_page(page_id, query)

    return render_template('search.html', my_title=the_title, subtitle=subtitle, the_author=author,
                           my_posts=html_list, year=the_year, text_color=text_color,
                           back_color=back_color)


@app.route('/<int:page_id>', methods=['GET', 'POST'])
def page(page_id):
    query = None
    html_list = generate_page(page_id, query)
    list_length = len(html_list)
    next_page = True

    if list_length < 1:
        page_id = 0
        return redirect(url_for('page', page_id=page_id))
    if list_length < posts_per_page:
        next_page = False
    return render_template('index.html', my_title=the_title, subtitle=subtitle, the_author=author,
                           my_posts=html_list, year=the_year, page_id=page_id,
                           next_page=next_page, text_color=text_color,
                           back_color=back_color)


@app.route('/post/<string>')
def perma_link(string):

    post = posts + "/" + string + ".md"
    html_list = []
    if post is not None and os.path.isfile(post):
        the_file = read_file(post)
        the_html = md_to_html(the_file)
        filename = os.path.basename(post)
        post_date = get_file_date(post, filename[0:10])
        final = {"date": post_date, "html": the_html}
        html_list.append(final)
        return render_template('post.html', my_title=the_title, subtitle=subtitle, the_author=author,
                               my_posts=html_list, year=the_year, text_color=text_color,
                               back_color=back_color)
    else:
        abort(404)
