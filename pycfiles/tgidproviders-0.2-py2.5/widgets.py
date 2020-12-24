# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tgidproviders/widgets.py
# Compiled at: 2007-09-02 11:27:28
import pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory
js_dir = pkg_resources.resource_filename('tgidproviders', 'static/javascript')
register_static_directory('tgidproviders', js_dir)