# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/adminbrowse/__init__.py
# Compiled at: 2010-12-02 17:53:11
from adminbrowse.base import ChangeListColumn, ChangeListTemplateColumn, ChangeListModelFieldColumn, template_column, model_field
from adminbrowse.related import link_to_change, link_to_changelist, related_list
from adminbrowse.columns import link_to_url, truncated_field
from adminbrowse.admin import AutoBrowseModelAdmin