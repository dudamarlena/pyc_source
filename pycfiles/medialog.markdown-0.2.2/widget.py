# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rolf/Plone5/zinstance/src/medialog.markdown/medialog/markdown/widgets/widget.py
# Compiled at: 2018-02-07 06:06:26
import zope.component, zope.interface, zope.schema.interfaces
from z3c.form import interfaces
from z3c.form import widget
from z3c.form.browser import text
from plone import api
from medialog.markdown.interfaces import IMarkdownSettings

class IMarkdownWidget(interfaces.IWidget):
    """Markdown widget."""
    pass


class MarkdownWidget(text.TextWidget):
    """Markdown Widget"""

    def make_button(self, name, icon, buttontext):
        group = 'group' + name
        name = 'cmd' + name
        title = name
        icon = icon
        buttontext = buttontext
        lenght = len(buttontext)
        return "{\n          name: '%(group)s',\n          data: [{\n            name: '%(name)s',\n            toggle: true, // this param only take effect if you load bootstrap.js\n            title: '%(title)s',\n            icon: '%(icon)s',\n            buttontext: '%(buttontext)s',\n            callback: function(e) {\n            // Append/remove admonion before the selection\n                var chunk, cursor, selected = e.getSelection(),\n                  content = e.getContent(),\n                  pointer, prevChar;\n\n                if (selected.length === 0) {\n                  // Give extra word\n                  chunk = e.__localize('tekst');\n                } else {\n                  chunk = selected.text;\n                }\n                e.replaceSelection('%(buttontext)s' + chunk);\n                cursor = selected.start + %(lenght)i - 1;\n                \n\n                // Set the cursor\n                e.setSelection(cursor, cursor + chunk.length);\n                }\n              }]\n            },\n            " % {'group': group, 'name': name, 
           'title': title, 
           'icon': icon, 
           'buttontext': buttontext, 
           'lenght': lenght}

    def make_buttons(self):
        buttons = ''
        btns = api.portal.get_registry_record(name='button_pairs', interface=IMarkdownSettings)
        for btn in btns:
            buttons += self.make_button(btn['name'], btn['icon'], btn['buttontext'])

        return '<script>\n          require([\n          \'jquery\',\n          \'++resource++medialog.markdown/markdown.min\',\n          \'++resource++medialog.markdown/bootstrap-markdown.min\',\n          ], function($) {\n              $(".markdown-textarea").markdown({\n              fullscreen:false,\n              resize: \'vertical\',\n              language: \'nb\',\n              hiddenButtons: \'cmdPreview\', \n              disabledButtons: \'cmdPreview\', \n              additionalButtons: [\n            [%(buttons)s]\n          ]\n        })\n          });\n        </script>' % {'buttons': buttons}

    def render_markdown(self):
        """Return the preview as a stringified HTML document."""
        portal_transforms = api.portal.get_tool(name='portal_transforms')
        value = self.value.encode('utf-8')
        data = portal_transforms.convertTo('text/html', value, mimetype='text/x-web-markdown')
        html = data.getData()
        return html

    def live_preview(self):
        return api.portal.get_registry_record(name='live_preview', interface=IMarkdownSettings)

    zope.interface.implementsOnly(IMarkdownWidget)


def MarkdownFieldWidget(field, request):
    """IFieldWidget factory for MarkdownWidget."""
    return widget.FieldWidget(field, MarkdownWidget(request))