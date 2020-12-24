# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cblog/widgets/base.py
# Compiled at: 2006-12-15 09:11:50
__all__ = [
 'HelplinkLabel', 'register_sitewidgets', 'serialize_et']
import pkg_resources, cElementTree as ET
from turbogears import config
from turbogears.widgets.meta import load_kid_template
from turbogears.widgets import register_static_directory
static_dir = pkg_resources.resource_filename('cblog', 'static')
register_static_directory('cblog', static_dir)
PlainHTML = load_kid_template('<html xmlns:py="http://purl.org/kid/ns#"\n  py:replace="elements"/>', modname='turbogears.widgets.plainhtml')[0]

def register_sitewidgets(widgets, pkg_name):
    """Register widgets to be included on every page.

    'widgets' is a list of widget instance names.

    Order of the widget names is important for proper inclusion
    of JavaScript and CSS.

    The named widget instances have to be instantiated in
    some of your modules.

    'pkg_name' is the name of your Python module/package, in which
    the widget instances are defined.
    """
    include_widgets = config.get('tg.include_widgets', [])
    for widget in widgets:
        include_widgets.append('%s.%s' % (pkg_name, widget))

    config.update({'global': {'tg.include_widgets': include_widgets}})


def serialize_et(elem, format='html'):
    t = PlainHTML(elements=elem)
    return t.serialize(output=format, fragment=True)


class HelplinkLabel(object):
    """A label with a link opening an online help window."""
    __module__ = __name__

    def __init__(self, label='', **params):
        self.params = params
        self.label = label

    def update_params(self, params):
        """Enter method docstring here."""
        for k in params:
            if callable(params[k]):
                params[k] = params[k]()

    def __call__(self, **params):
        _params = dict()
        _params.update(self.params)
        _params.update(params)
        self.update_params(_params)
        helplink = ET.Element('a', {'class': 'helplink'}, href=_params.get('url', ''), target='_blank')
        helplink.text = _params.get('linklabel', '')
        return (self.label, helplink)