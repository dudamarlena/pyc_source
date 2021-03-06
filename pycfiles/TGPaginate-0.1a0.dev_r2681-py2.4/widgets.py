# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tgpaginate/widgets.py
# Compiled at: 2009-05-27 16:52:35
import kid, types, pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory, DataGrid
from turbogears import expose
from scriptaculous import prototype_js
from controllers import paginate
from turbojson import jsonify
from sqlobject.main import SelectResults
js_dir = pkg_resources.resource_filename('tgpaginate', 'static/javascript')
register_static_directory('tgpaginate.js', js_dir)
js_dir = 'tgpaginate.js'
css_dir = pkg_resources.resource_filename('tgpaginate', 'static/css')
register_static_directory('tgpaginate.css', css_dir)
css_dir = 'tgpaginate.css'
images_dir = pkg_resources.resource_filename('tgpaginate', 'static/images')
register_static_directory('tgpaginate.images', images_dir)

class PaginatedGrid(DataGrid):
    __module__ = __name__
    params = ['var_name']
    var_name = 'items'
    template = 'tgpaginate.templates.paginatedgrid'


class AjaxPaginatedGrid(DataGrid):
    __module__ = __name__
    template = 'tgpaginate.templates.paginatedajaxgrid'
    javascript = [prototype_js, JSLink(js_dir, 'paginatedajaxgrid.js')]
    params = ['search_params', 'url', 'var_name', 'no_init', 'eval_scripts']
    eval_scripts = False
    options = {}
    search_params = {}
    url = ''
    var_name = 'items'
    no_init = ''
    row_attributes = None

    def __init__(self, *args, **kw):
        self.row_attributes = kw.pop('row_attributes', None)
        super(AjaxPaginatedGrid, self).__init__(*args, **kw)
        self.css.append(CSSLink(css_dir, 'paginatedgrid.css'))
        return

    def update_params(self, d):
        super(AjaxPaginatedGrid, self).update_params(d)
        options = dict()
        options['search_params'] = d.get('search_params')
        options['url'] = d.get('url')
        options['var_name'] = d.get('var_name')
        options['no_init'] = d.get('no_init')
        options['eval_scripts'] = d.get('eval_scripts')
        options['columns'] = [ i.name for i in d.get('columns') ]
        options['row_attributes'] = d.get('row_attributes')
        d['options'] = jsonify.encode(options)


class AjaxPaginatedGridDesc(WidgetDescription):
    __module__ = __name__
    full_class_name = 'tgpaginate.widgets.AjaxPaginatedGrid'
    for_widget = AjaxPaginatedGrid(name='demo_grid', fields=[
     ('ID',
      lambda x: x[0]),
     ('Person',
      lambda x: x[1])], url='%s/data_feeder' % full_class_name, var_name='example_list')
    template = '\n    <div xmlns:py="http://purl.org/kid/ns#">\n        ${for_widget.display()}\n        <script type="text/javascript">\n            // this is only needed if you actually need to select some data\n            $(\'demo_grid\').ajax.options.row_selector = \n                function (row) {\n                    // The argument row contains all the columns in a list.\n                    // Also, row is a a js object if it\'s passed through \n                    // jsonify_datagrid (row.id, row.name, etc).\n                    alert(\'selected id: \' + row[0] + \', data: \' + row);\n                }\n        </script>\n    </div>\n    '
    params = [
     'example_list']

    def __init__(self, *args, **kw):
        super(AjaxPaginatedGridDesc, self).__init__(*args, **kw)
        self.example_list = []
        for i in xrange(1, 96):
            self.example_list.append((i, 'Person %i' % i))

    @expose(format='json')
    @paginate('example_list')
    def data_feeder(self, *args, **kw):
        return dict(example_list=self.example_list)


from turbogears.decorator import weak_signature_decorator

def jsonify_datagrid(datagrid, list_name, *deco_args, **deco_kw):
    """Builds a jsonifiable data structure that contains the data specified
      in the datagrid columns.
    """

    def entangle(func):

        def decorated(func, *args, **kw):
            output = func(*args, **kw)
            data = output.get(list_name)
            if isinstance(data, SelectResults):
                data = list(data)
            if data:
                if isinstance(datagrid, (types.MethodType, types.FunctionType)):
                    datagrid_ = datagrid(args[0])
                else:
                    datagrid_ = datagrid
                prepared_data = list()
                datagrid_params = dict()
                datagrid_.update_params(datagrid_params)
                row_attributes = datagrid_.row_attributes
                for row in data:
                    data_row = dict()
                    if row_attributes:
                        if callable(row_attributes):
                            data_row['__row_attributes'] = row_attributes(row)
                        else:
                            data_row['__row_attributes'] = row_attributes
                    for col in datagrid_params['columns']:
                        data_row[col.name] = process_data(col.get_field(row))

                    prepared_data.append(data_row)

                output[list_name] = prepared_data
            return output

        return decorated

    return weak_signature_decorator(entangle)


serializer = kid.HTMLSerializer()

def process_data(data):
    if is_Element_or_kidXML(data):
        data = serializer.serialize(stream=kid.ElementStream(data), fragment=1, encoding='utf-8')
        data = data.decode('utf-8')
    return data


def is_Element_or_kidXML(data):
    if hasattr(data, 'tag') and hasattr(data, 'attrib') or isinstance(data, kid.parser.ElementStream):
        return True
    try:
        if isinstance(types.GeneratorType, data):
            return True
    except TypeError:
        pass

    return False