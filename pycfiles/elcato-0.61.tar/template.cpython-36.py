# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oly/repos/elcato/elcato/templates/jinja/template.py
# Compiled at: 2019-01-31 15:18:47
# Size of source mod 2**32: 965 bytes
import os
from jinja2 import Template
from jinja2 import Environment, BaseLoader
from jinja2 import Environment, FileSystemLoader
EXT = 'htm'
path = os.path.dirname(os.path.realpath(__file__))
env = Environment(loader=(FileSystemLoader(path)))
with open(f"{path}/index.html", 'r') as (fp):
    pageIndex = env.get_template('index.html')
with open(f"{path}/tags.html", 'r') as (fp):
    pageTags = env.get_template('tags.html')
with open(f"{path}/page.html", 'r') as (fp):
    pagePage = env.get_template('page.html')

def viewIndex(**data):
    return (pageIndex.render)(**data).encode()


def viewTags(**data):
    return (pageTags.render)(**data).encode()


def viewPage(**data):
    o = pagePage.render(title=(data.get('title')),
      path='../',
      doc=(data.get('doc')),
      body=(data.get('body')))
    return o.encode()