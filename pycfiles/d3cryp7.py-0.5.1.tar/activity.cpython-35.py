# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bkvaluemeal/Documents/d3cryp7/d3cryp7/blueprints/activity.py
# Compiled at: 2016-12-30 01:56:32
# Size of source mod 2**32: 1346 bytes
"""
Activity

This module defines the Flask blueprint for the application's activity log. See
the documentation for each object and their respective unit tests for more
information.
"""
from flask import Blueprint, render_template
import d3cryp7, sqlite3
blueprint = Blueprint('activity', __name__, template_folder='../templates')

@blueprint.route('/')
def show():
    """
        The activity log
        """
    with sqlite3.connect(d3cryp7.__db__) as (database):
        c = database.cursor()
        c.execute('SELECT count() FROM activity_log')
        count = c.fetchone()[0]
        c.execute('SELECT rowid, * FROM activity_log ORDER BY rowid DESC LIMIT 50')
        return render_template('activity.html', log=c, count=int(count / 50) + (count % 50 > 0) + 1, page=1)


@blueprint.route('/page')
@blueprint.route('/page/<int:page>')
def page(page=1):
    """
        The activity log at page X
        """
    with sqlite3.connect(d3cryp7.__db__) as (database):
        c = database.cursor()
        c.execute('SELECT count() FROM activity_log')
        count = c.fetchone()[0]
        c.execute('SELECT rowid, * FROM activity_log WHERE rowid <= %d ORDER BY rowid DESC LIMIT 50' % (count - (page - 1) * 50))
        return render_template('activity.html', log=c, count=int(count / 50) + (count % 50 > 0) + 1, page=page)