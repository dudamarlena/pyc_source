# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/phdoc/__init__.py
# Compiled at: 2013-10-01 11:59:05
import logging, os, os.path as p
__version__ = '0.7.3'
static_dir = p.join(p.dirname(__file__), 'static')
default_static_dir = p.join(static_dir, 'default-static')
default_template_dir = p.join(static_dir, 'default-templates')
if not hasattr(p, 'relpath'):

    def relpath(path, start=p.curdir):
        """Return a relative version of a path"""
        if not path:
            raise ValueError('no path specified')
        start_list = p.abspath(start).split(p.sep)
        path_list = p.abspath(path).split(p.sep)
        i = len(p.commonprefix([start_list, path_list]))
        rel_list = [
         p.pardir] * (len(start_list) - i) + path_list[i:]
        if not rel_list:
            return p.curdir
        return p.join(*rel_list)


    p.relpath = relpath
default_formatter = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(default_formatter)
console_handler.setLevel(logging.DEBUG)
logging.getLogger('phdoc').addHandler(console_handler)
logging.getLogger('phdoc').setLevel(logging.INFO)
import phdoc.builder, phdoc.directories, phdoc.render, phdoc.server, phdoc.templates