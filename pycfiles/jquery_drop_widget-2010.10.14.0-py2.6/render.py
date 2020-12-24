# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jquery_drop_widget/render.py
# Compiled at: 2010-10-14 14:04:21
"""
Render our jQuery Drop Widgets
"""
import time, re, os, pygments, pygments.lexers, pygments.formatters
JS_INCLUDE_DEFAULT = []
CSS_INCLUDE_DEFAULT = []

def MakeIdSafe(text, safe_char='-'):
    """Make text safe to be inserted into an HTML tag ID field."""
    unsafe_chars = '\',."<>!@#$%^&*(){}[]=+_`~;: \n'
    for char in unsafe_chars:
        if char in text:
            text = text.replace(char, safe_char)

    return text


class Output:

    def __init__(self, js_include=None, css_include=None):
        self.body = ''
        self.js_include = []
        for include in JS_INCLUDE_DEFAULT:
            if include not in self.js_include:
                self.js_include.append(include)

        if js_include:
            for include in js_include:
                if include not in self.js_include:
                    self.js_include.append(include)

        self.css_include = []
        for include in CSS_INCLUDE_DEFAULT:
            if include not in self.css_include:
                self.css_include.append(include)

        if css_include:
            for include in css_include:
                if include not in self.css_include:
                    self.css_include.append(include)

        self.js = []
        self.cookies = {}

    def __repr__(self):
        output = self.body
        if self.js:
            output += '\n<script>\n'
            for js in self.js:
                output += js + '\n'

            output += '\n</script>\n'
        return output

    def __iadd__(self, text):
        """In place add, to our self.body."""
        self.body += str(text)
        return self


def Value(id, content, options=None, data=None, cookies=None, headers=None):
    output = Output()
    output += '<div id="%s">%s</div>\n' % (id, content)
    return output


def Button_Link(id, content, options=None, data=None, cookies=None, headers=None):
    """Button: Made out of an A HREF tag."""
    output = Output()
    output += '<span id="%s"><a href="#" id="%s-link" class="ui-state-default ui-corner-all" style="padding: .4em 1em .4em 20px;text-decoration: none;position: relative;"><span class="ui-icon ui-icon-newwin" style="margin: 0 5px 0 0;position: absolute;left: .2em;top: 50%%;margin-top: -8px;"></span>%s</a></span>' % (id, id, content)
    if options and 'click' in options:
        func = options['click']
    else:
        func = ''
    click = "$('#%s-link').unbind('click');$('#%s-link').click(function(){%s});" % (id, id, func)
    output.js.append(click)
    return output


def Button(id, content, options=None, data=None, cookies=None, headers=None):
    """Button: Made out of a BUTTON tag."""
    output = Output()
    output += '<button id="%s" class="fg-button ui-state-default ui-corner-all" type="button">%s</button>' % (id, content)
    if options and 'click' in options:
        func = options['click']
    else:
        func = ''
    button = '\n    //all hover and click logic for buttons\n    $("#%s")\n    .hover(\n      function(){ \n        $(this).addClass("ui-state-hover"); \n      },\n      function(){ \n        $(this).removeClass("ui-state-hover"); \n      }\n    )\n    .click(function(){\n      %s\n    })\n    .mousedown(function(){\n        $(this).parents(\'.fg-buttonset-single:first\').find(".fg-button.ui-state-active").removeClass("ui-state-active");\n        if( $(this).is(\'.ui-state-active.fg-button-toggleable, .fg-buttonset-multi .ui-state-active\') ){ $(this).removeClass("ui-state-active"); }\n        else { $(this).addClass("ui-state-active"); }\t\n    })\n    .mouseup(function(){\n      if(! $(this).is(\'.fg-button-toggleable, .fg-buttonset-single .fg-button,  .fg-buttonset-multi .fg-button\') ){\n        $(this).removeClass("ui-state-active");\n      }\n    });\n  ' % (id, func)
    output.js.append(button)
    return output


def Input(id, content, options=None, data=None, cookies=None, headers=None):
    """Input to RPC"""
    output = Output()
    if options == None:
        options = {}
    output += '<span id="div_%s">\n' % id
    button_options = {'click': "RPC('%s', {'text':$('#%s').val()}); $('#%s').val(''); return false;" % (options['rpc'], id, id)}
    output = str(Button('input_button_%s' % id, options.get('title', 'Enter'), button_options))
    size = options.get('size', 20)
    output += '<input type="text" id="%s" size="%s" maxlength="120" value="%s">' % (id, size, content)
    output += '</span>\n'
    output += "\n  <script>\n    // Enters submits comments on the wall\n    $('#%s').keypress(function(event) {\n      if (event.keyCode == '13') {\n         //event.preventDefault();\n         RPC('%s', {'text':$('#%s').val()});\n         $('#%s').val('');\n       }\n    });\n  </script>\n  " % (id, options['rpc'], id, id)
    return output


def Tabs(id, content_dict, options=None, data=None, cookies=None, headers=None):
    """content is dict of strings, the strings match the tab names.
  
  Order is options['tabs'] list, which lists the tabs in order.  If not present
  tabs will be displayed in alphabetical order from content_dict.
  """
    output = Output()
    if options and 'tabs' in options:
        order = options['tabs']
    else:
        order = content_dict.keys()
        order.sort()
    output += '<div id="%s">\n' % id
    output += '<ul>\n'
    for count in range(0, len(order)):
        if options and 'labels' in options and options['labels'] and order[count] in options['labels']:
            output += '<li><a href="#%s-%d">%s</a></li>\n' % (id, count, options['labels'][order[count]])
        else:
            output += '<li><a href="#%s-%d">%s</a></li>\n' % (id, count, order[count])

    output += '</ul>\n'
    for count in range(0, len(order)):
        output += '<div id="%s-%d">\n' % (id, count)
        output += str(content_dict[order[count]])
        output += '</div>\n'

    output += '</div>\n'
    selected_tab = 'tabs[%s]' % id
    print selected_tab
    if not options or 'selected' not in options or selected_tab not in options['selected']:
        selected = 0
    else:
        selected = int(options['selected'][selected_tab])
    output.js.append("$('#%s').tabs('destroy'); $('#%s').tabs({selected: $.cookie('tab_%s')||0});" % (id, id, id))
    output.js.append('tabs["%s"] = true;' % id)
    return output


def Table(id, content_list, options=None, data=None, cookies=None, headers=None):
    """content is list of dicts."""
    output = Output()
    if options and 'order' in options:
        headers = options['order']
    elif content_list:
        headers = content_list[0].keys()
        headers.sort()
    else:
        headers = []
    if options and 'width' in options:
        width = 'width:%s;' % options['width']
    else:
        width = ''
    output += '\n  <span id="%s"><table class="ui-widget ui-widget-content" style="%s">\n    <thead>\n      <tr class="ui-widget-header ">\n  ' % (id, width)
    for header in headers:
        if options and 'labels' in options and header in options['labels']:
            output += '<th>%s</th>\n' % options['labels'][header]
        else:
            output += '<th>%s</th>\n' % header

    output += '\n      </tr>\n    </thead>\n    <tbody id="processes_body">\n  '
    for item in content_list:
        output += '<tr>\n'
        for header in headers:
            output += '<td>%s</td>\n' % item[header]

        output += '</tr>\n'

    output += '\n    </tbody>\n  </table></span>\n  '
    return output


def PowerTable(id, content_list, options=None, data=None, cookies=None, headers=None):
    """TODO(g): Retire this stupid name, and use the jQuery Plugin Author's name."""
    return DataTable(id, content_list, options=options, data=data, cookies=cookies, headers=headers)


def DataTable(id, content_list, options=None, data=None, cookies=None, headers=None):
    """content is a list of dicts.  Has sortable fields, filtering, pagination, scrolling.
  
  TODO(g): Credit all jQuery Plugin authors, in docstrings, and also in a
      credits list, with URLs to the sites so new versions can be attained.
  TODO(g): Come up with a packaging design to share these things so they are
      easy to segment and include (and try to get it accepted by jQuery people?)
  """
    output = Output()
    if options and 'order' in options:
        headers = options['order']
    elif content_list:
        try:
            headers = content_list[0].keys()
            headers.sort()
        except KeyError, e:
            headers = []

    else:
        headers = []
    if options and 'width' in options:
        width = 'width:%s;' % options['width']
    else:
        width = 'width:100%;'
    if options and 'height' in options:
        height = '"sScrollY": "%s"' % options['height']
    else:
        height = '"sScrollY": "200px"'
    data_tables_id = '%s__dt' % id
    output += '\n  <div id="%s" style="%s"><table id="%s" class="ui-widget ui-widget-content" style="%s">\n    <thead class="ui-widget-header">\n      <tr>\n  ' % (id, width, data_tables_id, width)
    for header in headers:
        if options and 'labels' in options and header in options['labels']:
            output += '<th>%s</th>\n' % options['labels'][header]
        else:
            output += '<th>%s</th>\n' % header

    output += '\n      </tr>\n    </thead>\n    <tbody id="%s_body" class="ui-widget-content">\n  ' % id
    for item in content_list:
        output += '<tr>\n'
        for header in headers:
            if header in item:
                output += '<td class="%s">%s</td>\n' % (header, item[header])
            else:
                output += '<td>&nbsp;</td>\n'

        output += '</tr>\n'

    output += '\n    </tbody>\n  </table></div>\n  '
    dt_options = ''
    if options and 'sort' in options:
        dt_options += ', "aaSorting": [%s] ' % str(options['sort'])
    data_table_js = '%s = $(\'#%s\').dataTable( {\n  "bPaginate": false,\n  "bDestroy": true,\n  //"bScrollCollapse": true,\n  "bAutoWidth": false,\n  "bJQueryUI": true,\n  %s\n  %s\n});\n' % (data_tables_id, data_tables_id, height, dt_options)
    output.js.append(data_table_js)
    return output


def Image(id, content, options=None, data=None, cookies=None, headers=None):
    """Content is the IMG SRC value."""
    output = Output()
    output += '<img id="%s" class="reload_90" src="%s?timestamp=%s">' % (id, content, int(time.time()))
    return output


def TypeFormat(text):
    text = str(text)
    if text.startswith('<type '):
        text = text[6:-1]
    text = text.replace('<', '&lt;').replace('>', '&gt;')
    if text.startswith("'") and text.endswith("'"):
        text = text[1:-1]
    return text


MAX_VALUE_STR_LENGHT = 80

def _GetTreeItems(data, id_prefix='', parent=None):
    """Returns a list of items (dicts), which have parents listed."""
    items = []
    if type(data) == dict:
        for key in data:
            item = {}
            item['key'] = key
            item['id'] = MakeIdSafe('%s_%s' % (id_prefix, key))
            item['kind'] = TypeFormat(type(data[key]))
            if type(data[key]) in (dict, list, tuple):
                item['icon'] = 'folder'
            else:
                item['icon'] = 'file'
            item['value'] = str(data[key])[:MAX_VALUE_STR_LENGHT]
            if parent:
                item['parent'] = parent
            items.append(item)
            if type(data[key]) in (dict, list, tuple):
                children = _GetTreeItems(data[key], item['id'], parent=item['id'])
                items += children

    elif type(data) in (list, tuple):
        for count in range(0, len(data)):
            value = data[count]
            item = {}
            item['key'] = count
            item['id'] = MakeIdSafe('%s_%s' % (id_prefix, count))
            item['kind'] = TypeFormat(type(data[count]))
            if type(value) in (dict, list, tuple):
                item['icon'] = 'folder'
            else:
                item['icon'] = 'file'
            item['value'] = str(data[count])[:MAX_VALUE_STR_LENGHT]
            if parent:
                item['parent'] = parent
            items.append(item)
            if type(value) in (dict, list, tuple):
                children = _GetTreeItems(value, item['id'], parent=item['id'])
                items += children

    else:
        key = '_'
        item = {}
        item['key'] = key
        item['id'] = MakeIdSafe('%s_%s' % (id_prefix, key))
        item['kind'] = TypeFormat(type(data))
        item['value'] = str(data)[:MAX_VALUE_STR_LENGHT]
        if parent:
            item['parent'] = parent
        items.append(item)
    return items


def TableTree(id, content, options=None, data=None, cookies=None, headers=None):
    """content is dict OR list (containing dicts, to be useful)"""
    output = Output()
    tree_items = _GetTreeItems(content)
    output += '\n<table id="%s" class="ui-widget ui-widget-content">\n  <thead class="ui-widget-header">\n    <tr>\n      <th>Key</th>\n      <th>Kind</th>\n      <th>Value</th>\n    </tr>\n  </thead>\n  <tbody class="ui-widget-content">\n  ' % id
    for item in tree_items:
        item_id = item['id']
        item_child = ''
        if 'parent' in item:
            item_child = 'class="child-of-%s"' % item['parent']
        icon = item.get('icon', 'file')
        key = item['key']
        kind = item['kind']
        value = item['value']
        output += '\n    <tr id="%s" %s>\n      <td class="initial"><span class="%s">%s</span></td>\n      <td>%s</td>\n      <td>%s</td>\n    </tr>\n    ' % (item_id, item_child, icon, key, kind, value)

    output += '  </tbody>\n</table>\n  '
    output.js.append('$("#%s").treeTable();' % id)
    return output


def DictTableTree(id, content, options=None, data=None, cookies=None, headers=None):
    """Returns a Tree Table of a dictionary or list, showing the type and value
  for each.
  
  content is dict OR list (containing dicts, to be useful)
  """
    output = Output()
    tree_items = _GetTreeItems(content)
    output += '\n<table id="%s" class="ui-widget ui-widget-content">\n  <thead class="ui-widget-header">\n    <tr>\n      <th>Key</th>\n      <th>Type</th>\n      <th>Value</th>\n    </tr>\n  </thead>\n  <tbody class="ui-widget-content">\n  ' % id
    for item in tree_items:
        item_id = item['id']
        item_child = ''
        if 'parent' in item:
            item_child = 'class="child-of-%s"' % item['parent']
        icon = item.get('icon', 'file')
        key = item['key']
        kind = item['kind']
        value = item['value']
        output += '\n    <tr id="%s" %s>\n      <td class="initial"><span class="%s">%s</span></td>\n      <td>%s</td>\n      <td>%s</td>\n    </tr>\n    ' % (item_id, item_child, icon, key, kind, value)

    output += '  </tbody>\n</table>\n  '
    output.js.append('$("#%s").treeTable();' % id)
    return output


def Accordion(id, content_list, options=None, data=None, cookies=None, headers=None):
    """content_list is list of tuples (string,string): (title, content)"""
    output = Output()
    if options == None:
        options = {}
    output += '<div id="%s" class="accordion">\n' % id
    for count in range(0, len(content_list)):
        content = content_list[count]
        if 'labels' in options:
            output += '<h3><a href="#">%s</a></h3>\n' % options['labels'][count]
        else:
            output += '<h3><a href="#">%s</a></h3>\n' % count
        output += '<div>\n'
        output += str(content)
        output += '</div>\n'

    output += '</div>\n'
    output.js.append("$('#%s').accordion('destroy'); $('#%s').accordion({fillSpace:true});" % (id, id))
    return output


def PopUp(id, content, options=None, data=None, cookies=None, headers=None):
    output = Output(js_include=['js/jquery.BubblePopup-1.1.min.js'])
    output += '\n  <script>\n  $("#%s").SetBubblePopup({\n    //bubbleAlign: \'center\',\n    //distanceFromTarget: 450,\n    //hideTail: true,\n    innerHtml: \'%s\'\n  });\n  </script>\n  ' % (id, content)
    return output


def Grid(id, content_dict, options=None, data=None, cookies=None, headers=None):
    output = Output()
    return output


def Layout(id, content_dict, options=None, data=None, cookies=None, headers=None):
    output = Output()
    return output


def Calendar(id, content_dict, options=None, data=None, cookies=None, headers=None):
    """content is dict of dates"""
    output = Output()
    return output


def CalendarRange(id, content_dict, options=None, data=None, cookies=None, headers=None):
    """content is dict of dates"""
    output = Output()
    return output


def TimeSelector(id, content, options=None, data=None, cookies=None, headers=None):
    output = Output()
    return output


def Menu(id, content, options=None, data=None, cookies=None, headers=None):
    """Menu"""
    if options == None:
        options = {}
    output = Output()
    if not options or 'label' not in options:
        name = 'UNNAMED'
    else:
        name = options['label']
    output += '\n<a tabindex="0" href="#" class="fg-button fg-button-icon-right ui-widget ui-state-default ui-corner-all" id="%s"><span class="ui-icon ui-icon-triangle-1-s"></span>%s</a>\n<div id="%s_content" class="hidden">\n<ul class="fg-menu">\n' % (id, name, id)
    for item in content:
        output += '<li class="fg-menu"><a href="#">%s</a></li>\n' % item

    output += '\n</ul>\n</div>\n  '
    menu_prep_js = "\n$('.fg-button').hover(\n  function(){ $(this).removeClass('ui-state-default').addClass('ui-state-focus'); },\n  function(){ $(this).removeClass('ui-state-focus').addClass('ui-state-default'); }\n);\n  "
    output.js.append(menu_prep_js)
    menu_js = '\n$(\'#%s\').menu({ \n  content: $(\'#%s\').next().html(), // grab content from this page\n  showSpeed: 400,\n  selectFunction: "%s"\n});\n  ' % (id, id, options.get('function', 'alert'))
    output.js.append(menu_js)
    return output


def MenuVertical(id, content, options=None, data=None, cookies=None, headers=None):
    output = Output()
    return output


def MenuContext(id, content, options=None, data=None, cookies=None, headers=None):
    output = Output()
    return output


def Slider(id, content, options=None, data=None, cookies=None, headers=None):
    output = Output()
    return output


def ThemeRoller(id, content, options=None, data=None, cookies=None, headers=None):
    output = Output()
    output.css_include.append('http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/base/ui.all.css')
    output.js.append("$('#%s').themeswitcher();" % id)
    output += '\n    <script type="text/javascript"\n      src="http://jqueryui.com/themeroller/themeswitchertool/">\n    </script>\n    <div id="%s"></div>\n  ' % id
    return output


def MultiList(id, content, options=None, data=None, cookies=None, headers=None):
    """TODO(g): Change all references to this name, which is the jQuery UI Plugin
      Author's name for the widget.  Add him to credits, and provide URL.
  """
    return ListSelectAndOrder(id, content, options=options, data=data, cookies=cookies, headers=headers)


def ListSelectAndOrder(id, content, options=None, data=None, cookies=None, headers=None):
    """Creates a 2 column list selection.  The left column is the selected list,
  and can also be ordered.  The right column is the total possible list.
  
  Content is a tuple of lists (total_list, selected_list).
  
  Project Demo URL: http://michael.github.com/multiselect
  """
    output = Output()
    output.js_include.append('js/plugins/localisation/jquery.localisation-min.js')
    output.js_include.append('js/plugins/scrollTo/jquery.scrollTo-min.js')
    output.js_include.append('js/ui.multiselect.js')
    output.css_include.append('css/common.css')
    output.css_include.append('css/ui.multiselect.css')
    output.js.append('$("#%s").multiselect();' % id)
    output += '  <select id="%s" class="multiselect" multiple="multiple" name="%s[]">\n' % (id, id)
    (total_list, selected_list) = content
    for item in total_list:
        if item in selected_list:
            output += '    <option value="%s" selected="selected">%s</option>\n' % (item, item)
        else:
            output += '    <option value="%s">%s</option>\n' % (item, item)

    output += '  </select>\n'
    return output


def Dialog(id, content, options=None, data=None, cookies=None, headers=None):
    output = Output()
    if options == None:
        options = {}
    title = options.get('title', 'Dialog')
    width = options.get('width', 600)
    auto_open = options.get('open', True)
    if auto_open:
        auto_open_str = "$('#%s').dialog('open');" % id
    else:
        auto_open_str = ''
    if options.get('modal', False):
        modal = 'true'
    else:
        modal = 'false'
    output += '\n<div id="%s" title="%s">\n%s\n</div>\n  ' % (id, title, content)
    output += '\n  <script>\n  // Destroy it first...\n  $(\'#%s\').dialog(\'destroy\');\n  \n  // Dialog\t\t\t\n  $(\'#%s\').dialog({\n    autoOpen: false,\n    width: %s,\n    modal: %s,\n    buttons: {\n      "Cancel": function() { \n        $(this).dialog("close"); \n      }, \n    }\n  });\n  \n  %s\n  </script>\n  ' % (id, id, width, modal, auto_open_str)
    if auto_open:
        output.js.append("$('#%s').dialog('open');" % id)
    return output


def Dialog_Ok(id, content, options=None, data=None, cookies=None, headers=None):
    """Just like a normal Dialog() box, but this has an OK button, and will
  run a JS function if Ok is clicked.  It is not meant to do anything but
  prompt the usade with a status message (content=HTML string) and then
  call the JS function (in options['function']) if OK is clicked.
  """
    output = Output()
    if options == None:
        options = {}
    title = options.get('title', 'Dialog')
    width = options.get('width', 600)
    auto_open = options.get('open', True)
    if auto_open:
        auto_open_str = "$('#%s').dialog('open');" % id
    else:
        auto_open_str = ''
    if options.get('modal', False):
        modal = 'true'
    else:
        modal = 'false'
    output += '\n<div id="%s" title="%s">\n%s\n</div>\n  ' % (id, title, content)
    output += '\n  <script>\n  // Destroy it first...\n  $(\'#%s\').dialog(\'destroy\');\n  \n  // Dialog\t\t\t\n  $(\'#%s\').dialog({\n    autoOpen: false,\n    width: %s,\n    modal: %s,\n    buttons: {\n      "Ok": function() { \n        %s\n        $(this).dialog("close"); \n      }, \n      "Cancel": function() { \n        $(this).dialog("close"); \n      }, \n    }\n  });\n  \n  %s\n  </script>\n  ' % (id, id, width, modal, options.get('function', ''), auto_open_str)
    if auto_open:
        output.js.append("$('#%s').dialog('open');" % id)
    return output


def FieldSet(id, content, options=None, data=None, cookies=None, headers=None):
    """Renders a form, field sets, and Ajax controls to send RPC to the server.
  
  content: [{'Fieldset Label':[{'input_field_key':{'label':'Field Label', 'default':'Something', 'type':'text'}}]}]
  """
    output = Output()
    if options == None:
        options = {}
    method = options.get('action', '')
    action = options.get('method', 'post')
    output += '\n  <form id="%s" action="%s" method="%s"> \n  ' % (id, action, method)
    fieldset_count = 0
    for fieldset_item in content:
        for fieldset_key in fieldset_item:
            fieldset_count += 1
            if fieldset_count % 2 == 1:
                fieldset_alt = ''
            else:
                fieldset_alt = ' class="alt"'
            output += '\n  <fieldset>\n    <legend><span>%s</span></legend>  \n    <ol>\n      ' % fieldset_key
            for input_item in fieldset_item[fieldset_key]:
                for input_name in input_item:
                    input_data = input_item[input_name]
                    input_id = '%s_%s' % (id, input_name)
                    input_label = input_data.get('label', input_name)
                    input_type = input_data.get('type', 'text')
                    input_default = input_data.get('default', '')
                    input_disabled = input_data.get('disabled', False)
                    if input_type == 'hidden':
                        hidden_text = input_default
                    else:
                        hidden_text = ''
                    if input_disabled:
                        disabled_text = 'disabled="disabled"'
                    else:
                        disabled_text = ''
                    if input_type == 'textarea':
                        cols = input_data.get('cols', 60)
                        rows = input_data.get('rows', 4)
                        size_text = ' cols="%s" rows="%s"' % (cols, rows)
                    elif 'size' in input_data:
                        size_text = 'size="%s"' % input_data['size']
                    else:
                        size_text = ''
                    if 'select_widget' in input_data:
                        select_widget = '<br>%s\n' % input_data['select_widget']
                    else:
                        select_widget = ''
                    if 'info' in input_data:
                        select_widget += '<div style="margin-left: 11em;">%s</div>\n' % input_data['info']
                    if input_type == 'textarea':
                        output += '\n        <li>  \n        <label for="%s">%s:</label>  \n        <textarea id="%s" name="%s" class="%s" type="%s" style="margin-left:11em;" %s %s/>%s</textarea>\n        %s\n        %s\n        </li>\n          ' % (input_name, input_label, id, input_name, input_type, input_type,
                         disabled_text, size_text, input_default, hidden_text, select_widget)
                    elif input_type == 'checkbox':
                        if input_default:
                            checked = 'checked'
                        else:
                            checked = ''
                        output += '\n        <li>  \n        <label for="%s">%s:</label>  \n        <input id="%s" name="%s" class="%s" type="%s" %s %s %s/>\n        %s\n        %s\n        </li>\n          ' % (input_name, input_label, id, input_name, input_type, input_type,
                         checked, disabled_text, size_text, hidden_text, select_widget)
                    elif not input_data.get('hide', False):
                        output += '\n        <li>  \n        <label for="%s">%s:</label>  \n        <input id="%s" name="%s" class="%s" type="%s" value="%s" %s %s/>\n        %s\n        %s\n        </li>\n          ' % (input_name, input_label, id, input_name, input_type, input_type,
                         input_default, disabled_text, size_text, hidden_text, select_widget)
                    else:
                        output += '\n        <input id="%s" name="%s" class="%s" type="%s" value="%s" %s %s/>\n          ' % (id, input_name, input_type, input_type,
                         input_default, disabled_text, size_text)

            output += '\n      </ol>  \n    </fieldset>\n    '

    submit_label = options.get('submit', 'Submit')
    output += '\n  <!-- Local button -->\n  <fieldset class="submit">  \n  <input class="submit" type="submit" value="%s" />  \n  </fieldset>\n  ' % submit_label
    output += '\n</form>\n  '
    rpc_function = options['rpc']
    js_success_function = options['js_function']
    if 'rpc_args' in options:
        data_str = ", 'data':%s" % str(options['rpc_args'])
    else:
        data_str = ''
    output += '\n<script>\n$("#%s").ajaxForm({\n  url: \'rpc/%s\',\n  dataType: \'json\',\n  success: %s\n  %s\n  });\n</script>\n  ' % (id, rpc_function, js_success_function, data_str)
    return output


def CodeHighlight(id, content, options=None, data=None, cookies=None, headers=None):
    """Outputs code highlight.
  
  Args:
    content: string, path to code to highlight
  """
    output = Output()
    if options == None:
        options = {}
    code_type = options.get('code', 'python')
    style = options.get('style', 'vs')
    lexer = pygments.lexers.get_lexer_by_name(code_type, stripall=True)
    formatter = pygments.formatters.HtmlFormatter(linenos=True, style=style)
    output += '<style>%s</style>\n' % formatter.get_style_defs('.highlight')
    highlighted = pygments.highlight(open(content).read(), lexer, formatter)
    output += '%s\n' % highlighted
    return output


def MatchRegexFiles(path_regex):
    """Returns a dictionary of matchs based on the regex and file names.
  
  TODO(g): CWD is critical here.  Duh!
  """
    dirs = {}
    items = os.walk('.')
    for (path, path_dirs, files) in items:
        path = path[2:]
        matched_files = []
        for filename in files:
            filepath = '%s/%s' % (path, filename)
            regex = '^(%s)$' % path_regex
            found = re.findall(regex, filepath)
            if found:
                matched_files.append(filename)

        if matched_files:
            dir_chunks = path.split('/')
            cur_dir = dirs
            for dir_chunk in dir_chunks:
                if dir_chunk not in cur_dir:
                    cur_dir[dir_chunk] = {}
                cur_dir = cur_dir[dir_chunk]

            for matched_file in matched_files:
                cur_dir[matched_file] = '%s/%s' % (path, matched_file)

    return dirs


def FileTableTree(id, content, options=None, data=None, cookies=None, headers=None):
    """Prints a Tree Table for the file system, matched against content regex.
  
  Options input_fieldset and input_name allow specification of an INPUT value
  to fill in, with the selection of this tree item.
  
  TODO(g): Add "rpc" option as well, which will RPC this function.
  TODO(g): Dynamic RPC: "Dynamic:path/to/script.py"
  """
    output = Output()
    if options == None:
        options = {}
    dirs = MatchRegexFiles(content)
    tree_items = _GetTreeItems(dirs)
    output += '\n<table id="%s" class="ui-widget ui-widget-content">\n  <thead class="ui-widget-header">\n    <tr>\n      <th>Path</th>\n    </tr>\n  </thead>\n  <tbody class="ui-widget-content">\n  ' % id
    for item in tree_items:
        item_id = item['id']
        item_child = ''
        if 'parent' in item:
            item_child = 'class="child-of-%s"' % item['parent']
        icon = item.get('icon', 'file')
        key = item['key']
        kind = item['kind']
        value = item['value']
        if 'input_fieldset' in options and 'input_name' in options:
            onClick = 'onClick="$(\'#%s input[name=%s]\').each(function(n,element){$(element).val(\'%s\');});"' % (options['input_fieldset'], options['input_name'], value)
        else:
            onClick = ''
        output += '\n    <tr id="%s" %s>\n      <td class="initial"><span class="%s" %s>%s</span></td>\n    </tr>\n    ' % (item_id, item_child, icon, onClick, key)

    output += '  </tbody>\n</table>\n  '
    output.js.append('$("#%s").treeTable({"initialState":"expanded"});' % id)
    return output


def SelectMenu(id, content, options=None, data=None, cookies=None, headers=None):
    """A select menu, with basic popup style.  Simple.  content=list of strings.
  """
    output = Output()
    if options == None:
        options = {}
    if 'select' in options:
        select = 'onselect="%s"' % options['select']
    else:
        select = ''
    output += '\n    <select name="%s" id="%s" %s>\n  ' % (id, id, select)
    for item in content:
        if item == options.get('selected', None):
            output += '\n        <option value="%s" selected="selected">%s</option>\n      ' % (item, item)
        else:
            output += '\n        <option value="%s">%s</option>\n      ' % (item, item)

    output += '\n    </select>\n  '
    output.js.append("$('#%s').selectmenu('destroy'); $('#%s').selectmenu()" % (id, id))
    return output


def Layout(id, content, options=None, data=None, cookies=None, headers=None):
    """Layout: 5 cells: center, north, south, east, west
  
  Layout is completely automated.  If the key is filled in, the area is created.
  """
    output = Output()
    if options == None:
        options = {}
    output += '\n  <div id="%s" class="layout {layout: {type: \'border\', hgap: 3, vgap: 3}}">\n  ' % id
    if content.get('north', False):
        output += '\n<div class="north">\n%s\n</div>\n' % content['north']
    if content.get('center', False):
        output += '\n<div class="center">\n%s\n</div>\n' % content['center']
    if content.get('west', False):
        output += '\n<div class="west">\n%s\n</div>\n' % content['west']
    if content.get('east', False):
        output += '\n<div class="east">\n%s\n</div>\n' % content['east']
    if content.get('south', False):
        output += '\n<div class="south">\n%s\n</div>\n' % content['south']
    output += '\n  </div>\n  '
    return output