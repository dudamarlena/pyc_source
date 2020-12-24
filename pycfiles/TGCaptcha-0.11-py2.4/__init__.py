# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tgcaptcha/__init__.py
# Compiled at: 2007-06-02 21:58:49
from paste.script import templates
import pkg_resources
from widgets import *

class TGCaptchaConfig(templates.Template):
    __module__ = __name__
    egg_plugins = [
     'TGCaptchaConfig']
    _template_dir = pkg_resources.resource_filename('tgcaptcha', 'template')
    summary = 'Provides a configuration file template for TGCaptcha'
    required_templates = ['tgbase']
    use_cheetah = False