# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_form/include.py
# Compiled at: 2020-02-23 12:53:51
# Size of source mod 2**32: 1028 bytes
"""PyAMS_form.include module

This module is used for Pyramid integration
"""
from pyams_form.form import FormSelector
from pyams_form.widget import WidgetSelector
__docformat__ = 'restructuredtext'

def include_package(config):
    """Pyramid package include"""
    config.add_translation_dirs('pyams_form:locales')
    config.add_subscriber_predicate('form_selector', FormSelector)
    config.add_subscriber_predicate('widget_selector', WidgetSelector)
    config.scan()