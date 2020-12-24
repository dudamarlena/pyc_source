# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/SutekhInfo.py
# Compiled at: 2019-12-12 07:58:05
"""Requirements and such for setuptools"""
from pkg_resources import resource_string
GPL = 'License :: OSI Approved :: GNU General Public License (GPL)'
LGPL = 'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)'
MIT = 'License :: OSI Approved :: MIT License'
PYTHON = ('License :: OSI Approved :: Python Software Foundation License', )

class SutekhInfo(object):
    VERSION = (1, 0, 0, 'final', 1)
    BASE_VERSION_STR = ('.').join([ str(x) for x in VERSION[:3] ])
    VERSION_STR = {'final': BASE_VERSION_STR, 
       'alpha': BASE_VERSION_STR + 'a' + str(VERSION[4]), 
       'rc': BASE_VERSION_STR + 'rc' + str(VERSION[4])}[VERSION[3]]
    NAME = 'Sutekh'
    DESCRIPTION = 'VtES Card Collection Manager'
    PEOPLE = {'Simon': ('Simon Cross', 'hodgestar+sutekh@gmail.com'), 
       'Neil': ('Neil Muller', 'drnlmuller+sutekh@gmail.com'), 
       'Adrianna': ('Adrianna Pinska', 'adrianna.pinska+sutekh@gmail.com')}
    AUTHORS = [
     PEOPLE['Simon'],
     PEOPLE['Neil']]
    AUTHOR_NAME = AUTHORS[0][0]
    AUTHOR_EMAIL = AUTHORS[0][1]
    MAINTAINERS = AUTHORS
    MAINTAINER_NAME = MAINTAINERS[0][0]
    MAINTAINER_EMAIL = MAINTAINERS[0][1]
    ARTISTS = [
     PEOPLE['Simon']]
    DOCUMENTERS = [
     PEOPLE['Neil'],
     PEOPLE['Adrianna']]
    SOURCEFORGE_URL = 'https://sourceforge.net/projects/sutekh/'
    PYPI_URL = 'https://pypi.python.org/pypi/Sutekh/'
    LICENSE = 'GPL'
    LICENSE_TEXT = resource_string(__name__, 'COPYING')
    CLASSIFIERS = [
     'Development Status :: 4 - Beta',
     'Environment :: Console',
     'Environment :: Win32 (MS Windows)',
     'Environment :: X11 Applications :: GTK',
     'Intended Audience :: Developers',
     'Intended Audience :: End Users/Desktop',
     GPL,
     'Operating System :: Microsoft :: Windows',
     'Operating System :: POSIX',
     'Programming Language :: Python :: 2.6',
     'Programming Language :: Python :: 2.7',
     'Topic :: Games/Entertainment',
     'Topic :: Software Development :: Libraries :: Python Modules']
    PLATFORMS = [
     'Linux',
     'Windows']
    INSTALL_REQUIRES = [
     'SQLObject >= 0.9.0',
     'singledispatch',
     'ply',
     'configobj',
     'keyring']
    NON_EGG_REQUIREMENTS = [
     'setuptools',
     'pysqlite',
     'PyGTK']
    DEPENDENCY_LICENSES = {'SQLObject': (
                   LGPL,
                   'http://www.gnu.org/copyleft/lesser.html',
                   'Version 3'), 
       'singledispath': (
                       MIT,
                       'https://bitbucket.org/ambv/singledispatch',
                       'MIT License'), 
       'ply': (
             LGPL,
             'http://www.gnu.org/licenses/lgpl-2.1.html',
             'Version 2.1'), 
       'configobj': ('License :: OSI Approved :: BSD License', 'http://www.voidspace.org.uk/python/configobj.html#license',
 'New-BSD license'), 
       'keyring': (
                 MIT,
                 'https://bitbucket.org/kang/python-keyring-lib/raw/tip/README.rst',
                 'MIT license'), 
       'setuptools': (
                    PYTHON,
                    'http://www.python.org/psf/license/',
                    'Version 2'), 
       'PyGTK': (
               LGPL,
               'http://www.gnu.org/copyleft/lesser.html',
               'Version 2 or later'), 
       'GTK': (
             LGPL,
             'http://www.gnu.org/copyleft/lesser.html',
             'Version 2 or later'), 
       'Python': (
                PYTHON,
                'http://www.python.org/psf/license/',
                'Version 2'), 
       'ZipDLL': (
                GPL,
                'http://www.gnu.org/copyleft/gpl.html',
                'Version 2 or later')}