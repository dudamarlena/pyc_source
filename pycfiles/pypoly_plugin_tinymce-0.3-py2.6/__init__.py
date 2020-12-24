# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pp_tinymce/__init__.py
# Compiled at: 2011-11-24 16:15:11
import pypoly
from pypoly.component import Component
from pypoly.content.webpage import JavaScript
from pypoly.content.webpage.form.text import WYSIWYG
__version__ = '0.3'

class Main(Component):

    def start(self):
        pypoly.hook.register('content.web.webpage.head', 'tinymce', tinymce_hook)
        return True


def tinymce_hook(webpage=None, *args, **kwargs):
    editor_ids = []
    for child in webpage.get_childs(level=None):
        if isinstance(child, WYSIWYG) == True:
            editor_ids.append(child.id)

    if len(editor_ids) == 0:
        return []
    else:
        source = '\n        tinyMCE.init({\n            mode : "exact",\n            elements : "%(editor_ids)s",\n            theme : "advanced",\n            theme_advanced_toolbar_location : "top",\n            theme_advanced_toolbar_align : "left",\n            theme_advanced_statusbar_location : "bottom",\n            theme_advanced_resizing : true,\n            theme_advanced_resize_horizontal : false,\n            width : "100%%",\n        });\n    ' % {'editor_ids': (',').join(editor_ids)}
        return [
         JavaScript(url=pypoly.url('/plugin/tinymce/tiny_mce/tiny_mce.js', plain=True)),
         JavaScript(source=source)]