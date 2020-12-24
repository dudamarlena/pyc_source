# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/ezinstall-project/ezinstall/__init__.py
# Compiled at: 2017-08-29 19:59:53
"""
``ezinstall (Easy install)`` is a package allows you to instantly install
package to your python environment **without having** ``setup.py`` file.
It simply copy the source code to ``site-packages`` directory.
**It also works for virtualenv**. The behavior is exactly the same as
``pip install setup.py --ignore-installed``.

It doesn't install any dependencies from ``requirement.txt``.
"""
__version__ = '0.0.2'
__short_description__ = 'Instantly install your package to site-packages.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@me.com'
__maintainer__ = 'Sanhe Hu'
__maintainer_email__ = 'husanhe@me.com'
__github_username__ = 'MacHu-GWU'
try:
    from .ezinstall import install
except:
    pass