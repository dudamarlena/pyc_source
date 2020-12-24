# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/wysihtml5/widgets.py
# Compiled at: 2014-01-19 03:33:05
from __future__ import unicode_literals
import six
from django.contrib.admin.widgets import AdminTextareaWidget
from django.forms.util import flatatt
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from wysihtml5.conf import settings
from wysihtml5.utils import get_function
render_cmd_icon = {}
render_cmd_dialog = {}

def render_blank(id):
    return b''


def render_createLink_dialog(id):
    return b'<div data-wysihtml5-dialog="createLink" style="display:none">  <label>%(_link_)s:</label>&nbsp;  <input data-wysihtml5-dialog-field="href" value="http://">  <a data-wysihtml5-dialog-action="save" class="button">%(_ok_)s</a>&nbsp;  <a data-wysihtml5-dialog-action="cancel" class="button">%(_cancel_)s</a></div>' % {b'_link_': _(b'Link'), b'_ok_': _(b'Ok'), 
       b'_cancel_': _(b'Cancel')}


def render_insertImage_dialog(id):
    return b'<div data-wysihtml5-dialog="insertImage" style="display:none">  <label>%(_link_)s:</label>&nbsp;  <input data-wysihtml5-dialog-field="src" value="http://">  <a data-wysihtml5-dialog-action="save" class="button">%(_ok_)s</a>&nbsp;  <a data-wysihtml5-dialog-action="cancel" class="button">%(_cancel_)s</a></div>' % {b'_link_': _(b'Image'), b'_ok_': _(b'Ok'), 
       b'_cancel_': _(b'Cancel')}


def render_formatBlockHeader_icon(id):
    return b'    <span data-wysihtml5-command-group="%(command_name)s" title="Format text header" class="heading-selector">      <div>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="h1">H1</span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="h2">H2</span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="h3">H3</span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="h4">H4</span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="h5">H5</span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="h6">H6</span>      </div>    </span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'formatBlockHeader'][b'command_name']}


def render_formatBlockParagraph_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Make a paragraph block" data-wysihtml5-command-value="p" class="command format-block-p"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'formatBlockParagraph'][b'command_name']}


def render_bold_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Make text bold (CTRL + B)" class="command"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'bold'][b'command_name']}


def render_italic_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Make text italic (CTRL + I)" class="command"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'italic'][b'command_name']}


def render_underline_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Underline text (CTRL + U)" class="command"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'underline'][b'command_name']}


def render_justifyLeft_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Paragraph left justified" class="command"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'justifyLeft'][b'command_name']}


def render_justifyCenter_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Paragraph center justified" class="command"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'justifyCenter'][b'command_name']}


def render_justifyRight_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Paragraph right justified" class="command"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'justifyRight'][b'command_name']}


def render_insertOrderedList_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Insert an ordered list" class="command"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'insertOrderedList'][b'command_name']}


def render_insertUnorderedList_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Insert an unordered list" class="command"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'insertUnorderedList'][b'command_name']}


def render_insertImage_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Insert an image" class="command insert-image"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'insertImage'][b'command_name']}


def render_createLink_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Insert a link" class="command create-link"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'createLink'][b'command_name']}


def render_insertHTML_icon(id):
    return b'<span data-wysihtml5-command="%(command_name)s" title="Insert a quote" class="command" data-wysihtml5-command-value="%(command_value)s"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'insertHTML'][b'command_name'], b'command_value': settings.WYSIHTML5_TOOLBAR[b'insertHTML'][b'command_value']}


def render_foreColor_icon(id):
    return b'      <span data-wysihtml5-command-group="%(command_name)s" title="Color the selected text" class="fore-color">      <div>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="silver" unselectable="on"></span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="gray" unselectable="on"></span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="maroon" unselectable="on"></span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="red" unselectable="on"></span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="purple" unselectable="on"></span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="green" unselectable="on"></span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="olive" unselectable="on"></span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="navy" unselectable="on"></span>        <span data-wysihtml5-command="%(command_name)s" data-wysihtml5-command-value="blue" unselectable="on"></span>      </div>    </span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'foreColor'][b'command_name']}


def render_changeView_icon(id):
    return b'<span data-wysihtml5-action="%(command_name)s" title="Show HTML" class="action" unselectable="on"></span>' % {b'command_name': settings.WYSIHTML5_TOOLBAR[b'changeView'][b'command_name']}


class Wysihtml5TextareaWidget(AdminTextareaWidget):

    class Media:
        css = {b'all': ('wysihtml5/css/toolbar.css', )}
        js = ('wysihtml5/js/advanced.js', 'wysihtml5/js/wysihtml5-0.4.0pre.min.js')

    def __init__(self, attrs=None, editor_settings=None, toolbar_settings=None):
        if not attrs:
            attrs = {b'rows': 25}
        else:
            if not attrs.get(b'rows', False):
                attrs.update({b'rows': 25})
            if editor_settings:
                self.editor_settings = editor_settings
            else:
                self.editor_settings = settings.WYSIHTML5_EDITOR
            if toolbar_settings:
                self.toolbar_settings = toolbar_settings
            else:
                self.toolbar_settings = settings.WYSIHTML5_TOOLBAR
            self.render_cmd_icon = {}
            self.render_cmd_dialog = {}
            for k, v in six.iteritems(self.toolbar_settings):
                if v.get(b'active', False):
                    self.render_cmd_icon[k] = v.get(b'render_icon', b'wysihtml5.widgets.render_blank')
                    if v.get(b'render_dialog', False):
                        self.render_cmd_dialog[k] = v[b'render_dialog']
                else:
                    self.render_cmd_icon[k] = b'wysihtml5.widgets.render_blank'
                    if v.get(b'render_dialog', False):
                        self.render_cmd_dialog[k] = b'wysihtml5.widgets.render_blank'

        super(Wysihtml5TextareaWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = b''
        final_attrs = self.build_attrs(attrs, name=name)
        textarea_widget = b'<textarea%s>%s</textarea>' % (
         flatatt(final_attrs),
         conditional_escape(force_text(value)))
        wid = final_attrs.get(b'id', b'unknown')
        toolbar_widget = self.render_toolbar_widget(wid)
        pos = wid.find(b'__prefix__')
        if pos != -1:
            js_widget = self.render_js_delay_widget(wid, pos)
        else:
            js_widget = self.render_js_init_widget(wid)
            return mark_safe(b'<div style="display:inline-block">' + toolbar_widget + textarea_widget + b'</div>' + js_widget)
        return

    def render_toolbar_widget(self, id):
        widget = b'<div id="%(id)s-toolbar" class="wysihtml5-editor-toolbar">  <div class="commands">' % {b'id': id}
        widget += get_function(self.render_cmd_icon[b'formatBlockHeader'])(id)
        widget += get_function(self.render_cmd_icon[b'formatBlockParagraph'])(id)
        widget += get_function(self.render_cmd_icon[b'bold'])(id)
        widget += get_function(self.render_cmd_icon[b'italic'])(id)
        widget += get_function(self.render_cmd_icon[b'underline'])(id)
        widget += get_function(self.render_cmd_icon[b'justifyLeft'])(id)
        widget += get_function(self.render_cmd_icon[b'justifyCenter'])(id)
        widget += get_function(self.render_cmd_icon[b'justifyRight'])(id)
        widget += get_function(self.render_cmd_icon[b'insertOrderedList'])(id)
        widget += get_function(self.render_cmd_icon[b'insertUnorderedList'])(id)
        widget += get_function(self.render_cmd_icon[b'insertImage'])(id)
        widget += get_function(self.render_cmd_icon[b'createLink'])(id)
        widget += get_function(self.render_cmd_icon[b'insertHTML'])(id)
        widget += get_function(self.render_cmd_icon[b'foreColor'])(id)
        widget += get_function(self.render_cmd_icon[b'changeView'])(id)
        widget += b'  </div>  <div class="wysihtml5-dialogs">'
        widget += get_function(self.render_cmd_dialog[b'createLink'])(id)
        widget += get_function(self.render_cmd_dialog[b'insertImage'])(id)
        widget += b'  </div></div>'
        return widget

    def render_js_delay_widget(self, id, position):
        options = {b'id': id}
        options.update(self.editor_settings)
        if not options.get(b'name', None) or options[b'name'] == b'null':
            options[b'name'] = b'"%s"' % id[3:]
        if not options.get(b'toolbar', None) or options[b'toolbar'] == b'null':
            options[b'toolbar'] = b'"%s-toolbar"' % id
        options[b'prefixid'] = id[0:position]
        widget = b"\n<script>\n  setTimeout(function() {\n    var id = '%(id)s';\n    var name = '%(name)s';\n    var toolbar = %(toolbar)s;\n    if(typeof(window._wysihtml5_inited) == 'undefined') {\n      window._wysihtml5_inited = []\n    }\n    if(typeof(window._wysihtml5_inited[id]) == 'undefined') {\n      window._wysihtml5_inited[id] = true;\n    } else {\n      var totforms = parseInt(document.getElementById('%(prefixid)sTOTAL_FORMS').value)-1;\n      var newid = id.replace(/__prefix__/, totforms);\n      var name = name.replace(/__prefix__/, totforms);\n      var newtoolbar = toolbar.replace(/__prefix__/, totforms);\n      django.jQuery('#'+toolbar).attr('id', newtoolbar);\n      console.log(newid);\n      if(document.getElementById(newid)) {\n        new wysihtml5.Editor(newid,{\n          name:                 name,\n          style:                %(style)s,\n          toolbar:              newtoolbar,\n          autoLink:             %(autoLink)s,\n          parserRules:          %(parserRules)s,\n          parser:               %(parser)s,\n          composerClassName:    %(composerClassName)s,\n          bodyClassName:        %(bodyClassName)s,\n          useLineBreaks:        %(useLineBreaks)s,\n          stylesheets:          %(stylesheets)s,\n          placeholderText:      %(placeholderText)s,\n          allowObjectResizing:  %(allowObjectResizing)s,\n          supportTouchDevices:  %(supportTouchDevices)s\n        });\n      }\n    }\n  }, 0);\n</script>" % options
        return widget

    def render_js_init_widget(self, id):
        options = {b'id': id}
        options.update(self.editor_settings)
        if options.get(b'toolbar', b'null') == b'null':
            options[b'toolbar'] = b'"%s-toolbar"' % id
        widget = b'\n<script>\n  new wysihtml5.Editor("%(id)s",{\n    name:                 %(name)s,\n    style:                %(style)s,\n    toolbar:              %(toolbar)s,\n    autoLink:             %(autoLink)s,\n    parserRules:          %(parserRules)s,\n    parser:               %(parser)s,\n    composerClassName:    %(composerClassName)s,\n    bodyClassName:        %(bodyClassName)s,\n    useLineBreaks:        %(useLineBreaks)s,\n    stylesheets:          %(stylesheets)s,\n    placeholderText:      %(placeholderText)s,\n    allowObjectResizing:  %(allowObjectResizing)s,\n    supportTouchDevices:  %(supportTouchDevices)s\n  });\n</script>' % options
        return widget