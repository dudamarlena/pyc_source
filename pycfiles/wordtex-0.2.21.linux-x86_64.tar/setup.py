# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/setup.py
# Compiled at: 2013-11-13 15:05:09
from distutils.core import setup
import publish
ctb_packages = [
 'cloudtb', 'cloudtb.extra', 'cloudtb.extra.PyQt',
 'cloudtb.tests', 'cloudtb.external']
ctb_packages = [ 'wordtex.' + n for n in ctb_packages ]
setup(name='wordtex', version=publish.VERSION, description='Latex to Word Press HTML converter', author='Garrett Berg', author_email='garrett@cloudformdesign.com', url='https://github.com/cloudformdesign/wordtex', packages=[
 'wordtex'] + ctb_packages, package_dir={'': '_publish'})