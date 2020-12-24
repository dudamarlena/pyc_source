# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/setup.py
# Compiled at: 2015-06-28 16:18:01
from setuptools import setup
setup(name='bookmark_merger', version='0.2.4', description='code for merging multiple firefox bookmark.html files', long_description='Bookmarks merger allows the user to merge multiple firefox bookmark.html files \ntogether, taking care to intelligently merge duplicate folder layouts. The script\nbookmark_merger.py can be used on a folder of bookmarks.html files or the \nbookmark_parser.py can be imported as a module. More detailed instructions exist\nin the README file and on the sourceforge site.\n        ', classifiers=[
 'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
 'Programming Language :: Python',
 'Programming Language :: Python :: 2',
 'Programming Language :: Python :: 3',
 'Development Status :: 3 - Alpha',
 'Environment :: Console',
 'Intended Audience :: Developers',
 'Intended Audience :: End Users/Desktop',
 'Intended Audience :: System Administrators',
 'Natural Language :: English',
 'Operating System :: OS Independent',
 'Topic :: Utilities',
 'Topic :: Internet :: WWW/HTTP :: Browsers'], author='robochat', author_email='rjsteed@talk21.com', url='https://sourceforge.net/projects/bookmark-merger/', license='LGPLv3', keywords='firefox', py_modules=[
 'bookmark_pyparser', 'example', 'example_bookmark_merger', 'setup'], scripts=[
 'bookmark_merger.py'], data_files=[
 (
  '', ['COPYING', 'COPYING.LESSER', 'README'])], install_requires=[
 'pyparsing'], zip_safe=False)