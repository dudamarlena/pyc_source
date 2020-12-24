# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gas/endi/py3/deform_extensions/deform_extensions/__init__.py
# Compiled at: 2019-11-08 10:04:06
# Size of source mod 2**32: 27423 bytes
"""
Provide custom colander schemas and associated widgets to render forms
differently
"""
import cgi, json, warnings, colander, deform, random, fanstatic
from string import ascii_lowercase
from collections import OrderedDict
from itertools import zip_longest
import deform.schema as defaults
import js.jquery as jquery
import js.underscore as underscore
from js.jquery_timepicker_addon import timepicker_js
import js.jqueryui as jqueryui_bootstrap_theme
TEMPLATES_PATH = 'deform_extensions:templates/'

def gen_random_string(size=15):
    """
    Generate random string

        size

            size of the resulting string
    """
    return ''.join((random.choice(ascii_lowercase) for _ in range(size)))


def random_tag_id(size=15):
    """
    Return a random string supposed to be used as tag id
    """
    return gen_random_string(size)


def grouper(iterable, items, fillvalue=None):
    """
    Collect data into fixed-length chunks or blocks

    e.g:

        grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx

    Got it from https://docs.python.org/2/library/itertools.html#recipes
    """
    args = [
     iter(iterable)] * items
    return zip_longest(*args, **{'fillvalue': fillvalue})


class DisabledInput(deform.widget.Widget):
    __doc__ = '\n        A non editable input\n    '
    template = 'disabledinput.pt'

    def serialize(self, field, cstruct=None, readonly=True):
        if cstruct is colander.null:
            cstruct = ''
        quoted = cgi.escape(cstruct, quote='"')
        params = {'name':field.name,  'value':quoted}
        return (field.renderer)((self.template), **params)

    def deserialize(self, field, pstruct):
        return pstruct


class Inline(colander.Mapping):
    __doc__ = '\n    Inline schema type, necessary to avoid our mapping to be render as tabs\n    (see deform_bootstrap.utils.tabify function )\n    '


class InlineMappingWidget(deform.widget.MappingWidget):
    __doc__ = '\n    The custom widget we use to render our mapping\n    '
    template = 'inline_mapping.pt'
    item_template = 'inline_mapping_item.pt'
    readonly_template = 'inline_mapping.pt'
    readonly_item_template = 'inline_mapping_item.pt'


class InlineMappingSchema(colander.MappingSchema):
    __doc__ = '\n    Schema providing inline rendering of form elements\n    '
    schema_type = Inline
    widget = InlineMappingWidget()


class VoidWidget(deform.widget.Widget):
    __doc__ = '\n    Void widget used to fill our grid\n    '

    def __init__(self, width=1):
        self.width = width

    def render_template(self, template):
        """
        Return a div of class col-md-<width>
        """
        return "<div class='col-md-{0}'><br /></div>".format(self.width)


class StaticWidget(deform.widget.Widget):
    __doc__ = '\n    Static widget used to insert static html in grids\n    '

    def __init__(self, html_str, width=1):
        self.width = width
        self.html_str = html_str

    def render_template(self, template):
        """
        Return a div of class col-md-<width>
        """
        return "<div class='col-md-{0}'>{1}</div>".format(self.width, self.html_str)


class TableMappingWidget(deform.widget.MappingWidget):
    __doc__ = '\n    A custom widget rendering a mapping as a table\n\n    :param cols: number of columns we want\n    '
    default_cols = 3
    num_cols = 12
    template = 'grid_mapping.pt'
    item_template = 'grid_mapping_item.pt'
    readonly_template = 'grid_mapping.pt'
    readonly_item_template = 'grid_mapping_item.pt'

    def childgroup(self, field):
        """
        Return children grouped regarding the grid description
        """
        cols = getattr(self, 'cols', self.default_cols)
        width = self.num_cols / cols
        for child in field.children:
            child.width = width

        res = list(grouper((field.children), cols, fillvalue=None))
        return res


class GridMappingWidget(TableMappingWidget):
    __doc__ = '\n    A custom mapping widget rendering it as a grid\n\n    :param tuple grid: A matrix describing the grid we want. The matrix should\n    be composed of two dimensionnal vectors (width, filled) where filled is a\n    boolean.\n\n    :param tuple named_grid: A matrix describing the grid we want. The matrix\n    should be composed of two dimensionnal vectors (name, width).\n\n\n\n    .. code-block:: python\n\n        class CompanyMainInformations(colander.MappingSchema):\n            title = colander.SchemaNode(\n                colander.String(),\n                title=u\'Nom entreprise\',\n            )\n            address = colander.SchemaNode(\n                colander.String(),\n                title=u\'Adresse\',\n                width="5",\n            )\n            lon_coord = colander.SchemaNode(\n                colander.Float(),\n                title=u"Longitude",\n            )\n            lat_coord = colander.SchemaNode(\n                colander.Float(),\n                title=u"Latitude",\n            )\n\n        GRID = (\n            ((3, True), ),\n            ((6, True), (2, False), (2, True), (2, True)),\n            )\n\n        class CompanySchema(colander.Schema):\n            tab = CompanyMainInformations(\n                widget=GridMappingWidget(grid=GRID)\n            )\n\n        NAMED_GRID = (\n            ((\'title\', 3), ),\n            ((\'address\', 6), (None, 2), (\'lon_coord\', 2), (\'lat_coord\', 2)),\n            )\n\n        class CompanySchema(colander.Schema):\n            tab = CompanyMainInformations(\n                widget=GridMappingWidget(named_grid=NAMED_GRID)\n                )\n\n\n    Here, in both cases, we\'ve got a two lines grid with 1 element on the first\n    line and 3 on the second one. The second element of the second line will be\n    a void cell of 2 units width\n\n    You can also pass StaticWidget instances in both cases\n    This way static html datas can be inserted in forms\n\n    .. code-block:: python\n\n        NAMED_GRID = (\n            ((\'title\', 3), ),\n            (\n                (StaticWidget("<div>Hello</div>"), 6),\n                (None, 2), (\'lon_coord\', 2), (\'lat_coord\', 2)\n             ),\n        )\n\n        GRID = (\n            ((3, True), ),\n            (\n                (6, StaticWidget("<div>Hello</div>")),\n                (2, False), (2, True), (2, True)\n            ),\n        )\n\n    '
    num_cols = 12

    def _childgroup(self, children, grid):
        """
        Stores the children in a list following the grid's structure

        :param children: list of fields

        :param grid: a list of list corresponding of the layout to apply to the
        given children
        """
        result = []
        index = 0
        hidden_fields = []
        for row in grid:
            child_row = []
            width_sum = 0
            for width, filled in row:
                width_sum += width
                if width_sum > self.num_cols:
                    warnings.warn('It seems your grid configuration overlaps the bootstrap layout columns number. One of your lines is larger than {0}. You can increase this column number by compiling bootstrap css with lessc.'.format(self.num_cols))
                elif isinstance(filled, StaticWidget):
                    child = filled
                    child.width = width
                else:
                    if filled:
                        try:
                            child = children[index]
                        except IndexError:
                            warnings.warn("The grid items number doesn't match the number of children of our mapping widget")
                            break

                        if type(child.widget) == deform.widget.HiddenWidget:
                            hidden_fields.append(child)
                            index += 1
                            try:
                                child = children[index]
                            except IndexError:
                                warnings.warn("The grid items number doesn't match the number of children of our mapping widget")
                                break

                        child.width = width
                        index += 1
                    else:
                        child = VoidWidget(width)
                child_row.append(child)

            if child_row != []:
                result.append(child_row)

        if index <= len(children):
            result.append(children[index:])
        if hidden_fields != []:
            result.append(hidden_fields)
        return result

    @staticmethod
    def _dict_children(children):
        """
        Format the given children list as a dict
        """
        return dict(((elem.name, elem) for elem in children))

    def _childgroup_by_name(self, children, grid):
        """
        Group the children ordering them by name
        """
        children = self._dict_children(children)
        result = []
        for row in grid:
            child_row = []
            row_is_void = True
            width_sum = 0
            for name, width in row:
                width_sum += width
                if width_sum > self.num_cols:
                    warnings.warn('It seems your grid configuration overlaps the bootstrap layout columns number. One of your lines is larger than {0}. You can increase this column number by compiling bootstrap css with lessc.'.format(self.num_cols))
                elif isinstance(name, StaticWidget):
                    child = name
                    child.width = width
                    row_is_void = False
                else:
                    if name is not None:
                        try:
                            child = children.pop(name)
                            row_is_void = False
                        except KeyError:
                            warnings.warn('No node {0} found'.format(name))
                            child = VoidWidget(width)

                        child.width = width
                    else:
                        child = VoidWidget(width)
                child_row.append(child)

            if not row_is_void:
                result.append(child_row)

        for value in children.values():
            result.append([value])

        return result

    def childgroup(self, field):
        """
        Return a list of fields stored by row regarding the configured grid

        :param field: The original field this widget is attached to
        """
        grid = getattr(self, 'grid', None)
        named_grid = getattr(self, 'named_grid', None)
        if grid is not None:
            childgroup = self._childgroup(field.children, grid)
        else:
            if named_grid is not None:
                childgroup = self._childgroup_by_name(field.children, named_grid)
            else:
                raise AttributeError('Missing the grid or named_grid argument')
        return childgroup


class AccordionMappingWidget(GridMappingWidget):
    __doc__ = "\n    Render a mapping as an accordion and places inner fields in a grid\n\n    .. code-block:: python\n\n        class Mapping(colander.MappingSchema):\n            field = colander.SchemaNode(...)\n\n        class Schema(colander.Schema):\n            mymapping = Mapping(title=u'The accordion header',\n                widget = AccordionMappingWidget(grid=GRID)\n                )\n\n    you'll need to set the bootstrap_form_style to 'form-grid'\n\n    Form(schema=Schema(), bootstrap_form_style='form-grid')\n    "
    template = 'accordion_mapping.pt'
    readonly_template = 'accordion_mapping.pt'

    @property
    def tag_id(self):
        """
        Return a unique tag id for this mapping
        """
        if not hasattr(self, '_tag_id'):
            self._tag_id = random_tag_id()
        return self._tag_id


class TableFormWidget(TableMappingWidget):
    template = 'grid_form.pt'
    readonly_template = 'grid_form.pt'


class GridFormWidget(GridMappingWidget):
    __doc__ = '\n    Render a form as a grid\n\n    .. code-block:: python\n\n        class CompanyMainInformations(colander.MappingSchema):\n            title = colander.SchemaNode(\n                colander.String(),\n                title=u\'Nom entreprise\',\n            )\n            address = colander.SchemaNode(\n                colander.String(),\n                title=u\'Adresse\',\n                width="5",\n            )\n\n        LAYOUT = (((2, True), (2, False), (2, True),),)\n\n        schema = CompanyMainInformations()\n        form = Form(schema)\n        form.widget = GridFormWidget(grid=LAYOUT)\n\n    .. warning::\n\n        Here you need to set the widget after you initialize the form object\n\n    '
    template = 'grid_form.pt'
    readonly_template = 'grid_form.pt'


class AccordionFormWidget(GridFormWidget):
    __doc__ = '\n    AccordionFormWidget is supposed to be combined with colanderalchemy\n\n    The way it works::\n\n        In your SqlAlchemy models, enter the __colanderalchemy__ key under the\n        info attribute.  All columns of a single model can have a section key.\n        If so, an accordion will contain all columns under the same section key\n\n        If you want each accordion to be rendered as a grid, you can optionnaly\n        pass a grids or named_grids argument that should be a dict :\n            {<section_name>: <associated_grid_object>}\n\n        The associated_grid_object should be in the same format as for the\n        GridMappingWidget\n\n\n    .. code-block:: python\n\n        class Model(DBBASE):\n            coordonnees_emergency_name = Column(\n                String(50),\n                info={\n                    \'colanderalchemy\':{\n                        \'title\': u"Contact urgent : Nom",\n                        \'section\': u\'Coordonnées\',\n                    }\n                }\n            )\n            coordonnees_emergency_phone = Column(\n                String(14),\n                info={\n                    \'colanderalchemy\':{\n                        \'title\': u\'Contact urgent : Téléphone\',\n                        \'section\': u\'Coordonnées\',\n                    }\n                }\n            )\n\n            # STATUT\n            statut_social_status_id = Column(\n                ForeignKey(\'social_status_option.id\'),\n                info={\n                    \'colanderalchemy\':\n                    {\n                        \'title\': u"Statut social à l\'entrée",\n                        \'section\': u\'Statut\',\n                        \'widget\': get_deferred_select(SocialStatusOption),\n                    }\n                }\n            )\n\n        schema = SQLAlchemySchemaNode(Model)\n        form = Form(schema)\n        form.widget = AccordionFormWidget()\n    '
    num_cols = 12
    template = 'accordion_form.pt'
    readonly_template = 'accordion_form.pt'
    default_item_template = deform.widget.MappingWidget.item_template

    def accordions(self, form):
        """
        return the chlidren of the given form in a dict allowing to render them
        in accordions with a grid layout
        :param form: the form object
        """
        fixed = []
        accordions = OrderedDict()
        for child in form.children:
            section = getattr(child.schema, 'section', '')
            if not section:
                fixed.append(child)
            else:
                if section not in accordions.keys():
                    accordions[section] = {'tag_id':random_tag_id(),  'children':[],  'name':section, 
                     'error':False}
                if child.error:
                    accordions[section]['error'] = True
                accordions[section]['children'].append(child)

        grids = getattr(self, 'grids', {})
        named_grids = getattr(self, 'named_grids', {})
        if grids != {}:
            method = self._childgroup
        else:
            if named_grids != {}:
                method = self._childgroup_by_name
                grids = named_grids
            else:
                warnings.warn('Missing both grids and named_grids argument')
        for accordion in accordions.values():
            name = accordion['name']
            grid = grids.get(name)
            if grid is not None:
                children = accordion.pop('children')
                accordion['rows'] = method(children, grid)

        return (
         fixed, accordions)


class LocalizationWidget(deform.widget.TextInputWidget):
    __doc__ = "\n    A widget with a link for configuring localization picking it from a map\n    A link will be provided, by clicking on it, we do some fancy html\n    manipulation to replace the fields and have a pretty layout\n\n    e.g:\n\n        >>> widget = LocalizationWidget(\n        ...     lat_field_name='lat_coord',\n        ...     lon_field_name='lon_coord'\n        ... )\n        >>> class Schema():\n        ...     lat_coord = colander.Schema(colander.Float())\n        ...     lon_coord = colander.Schema(colander.Float(), widget=widget)\n    "
    template = 'localization.pt'
    readonly_template = 'localization.pt'


class HiddenLocalizationWidget(deform.widget.TextInputWidget):
    __doc__ = '\n    A hidden version\n    '
    template = 'hidden_localization.pt'
    readonly_template = 'hidden_localization.pt'


class CustomDateInputWidget(deform.widget.Widget):
    __doc__ = '\n\n    Renders a JQuery UI date picker widget\n    (http://jqueryui.com/demos/datepicker/).  Most useful when the\n    schema node is a ``colander.Date`` object.\n    alt Tag is used to allow full customization of the displayed input\n\n    **Attributes/Arguments**\n\n    size\n        The size, in columns, of the text input field.  Defaults to\n        ``None``, meaning that the ``size`` is not included in the\n        widget output (uses browser default size).\n\n    template\n        The template name used to render the widget.  Default:\n        ``dateinput``.\n\n    options\n        Options for configuring the widget (eg: date format)\n\n    readonly_template\n        The template name used to render the widget in read-only mode.\n        Default: ``readonly/textinput``.\n    '
    template = 'dateinput.pt'
    readonly_template = 'readonly/textinput.pt'
    size = None
    requirements = (('modernizr', None), ('jqueryui', None), ('custom_dates', None))
    default_options = (('dateFormat', 'dd/mm/yy'), )

    def __init__(self, *args, **kwargs):
        self.options = dict(self.default_options)
        (deform.widget.Widget.__init__)(self, *args, **kwargs)

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (colander.null, None):
            cstruct = ''
        template = readonly and self.readonly_template or self.template
        options = self.options
        options['altFormat'] = 'yy-mm-dd'
        return field.renderer(template, field=field,
          cstruct=cstruct,
          options=(self.options))

    def deserialize(self, field, pstruct):
        date = colander.null
        if pstruct:
            if hasattr(pstruct, 'get'):
                date = pstruct.get('date', colander.null)
                if date == '':
                    date = colander.null
        return date


class CustomDateTimeInputWidget(CustomDateInputWidget):
    __doc__ = "\n    Renders a datetime picker widget.\n\n    The default rendering is as a native HTML5 datetime  input widget,\n    falling back to jQuery UI date picker with a JQuery Timepicker add-on\n    (http://trentrichardson.com/examples/timepicker/).\n\n    Used for ``colander.DateTime`` schema nodes.\n\n    **Attributes/Arguments**\n\n    options\n        A dictionary of options that's passed to the datetimepicker.\n\n    size\n        The size, in columns, of the text input field.  Defaults to\n        ``None``, meaning that the ``size`` is not included in the\n        widget output (uses browser default size).\n\n    style\n        A string that will be placed literally in a ``style`` attribute on\n        the text input tag.  For example, 'width:150px;'.  Default: ``None``,\n        meaning no style attribute will be added to the input tag.\n\n    template\n        The template name used to render the widget.  Default:\n        ``dateinput``.\n\n    readonly_template\n        The template name used to render the widget in read-only mode.\n        Default: ``readonly/textinput``.\n    "
    template = 'datetimeinput.pt'
    readonly_template = 'readonly/textinput.pt'
    type_name = 'datetime'
    size = None
    style = None
    requirements = (('modernizr', None), ('jqueryui', None), ('datetimepicker', None),
                    ('custom_dates', None))
    default_options = (('dateFormat', 'dd/mm/yy'), ('timeFormat', 'HH:mm'), ('separator', ' '))

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (colander.null, None):
            cstruct = ''
        if cstruct:
            parsed = colander.iso8601.ISO8601_REGEX.match(cstruct)
            if parsed:
                timezone = parsed.groupdict()['timezone']
                if timezone:
                    if cstruct.endswith(timezone):
                        cstruct = cstruct[:-len(timezone)]
        options = self.options
        options['altFormat'] = 'yy-mm-dd'
        separator = options.get('separator', ' ')
        cstruct = separator.join(cstruct.split('T'))
        options = json.dumps(options)
        template = readonly and self.readonly_template or self.template
        return field.renderer(template,
          field=field,
          cstruct=cstruct,
          options=options)

    def deserialize(self, field, pstruct):
        datetime_data = ''
        if pstruct:
            if hasattr(pstruct, 'get'):
                datetime_data = pstruct.get('datetime', colander.null)
        if datetime_data in ('', colander.null):
            return colander.null
        return datetime_data.replace(self.options['separator'], 'T')


class RadioChoiceToggleWidget(deform.widget.RadioChoiceWidget):
    __doc__ = '\n    Renders a sequence of ``<input type="radio"/>`` buttons based on a\n    predefined set of values.\n\n    **Attributes/Arguments**\n\n    values\n        A sequence of three-tuples (the first value must be of type\n        string, unicode or integer, the second value must be string or\n        unicode) indicating allowable, displayed values, e.g. ``(\n        (\'true\', \'True\', \'otherformelement1\'), (\'false\', \'False\',\n        \'otherformelement2\') )``.\n        The first element is the value that will be submitted by the form\n        The second is the display value.\n        The third element in the tuple is the colande name of the form item that\n        will be shown when the radio is checked if the void string \'\' is\n        provided, only all other elements will be hidden.\n\n    template\n        The template name used to render the widget.  Default:\n        ``radio_choice_toggle``.\n\n    null_value\n        The value used to replace the ``colander.null`` value when it\n        is passed to the ``serialize`` or ``deserialize`` method.\n        Default: the empty string.\n\n    inline\n        If true, choices will be rendered on a single line.\n        Otherwise choices will be rendered one per line.\n        Default: false.\n    '
    template = 'radio_choice_toggle.pt'
    readonly_template = 'radio_choice_toggle.pt'
    values = ()
    requirements = (('radio_choice_toggle', None), )

    def serialize(self, field, cstruct, **kw):
        if cstruct in (colander.null, None):
            cstruct = self.null_value
        readonly = kw.get('readonly', self.readonly)
        values = kw.get('values', self.values)
        template = readonly and self.readonly_template or self.template
        kw['values'] = values
        tmpl_values = self.get_template_values(field, cstruct, kw)
        return (field.renderer)(template, **tmpl_values)


class CheckboxToggleWidget(deform.widget.CheckboxWidget):
    __doc__ = '\n    Renders an ``<input type="checkbox"/>`` widget.\n\n    **Attributes/Arguments**\n\n    true_val\n        The value which should be returned during deserialization if\n        the box is checked.  Default: ``true``.\n\n    false_val\n        The value which should be returned during deserialization if\n        the box was left unchecked.  Default: ``false``.\n\n    template\n        The template name used to render the widget.  Default:\n        ``checkbox``.\n\n    readonly_template\n        The template name used to render the widget in read-only mode.\n        Default: ``readonly/checkbox``.\n\n    true_target\n\n        The item that should be displayed on true value\n\n    false_target\n\n        The item that should be displayed on false value\n    '
    template = 'checkbox_toggle.pt'
    readonly_template = 'checkbox_toggle.pt'
    true_val = 'true'
    false_val = 'false'
    true_target = ''
    false_target = ''
    requirements = (('checkbox_toggle', None), )

    def serialize(self, field, cstruct, **kw):
        readonly = kw.get('readonly', self.readonly)
        template = readonly and self.readonly_template or self.template
        values = self.get_template_values(field, cstruct, kw)
        return (field.renderer)(template, **values)


library = fanstatic.Library('deform_extensions', 'resources')
custom_dates = fanstatic.Resource(library,
  'date.js',
  depends=[
 timepicker_js, jqueryui_bootstrap_theme])
radio_choice_toggle = fanstatic.Resource(library,
  'radio_choice_toggle.js',
  depends=[
 jquery, underscore])
checkbox_toggle = fanstatic.Resource(library,
  'checkbox_toggle.js',
  depends=[
 jquery, underscore])

def add_resources_to_registry():
    """
    Add resources to the deform registry
    """
    from deform.widget import default_resource_registry
    default_resource_registry.set_js_resources('jqueryui', None, None)
    default_resource_registry.set_js_resources('datetimepicker', None, None)
    default_resource_registry.set_js_resources('custom_dates', None, None)
    default_resource_registry.set_js_resources('radio_choice_toggle', None, None)
    default_resource_registry.set_js_resources('checkbox_toggle', None, None)
    from js.deform import resource_mapping
    import js.select2 as select2
    resource_mapping['select2'] = select2
    from js.jquery_timepicker_addon import timepicker
    resource_mapping['datetimepicker'] = timepicker
    resource_mapping['custom_dates'] = custom_dates
    resource_mapping['radio_choice_toggle'] = radio_choice_toggle
    resource_mapping['checkbox_toggle'] = checkbox_toggle


def set_default_widgets():
    """
    Set custom date and datetime input widgets for a better user-experience
    """
    defaults[colander.DateTime] = CustomDateTimeInputWidget
    defaults[colander.Date] = CustomDateInputWidget


def add_template_path():
    """
    Set the template path in the renderer's lookup informations
    """
    deform.renderer.configure_zpt_renderer(['deform_extensions:templates'])


def includeme(config):
    add_resources_to_registry()
    set_default_widgets()
    add_template_path()