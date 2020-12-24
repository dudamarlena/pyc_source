# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/adverlet/browser/widget.py
# Compiled at: 2008-12-22 07:00:12
__license__ = 'GPL v.3'
from zope.component import getUtility
from z3c.widget.tiny.widget import TinyWidget
from ice.adverlet.interfaces import ISourceStorage

class RichTextWidget(TinyWidget):
    __module__ = __name__
    height = 25
    mce_theme = 'advanced'
    mce_theme_advanced_toolbar_location = 'top'
    mce_theme_advanced_toolbar_align = 'left'
    mce_theme_advanced_statusbar_location = 'bottom'
    width = '100%'
    mce_entity_encoding = 'raw'
    mce_convert_newlines_to_brs = 'false'
    mce_relative_urls = 'false'
    mce_theme_advanced_buttons1 = 'bold,italic,underline,strikethrough,justifyleft,justifycenter,justifyright,justifyfull,bullist,numlist,outdent,indent,formatselect,fontselect,fontsizeselect'
    mce_theme_advanced_buttons2 = 'cut,copy,paste,pastetext,pasteword,undo,redo,link,unlink,anchor,image,cleanup,code,insertdate,inserttime,forecolor,backcolor'
    mce_theme_advanced_buttons3 = 'tablecontrols,hr,removeformat,visualaid,sub,sup,charmap,iespell,media,advhr,ltr,rtl,preview,fullscreen'
    mce_extended_valid_elements = 'a[name|href|target|title|onclick],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]'

    @property
    def mce_plugins(self):
        return (',').join(getUtility(ISourceStorage).mceplugins)