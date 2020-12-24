# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../jsbuild/templates/__init__.py
# Compiled at: 2010-10-07 09:46:53
from os.path import dirname
DIR = dirname(__file__)
with open('%s/package.js' % DIR) as (pkg_template):
    jspackage = pkg_template.read()
with open('%s/module.js' % DIR) as (mod_template):
    jsmodule = mod_template.read()
with open('%s/maincall.js' % DIR) as (maincall_template):
    jsmaincall = maincall_template.read()