# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/projects/nav.py
# Compiled at: 2020-04-25 05:24:46
# Size of source mod 2**32: 801 bytes
from flask_login import current_user
from flask_nav.elements import Navbar, View
from projects.conf import config
from projects import nav

@nav.navigation()
def nav_bar():
    navbar = list(Navbar(View('{}'.format(config.get('PROJECTS', 'title')), 'projects.projects'), View('Projects', 'projects.projects')).items)
    if current_user.is_authenticated:
        navbar.extend([
         View('My Projects', 'projects.my_projects'),
         View('Create Project', 'projects.create'),
         View('Logout', 'projects.logout')])
    else:
        navbar.extend([
         View('Login', 'projects.login')])
    return Navbar('{}'.format(config.get('PROJECTS', 'title')), *navbar)