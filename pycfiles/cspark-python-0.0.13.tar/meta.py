# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cspace/hgsite/meta.py
# Compiled at: 2013-06-09 10:57:05
__doc__ = 'Project metadata\nCopyright (C) 2012 Remy Blank\n'
import time as _time
project = 'HgSite'
name = 'cspace-%s' % (project,)
version = '1.1'
devel = version.endswith('dev')
date = '2013-03-02' if not devel else _time.strftime('%Y-%m-%d')
author = 'Remy Blank'
author_email = 'software@c-space.org'
copyright = 'Copyright (C) %s %s' % (date[0:4], author)
license = 'GPLv3'
license_url = 'http://www.gnu.org/licenses/gpl-3.0.html'
repository_url = 'http://rc.c-space.org/hg/%s' % project
url = repository_url
download_url = 'http://c-space.org/download/%s/' % project
min_python_version = (2, 6)
description = 'Serve a web site straight out of a Mercurial repository'
long_description = '%(project)s is a Mercurial extension that allows serving a dynamic, read-only\nwebsite using a Mercurial repository as the backend storage. Pages are served\nby `hgweb`, the same component that serves the Mercurial repository, and no\nadditional configuration is necessary in the web server.\n\nFor more information, see the project site at:\n\n  %(url)s\n' % globals()
keywords = [
 'mercurial', 'extension', 'version control', 'web site', 'documentation']
platforms = [
 'OS Independent']
classifiers = [
 'Development Status :: 4 - Beta',
 'Environment :: Plugins',
 'Environment :: Web Environment',
 'Intended Audience :: Developers',
 'Intended Audience :: System Administrators',
 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
 'Operating System :: OS Independent',
 'Programming Language :: Python',
 'Programming Language :: Python :: 2',
 'Programming Language :: Python :: 2.6',
 'Programming Language :: Python :: 2.7',
 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
 'Topic :: Internet :: WWW/HTTP :: Site Management',
 'Topic :: Software Development :: Version Control']