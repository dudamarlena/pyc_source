# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spinner/widgets.py
# Compiled at: 2009-08-18 08:27:48
import pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory
from turbogears.widgets import *
static_dir = pkg_resources.resource_filename('spinner', 'static')
register_static_directory('spinner', static_dir)

class Spinner(FormField):
    """Creates a spinner widget which can be used directly in html"""
    template = '\n      <form xmlns:py="http://purl.org/kid/ns#">\n      <table cellpadding="0" cellspacing="0" border="0">\n      <tr>\n      <td rowspan="2"><input type="text" name="number" value="${value}" class="${field_class}" style="width:50px;height:15px;font-weight:bold;" /></td>\n<td><input type="button" value=" /\\ " onclick="this.form.number.value++;" style="font-size:7px;margin:0;padding:0;width:20px;height:12px;" /></td>\n      </tr>\n      <tr>\n<td><input type="button" value=" \\/ " onclick="this.form.number.value--;" style="font-size:7px;margin:0;padding:0;width:20px;height:12px;" /></td>\n      </tr>\n      </table>\n      </form>\n      '


class Spinner(WidgetDescription):
    name = 'Spinner'
    for_widget = Spinner('spinner', default='10')
    full_class_name = 'spinner.Spinner'