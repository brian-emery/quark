# quark
**A teeny-tiny, feature-limited blogging platform.**

quark is written in Python and utilizes Flask, jinja2, tornado, Markdown, 
jQuery, and Bootstrap.

### Installing quark

* Install Python 2.7+ with Flask, tornado, and Markdown
* Edit config.txt to meet your needs.
* Run: `python run.py`

### Using quark

Any .txt or .md files dropped into the 'posts' directory will be added to the
post list. quark expects these files to be written in markdown. If you want
the post to have a specific date, prepend it to the filename. For example:

`2015-04-13_my_first_post.txt`

If you do not specify a date in the filename, quark will rename the file with
today's date. The posts will be sorted (descending) by date.

### To Do:

* Add pagination.
* Properly sort posts within a single day.

### Screenshot:

![screenshot](http://i.imgur.com/ut0PnPO.png)
