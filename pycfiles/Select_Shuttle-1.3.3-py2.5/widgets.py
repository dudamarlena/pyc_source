# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/selectshuttle/widgets.py
# Compiled at: 2008-12-14 17:45:01
import pkg_resources
from turbogears.controllers import expose
from turbogears import widgets
from turbogears.validators import Int, FancyValidator, Schema
from turbogears.widgets import JSLink, WidgetDescription, register_static_directory
__all__ = [
 'ShuttleValidator',
 'SelectShuttle']
pkg_name = 'selectshuttle'
option_transfer = JSLink(pkg_name, 'OptionTransfer.js')
js_dir = pkg_resources.resource_filename(pkg_name, 'static/javascript')
register_static_directory(pkg_name, js_dir)
css_code = '\n.selectshuttle {\n    width: 100%;\n}\ntable.selectshuttle th {\n    text-align: left;\n}\ntd.selectshuttle-left {\n    text-align: left;\n    width: 45%;\n}\ntd.selectshuttle-middle {\n    text-align: center;\n    valign: middle;\n}\ntd.selectshuttle-right {\n    text-align: left;\n    width: 45%;\n}\ntd.selectshuttle-addlink {\n    text-align: center;\n}\n'
template = '\n<div xmlns:py=\'http://purl.org/kid/ns#\'>\n    <script type="text/javascript">\n    var ${optrans_name} = new OptionTransfer(\'${name}.${available.name}\',\n                                             \'${name}.${selected.name}\');\n    ${optrans_name}.setAutoSort(true);\n    ${optrans_name}.saveNewLeftOptions(\'${name}.available_new\');\n    ${optrans_name}.saveAddedLeftOptions(\'${name}.available_added\');\n    ${optrans_name}.saveRemovedLeftOptions(\'${name}.available_removed\');\n    ${optrans_name}.saveNewRightOptions(\'${name}.selected_new\');\n    ${optrans_name}.saveAddedRightOptions(\'${name}.selected_added\');\n    ${optrans_name}.saveRemovedRightOptions(\'${name}.selected_removed\');\n    </script>\n    ${display_field_for(available_new)}\n    ${display_field_for(available_added)}\n    ${display_field_for(available_removed)}\n    ${display_field_for(selected_new)}\n    ${display_field_for(selected_added)}\n    ${display_field_for(selected_removed)}\n    <table align=\'left\' width=\'100%\' class=\'selectshuttle\'>\n      <thead>\n        <tr>\n          <th class=\'selectshuttle-left\' py:content=\'title_available\'>Left Options</th>\n          <th class=\'selectshuttle-middle\'></th>\n          <th class=\'selectshuttle-right\' py:content=\'title_selected\'>Right Options</th>\n        </tr>\n      </thead>\n      <tbody>\n        <tr>\n          <td class=\'selectshuttle-left\'>${display_field_for(available)}</td>\n          <td class=\'selectshuttle-middle\'>\n            <input type="button"\n                   name="btn_selected"\n                   id="${optrans_name}_btn_selected"\n                   py:attrs="value=btn_to_selected"\n                   onclick="${optrans_name}.transferRight()"\n            /><br /><br />\n            <input type="button"\n                   name="btn_all_selected"\n                   id="${optrans_name}_btn_all_selected"\n                   py:attrs="value=btn_all_selected"\n                   onclick="${optrans_name}.transferAllRight()"\n            /><br /><br />\n            <input type="button"\n                   name="btn_all_available"\n                   id="${optrans_name}_btn_all_available"\n                   py:attrs="value=btn_all_available"\n                  onclick="${optrans_name}.transferAllLeft()"\n            /><br /><br />\n            <input type="button"\n                   name="btn_available"\n                   id="${optrans_name}_btn_available"\n                   py:attrs="value=btn_to_available"\n                   onclick="${optrans_name}.transferLeft()"\n            />\n          </td>\n          <td class=\'selectshuttle-right\'>${display_field_for(selected)}</td>\n        </tr>\n        <tr py:if=\'add_link is not None\'>\n          <td class=\'selectshuttle-addlink\' colspan=\'3\'>\n            <a target="${target}" href="${add_link}">\n                <span py:strip="1" py:if="add_image_src is not None">\n                    <img src="${add_image_src}" border="0" />\n                </span>\n                ${add_text}\n            </a>\n          </td>\n        </tr>\n      </tbody>\n    </table>\n    <script type="text/javascript">\n      var form_reference = document.getElementById(\'${optrans_name}_btn_available\').form;\n      ${optrans_name}.init(form_reference);\n    </script>\n</div>\n'

class ShuttleValidator(Schema):

    def from_python(self, value, state=None):
        return value


class ShuttleParser(FancyValidator):

    def to_python(self, value, state=None):
        if value is None:
            return []
        return map(Int.to_python, filter(bool, value.split(',')))


class SelectShuttle(widgets.CompoundFormField):
    """
    The SelectShuttle widget provides a mechanism for selecting
    multiple values from a list of values by allowing the user
    to move items between two lists.

    On modern browsers you can also double click an item to move it
    from one list to the other.

    After the first "move", all entries will be sorted automatically
    accordingly to its "description" on both lists.

    An optional "add" link, text, image and link target may be
    specified as well to enhance the usability of this widget when
    new options can be added.

    Take a look at the code for SelectShuttleDesc for an example of
    how to use this widget in your code.
    """
    javascript = [
     option_transfer]
    css = [widgets.CSSSource(src=css_code, media='screen')]
    template = template
    member_widgets = [
     'available', 'available_new', 'available_added',
     'available_removed', 'selected', 'selected_new',
     'selected_added', 'selected_removed']
    available = widgets.MultipleSelectField('available', size=10, validator=Int())
    selected = widgets.MultipleSelectField('selected', size=10, validator=Int())
    available_new = widgets.HiddenField('available_new', validator=ShuttleParser())
    available_added = widgets.HiddenField('available_added', validator=ShuttleParser())
    available_removed = widgets.HiddenField('available_removed', validator=ShuttleParser())
    selected_new = widgets.HiddenField('selected_new', validator=ShuttleParser())
    selected_added = widgets.HiddenField('selected_added', validator=ShuttleParser())
    selected_removed = widgets.HiddenField('selected_removed', validator=ShuttleParser())
    params = [
     'title_available', 'title_selected',
     'btn_all_selected', 'btn_all_available',
     'btn_to_selected', 'btn_to_available',
     'available_options',
     'add_link', 'add_text', 'target', 'add_image_src']
    params_doc = {'title_available': 'Header for available options', 
       'title_selected': 'Header for selected options', 
       'btn_all_selected': 'Text to the button that moves all available to selected', 
       'btn_all_available': 'Text to the button that moves all selected to available', 
       'btn_to_selected': 'Text to the button that moves one available option to selected', 
       'btn_to_available': 'Text to the button that moves one selected option to available', 
       'available_options': 'Options to be shown as available', 
       'add_link': 'Hyperlink to some action (e.g. add new options) - optional', 
       'add_text': 'Text to show the user for the add_link - optional', 
       'target': 'Target to open the add_link - optional', 
       'add_image_src': 'Image to show before the add_link text - optional'}
    validator = ShuttleValidator()
    title_available = 'Left'
    title_selected = 'Right'
    btn_to_selected = '>>'
    btn_all_selected = 'All >>'
    btn_all_available = '<< All'
    btn_to_available = '<<'
    available_options = []
    convert = False
    add_link = None
    add_text = 'Add a new option'
    target = ''
    add_image_src = '/tg_static/images/add.png'

    def update_params(self, params):
        super(SelectShuttle, self).update_params(params)
        params['optrans_name'] = optrans_name = 'optrans_' + params['name'].replace('.', '_')
        value = params.get('value', None) or {}
        available_opts = params['available_options']
        selected_opts = value.get('selected', [])
        redisplayed_opts = value.get('selected_new', None)
        if redisplayed_opts is not None:
            redisplayed_opts = ShuttleParser.to_python(redisplayed_opts)

            def get_name(find_id):
                for (id, name) in available_opts:
                    if find_id == id:
                        return name

            selected_opts = [ (id, get_name(id)) for id in redisplayed_opts ]
        not_selected = lambda x: x not in selected_opts
        available_opts = filter(not_selected, available_opts)
        widgets_params = params['member_widgets_params']
        widgets_params.update(options=dict(available=available_opts, selected=selected_opts), attrs=dict(available=dict(ondblclick=optrans_name + '.transferRight()'), selected=dict(ondblclick=optrans_name + '.transferLeft()')))
        params['member_widgets_params'] = widgets_params
        params['params_for'] = lambda f: self.params_for(f, **widgets_params)
        return


class SelectShuttleDesc(WidgetDescription):
    name = 'Select Shuttle'
    full_class_name = 'selectshuttle.SelectShuttle'
    form_name = 'remote_form_for_shuttle'
    template = '\n    <div>\n        <form action="%s/post_data" name="%s" method="POST">\n            ${for_widget.display()}<br />\n            <input type="submit" value="Submit" />\n        </form>\n    </div>\n    ' % (full_class_name, form_name)
    for_widget = SelectShuttle(name='select_shuttle_demo', label='The shuttle', title_available='Available options', title_selected='Selected options', available_options=[ (i, 'Option %d' % i) for i in xrange(5) ], default=dict(selected=[ (i, 'Option %d' % i) for i in xrange(3) ]))
    validating_form = widgets.Form(fields=[for_widget])
    [
     expose()]

    def post_data(self, **kw):
        kw = self.validating_form.validate(kw)
        return '<b>Coerced data:</b><br />%s<br /><br /> ' % kw