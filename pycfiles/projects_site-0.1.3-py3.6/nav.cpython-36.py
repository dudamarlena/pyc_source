# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/projects/nav.py
# Compiled at: 2020-04-20 14:39:31
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