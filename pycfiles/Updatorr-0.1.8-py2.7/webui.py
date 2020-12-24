# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/updatorr/webui.py
# Compiled at: 2013-03-11 10:45:08
import os, logging, pkg_resources
from deluge.plugins.pluginbase import WebPluginBase
log = logging.getLogger(__name__)

def get_resource(filename):
    return pkg_resources.resource_filename('updatorr', os.path.join('data', filename))


class WebUI(WebPluginBase):
    scripts = [
     get_resource('updatorr.js')]
    debug_scripts = scripts