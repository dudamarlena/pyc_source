# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www_rbac/widgets.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 965 bytes
from flask_appbuilder.widgets import RenderTemplateWidget

class AirflowModelListWidget(RenderTemplateWidget):
    template = 'airflow/model_list.html'