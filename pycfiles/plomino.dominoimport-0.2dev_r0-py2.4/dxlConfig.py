# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plomino/dominoimport/dxlConfig.py
# Compiled at: 2009-07-06 10:08:57
RICHTEXT_STYLES = {'anchor': {'balise': 'a', 'att_name': 'name'}, 'par': {'balise': 'p', 'redo': True}, 'block': {'balise': 'div', 'redo': True}, 'span': {'balise': 'span', 'redo': True}, 'table': {'balise': 'table', 'redo': True}, 'tablerow': {'balise': 'tr', 'redo': True}, 'tablecell': {'balise': 'td', 'redo': True}, 'break': {'balise': 'br', 'end_tag': False}, 'horizrule': {'balise': 'hr', 'end_tag': False}, 'picture': {'balise': 'img', 'att_alt': 'alttext', 'end_tag': False}, 'attachmentref': {'balise': 'a', 'att_href': 'name'}}
FIELD_TYPES = {'text': 'TEXT', 'password': 'TEXT', 'number': 'NUMBER', 'datetime': 'DATETIME', 'richtext': 'RICHTEXT', 'richtextlite': 'RICHTEXT', 'names': 'NAME', 'authors': 'NAME', 'readers': 'NAME', 'keyword': 'SELECTION'}
FIELD_TYPES_ATTR = {'combobox': 'SELECT', 'listbox': 'MULTISELECT', 'dialoglist': 'MULTISELECT', 'checkbox': 'CHECKBOX', 'radiobutton': 'RADIO', 'comma': ','}
FIELD_MODES = {'editable': 'EDITABLE', 'computed': 'COMPUTED', 'computedfordisplay': 'DISPLAY', 'computedwhencomposed': 'CREATION'}
DOMINO_MIME_TYPES = {'Adobe Acrobat Document': 'pdf', 'XML Document': 'xml', 'xmlfile': 'xml', 'AcroExch.Document': 'pdf', 'htmlfile': 'html'}
DOMINO_IMAGE_FORMAT = [
 'jpeg', 'gif', 'cfg']
DOMINO_CODE_TYPE = [
 'lotusscritp', 'formula', 'lotusscript', 'javaproject', 'simpleaction', 'javascript']