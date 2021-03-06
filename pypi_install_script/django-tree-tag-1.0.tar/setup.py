# Copyright (C) 2012 Johannes Spielmann
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup

with open('README') as file:
    long_description = file.read()

setup(
    name='django-tree-tag',
    version='1.0',
    
    packages=['tree_tag', 'tree_tag.templatetags'],
    
    url='https://bitbucket.org/shezi/django-tree-tag/',
    
    author='Johannes Spielmann',
    author_email='jps@shezi.de',
    
    description='A simple module for recursion in Django templates',
    long_description=long_description,
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        ],
    )
