# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/snakefight/util.py
# Compiled at: 2011-05-18 20:43:47
import inspect, os
from collections import defaultdict
from StringIO import StringIO
from pkg_resources import resource_string
web_xml_defaults = defaultdict(str)
web_xml_defaults.update(log_level='info')

def gen_web_xml(**options):
    """Generate a deployment descriptor (web.xml)"""
    vars = web_xml_defaults.copy()
    vars.update(options)
    tmpl = os.path.join('war_template', 'WEB-INF', 'web.xml_tmpl')
    return resource_string('snakefight', tmpl) % vars


def gen_paste_loadapp(config, app_name):
    """Generate a .py module with a loadapp() callable that loads the
    Paste app via config"""
    code = StringIO()
    code.write("# as located in WEB-INF\nconfig = '%s'\napp_name = '%s'\n\n" % (config, app_name))
    code.write(inspect.getsource(loadapp))
    return code.getvalue()


def loadapp():
    """Load a WSGI app from a Paste config file in WEB-INF"""
    import os, paste.deploy
    config_dir = os.path.normpath(__file__)
    for i in range(2):
        config_dir = os.path.dirname(config_dir)

    return paste.deploy.loadapp('config:%s#%s' % (
     os.path.join(config_dir, config), app_name))