# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/www/config/environment.py
# Compiled at: 2007-04-18 06:57:54
import os, pylons.config, webhelpers
from econ.www.config.routing import make_map

def load_environment(global_conf={}, app_conf={}):
    map = make_map(global_conf, app_conf)
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = {'root_path': root_path, 'controllers': os.path.join(root_path, 'controllers'), 'templates': [ os.path.join(root_path, path) for path in ('components', 'templates') ], 'static_files': os.path.join(root_path, 'public')}
    tmpl_options = {}
    tmpl_options['myghty.log_errors'] = True
    tmpl_options['myghty.escapes'] = dict(l=webhelpers.auto_link, s=webhelpers.simple_format)
    return pylons.config.Config(tmpl_options, map, paths)