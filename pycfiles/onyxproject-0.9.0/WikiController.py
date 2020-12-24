# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/controllers/base/views/WikiController.py
# Compiled at: 2017-03-29 12:18:51
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import core
from flask import render_template, request, g
from flask.ext.login import login_required
from onyx.api.wiki import Wikipedia
from onyxbabel import gettext
from onyx.api.exceptions import *
wikipedia = Wikipedia()

@core.route('wiki', methods=['GET', 'POST'])
@login_required
def wiki():
    if request.method == 'GET':
        return render_template('wiki/index.html')
    if request.method == 'POST':
        try:
            wikipedia.lang = g.lang
            wikipedia.search = request.form['search']
            article = wikipedia.get_article()
            summary = wikipedia.get_summary()
            return render_template('wiki/result.html', head=article.title, url=article.url, summary=summary)
        except WikiException:
            return render_template('wiki/result.html', head=gettext('Error'), summary=gettext('This is not an article'))