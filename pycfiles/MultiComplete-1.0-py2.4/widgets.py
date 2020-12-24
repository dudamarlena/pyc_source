# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/multicomplete/widgets.py
# Compiled at: 2006-07-02 06:15:03
import pkg_resources
from turbogears import expose
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory, FormField
js_dir = pkg_resources.resource_filename('multicomplete', 'static/javascript')
register_static_directory('multicomplete', js_dir)
xdbc = JSLink('multicomplete', 'xdbc.js')
xWoco = JSLink('multicomplete', 'xWoco.js')

class MultiCompleteBase(FormField):
    __module__ = __name__
    javascript = [xdbc, xWoco]
    params = ['db_src']


class MultiCompleteField(MultiCompleteBase):
    """Provides a text field where the words are automatically filled
    in based on the XML file provided at db_src."""
    __module__ = __name__
    template = '<div xmlns:py="http://purl.org/kid/ns#"><input xmlns:py="http://purl.org/kid/ns#"\n        name="${name}"\n        class="${field_class}"\n        id="${field_id}"\n        py:attrs="attrs"\n        value="${value}"\n        type="text"\n    />\n    <script type="text/javascript">\n        woco.init("${db_src}", "${field_id}");\n    </script>\n    </div>\n    '
    params = [
     'attrs', 'db_src']
    attrs = {}


class MultiCompleteTextArea(MultiCompleteBase):
    """Provides a text field where the words are automatically filled
    in based on the XML file provided at db_src."""
    __module__ = __name__
    template = '<div xmlns:py="http://purl.org/kid/ns#"><textarea xmlns:py="http://purl.org/kid/ns#"\n        name="${name}"\n        class="${field_class}"\n        id="${field_id}"\n        rows="${rows}"\n        cols="${cols}"\n        py:attrs="attrs"\n        py:content="value"\n    />\n    <script type="text/javascript">\n        woco.init("${db_src}", "${field_id}");\n    </script>\n    </div>\n    '
    params = [
     'attrs', 'rows', 'cols', 'db_src']
    attrs = {}
    rows = 7
    cols = 50


class MultiCompleteFieldDesc(WidgetDescription):
    __module__ = __name__
    full_class_name = 'multicomplete.MultiCompleteField'

    def __init__(self, *args, **kw):
        super(MultiCompleteFieldDesc, self).__init__(*args, **kw)
        self.for_widget = MultiCompleteField(name='multicomplete', db_src='%s/data.json' % self.full_class_name)

    [
     expose('json')]

    def data_json(self):
        return dict(data=['alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india', 'juliet', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo', 'sierra', 'tango', 'uniform', 'victor', 'whiskey', 'xray', 'yankee', 'zulu'])