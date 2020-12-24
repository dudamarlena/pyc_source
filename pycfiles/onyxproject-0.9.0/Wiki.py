# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/Aituglo/Desktop/Onyx/onyx/core/controllers/api/views/Wiki.py
# Compiled at: 2017-03-29 12:18:51
"""
Onyx Project
http://onyxproject.fr
Software under licence Creative Commons 3.0 France
http://creativecommons.org/licenses/by-nc-sa/3.0/fr/
You may not use this software for commercial purposes.
@author :: Cassim Khouani
"""
from .. import api
from flask import render_template, request, g
from flask.ext.login import login_required
from onyx.api.wiki import Wikipedia
from onyxbabel import gettext
from onyx.api.exceptions import *
wikipedia = Wikipedia()

@api.route('wiki', methods=['GET', 'POST'])
@login_required
def wiki():
    if request.method == 'POST':
        try:
            wikipedia.lang = g.lang
            wikipedia.search = request.form['search']
            article = wikipedia.get_article()
            summary = wikipedia.get_summary()
            return article
        except WikiException:
            return gettext('An error has occured !')