# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jakob/Jest/Jalapeno/GUI/views/sites.py
# Compiled at: 2017-03-04 23:58:55
# Size of source mod 2**32: 839 bytes
from flask import Blueprint, render_template, request
from Jalapeno.lib.siteMgr import Site
sites = Blueprint('sites', __name__)

@sites.route('/sites')
def show():
    return render_template('sites.html')


@sites.route('/sites/site-create', methods=['GET', 'POST'])
def create():
    try:
        sitename = request.get_data().decode()
        Site.site_create(sitename)
        Site.site_list_add(sitename)
    except:
        print('Something wrong when creating')

    return render_template('sites.html')


@sites.route('/sites/switch-site', methods=['GET', 'POST'])
def switch():
    try:
        sitename = request.get_data().decode()
        if Site.site_switch(sitename):
            return sitename
        else:
            return
    except:
        pass


@sites.route('/sites/current-site', methods=['GET', 'POST'])
def current():
    try:
        sitename = Site.get_site()
    except:
        pass

    return sitename