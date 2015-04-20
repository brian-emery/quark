__author__ = 'brian-emery'

import codecs
import markdown
import os
from datetime import datetime


def read_file(the_file):
    input_file = codecs.open(the_file, mode="r", encoding="utf-8")
    text = input_file.read()
    return text


def md_to_html(the_text):
    html = markdown.markdown(the_text)
    return html


def get_file_date(the_file, the_date):
    if validate(the_date):
        return the_date
    else:
        the_day = datetime.today().strftime('%Y-%m-%d')
        path, filename = os.path.split(the_file)
        mod_filename = the_day + "_" + filename
        new_file = os.path.join(path, mod_filename)
        os.rename(the_file, new_file)
        return the_day


def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except TypeError:
        return False
    except ValueError:
        return False