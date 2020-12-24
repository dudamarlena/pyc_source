# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tuvedi/__init__.py
# Compiled at: 2011-11-25 02:37:15
import pkg_resources, pypoly
__version__ = '0.3'

def run():
    path = pkg_resources.resource_filename('tuvedi.admin', 'templates')
    pypoly.config.set_pypoly('template.path', path)
    pypoly.config.set_pypoly('template.default', 'tuvedi')
    pypoly.config.set_pypoly('template.templates', ['tuvedi'])
    pypoly.run()