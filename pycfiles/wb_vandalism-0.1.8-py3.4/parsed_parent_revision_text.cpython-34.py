# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wb_vandalism/datasources/parsed_parent_revision_text.py
# Compiled at: 2015-10-28 15:47:46
# Size of source mod 2**32: 394 bytes
import json, pywikibase
from revscoring.datasources import Datasource
from revscoring.datasources.parent_revision import text

def process_item(text):
    if text is None:
        return
    else:
        item = pywikibase.ItemPage()
        item.get(content=json.loads(text))
        return item


item = Datasource('parsed_parent_revision.item', process_item, depends_on=[text])