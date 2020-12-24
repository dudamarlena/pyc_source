# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\models\tree_models\xml_navigator.py
# Compiled at: 2019-01-23 04:25:13
# Size of source mod 2**32: 829 bytes
import logging

class XmlNavigatorAdditionalParams:

    def __init__(self):
        try:
            complex_value_attribute = False
            complex_value_attribute_paths = []
        except Exception as e:
            logging.error('Error initialization. ' + str(e))


class XmlNavigator:

    def __init__(self, paths, value_attribute, convert_types, style, additional_params=None):
        try:
            self.paths = paths
            self.value_attribute = value_attribute
            self.convert_types = convert_types
            self.style = style
            self.additional_params = additional_params
        except Exception as e:
            logging.error('Error initialization. ' + str(e))