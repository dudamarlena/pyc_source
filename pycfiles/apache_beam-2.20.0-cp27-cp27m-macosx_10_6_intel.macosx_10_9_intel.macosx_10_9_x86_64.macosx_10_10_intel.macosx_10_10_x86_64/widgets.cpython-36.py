# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www_rbac/widgets.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 965 bytes
from flask_appbuilder.widgets import RenderTemplateWidget

class AirflowModelListWidget(RenderTemplateWidget):
    template = 'airflow/model_list.html'