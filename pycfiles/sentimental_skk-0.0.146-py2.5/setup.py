# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/canossa/setup.py
# Compiled at: 2014-04-25 02:28:21
from setuptools import setup, find_packages
from canossa import __version__, __license__, __author__
import inspect, os
filename = inspect.getfile(inspect.currentframe())
dirpath = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))
import canossa.line
canossa.line.test()
try:
    import canossa.tff, canossa.termprop
except ImportError:
    print 'Please do:\n git submodule update --init'
    import sys
    sys.exit(1)

import canossa.cell as cell, canossa.attribute as attribute, canossa.line as line, canossa.cursor as cursor, canossa.screen as screen, canossa.popup as popup, canossa.iframe as iframe, canossa.output as output, doctest
dirty = False
for m in (attribute, cell, line, cursor,
 attribute, popup, iframe, output, screen):
    (failure_count, test_count) = doctest.testmod(m)
    if failure_count > 0:
        dirty = True

if dirty:
    raise Exception('test failed.')
setup(name='canossa', version=__version__, description='Provides basic, transparent, off-screen(invisible) terminal emulation service, for terminal apps.', long_description=open(dirpath + '/README.rst').read(), py_modules=[
 'canossa'], eager_resources=[], classifiers=[
 'Development Status :: 4 - Beta',
 'Topic :: Terminals',
 'Environment :: Console',
 'Intended Audience :: Developers',
 'License :: OSI Approved :: MIT License',
 'Programming Language :: Python'], keywords='terminal', author=__author__, author_email='user@zuse.jp', url='https://github.com/saitoha/canossa', license=__license__, packages=find_packages(exclude=[]), zip_safe=True, include_package_data=False, install_requires=[
 'tff'], entry_points='\n                              [console_scripts]\n                              canossa = canossa:main\n                              ')