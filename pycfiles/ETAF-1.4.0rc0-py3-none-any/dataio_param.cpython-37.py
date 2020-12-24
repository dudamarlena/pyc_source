# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/federatedml/param/dataio_param.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 8138 bytes
from federatedml.param.base_param import BaseParam

class DataIOParam(BaseParam):
    __doc__ = '\n    Define dataio parameters that used in federated ml.\n\n    Parameters\n    ----------\n    input_format : str, accepted \'dense\',\'sparse\' \'tag\' only in this version. default: \'dense\'.\n                   please have a look at this tutorial at "DataIO" section of federatedml/util/README.md.\n                   Formally,\n                       dense input format data should be set to "dense",\n                       svm-light input format data should be set to "sparse",\n                       tag or tag:value input format data should be set to "tag".\n\n    delimitor : str, the delimitor of data input, default: \',\'\n\n    data_type : str, the data type of data input, accepted \'float\',\'float64\',\'int\',\'int64\',\'str\',\'long\'\n               "default: "float64"\n\n    exclusive_data_type : dict, the key of dict is col_name, the value is data_type, use to specified special data type\n                          of some features.\n\n    tag_with_value: bool, use if input_format is \'tag\', if tag_with_value is True,\n                    input column data format should be tag[delimitor]value, otherwise is tag only\n\n    tag_value_delimitor: str, use if input_format is \'tag\' and \'tag_with_value\' is True,\n                         delimitor of tag[delimitor]value column value.\n\n    missing_fill : bool, need to fill missing value or not, accepted only True/False, default: True\n\n    default_value : None or single object type or list, the value to replace missing value.\n                    if None, it will use default value define in federatedml/feature/imputer.py,\n                    if single object, will fill missing value with this object,\n                    if list, it\'s length should be the sample of input data\' feature dimension,\n                        means that if some column happens to have missing values, it will replace it\n                        the value by element in the identical position of this list.\n                    default: None\n\n    missing_fill_method: None or str, the method to replace missing value, should be one of [None, \'min\', \'max\', \'mean\', \'designated\'], default: None\n\n    missing_impute: None or list, element of list can be any type, or auto generated if value is None, define which values to be consider as missing, default: None\n\n    outlier_replace: bool, need to replace outlier value or not, accepted only True/False, default: True\n\n    outlier_replace_method: None or str, the method to replace missing value, should be one of [None, \'min\', \'max\', \'mean\', \'designated\'], default: None\n\n    outlier_impute: None or list,  element of list can be any type, which values should be regard as missing value, default: None\n\n    outlier_replace_value: None or single object type or list, the value to replace outlier.\n                    if None, it will use default value define in federatedml/feature/imputer.py,\n                    if single object, will replace outlier with this object,\n                    if list, it\'s length should be the sample of input data\' feature dimension,\n                        means that if some column happens to have outliers, it will replace it\n                        the value by element in the identical position of this list.\n                    default: None\n\n    with_label : bool, True if input data consist of label, False otherwise. default: \'false\'\n\n    label_name : str, column_name of the column where label locates, only use in dense-inputformat. default: \'y\'\n\n    label_type : object, accepted \'int\',\'int64\',\'float\',\'float64\',\'long\',\'str\' only,\n                use when with_label is True. default: \'false\'\n\n    output_format : str, accepted \'dense\',\'sparse\' only in this version. default: \'dense\'\n\n    '

    def __init__(self, input_format='dense', delimitor=',', data_type='float64', exclusive_data_type=None, tag_with_value=False, tag_value_delimitor=':', missing_fill=True, default_value=0, missing_fill_method=None, missing_impute=None, outlier_replace=True, outlier_replace_method=None, outlier_impute=None, outlier_replace_value=0, with_label=False, label_name='y', label_type='int', output_format='dense'):
        self.input_format = input_format
        self.delimitor = delimitor
        self.data_type = data_type
        self.exclusive_data_type = exclusive_data_type
        self.tag_with_value = tag_with_value
        self.tag_value_delimitor = tag_value_delimitor
        self.missing_fill = missing_fill
        self.default_value = default_value
        self.missing_fill_method = missing_fill_method
        self.missing_impute = missing_impute
        self.outlier_replace = outlier_replace
        self.outlier_replace_method = outlier_replace_method
        self.outlier_impute = outlier_impute
        self.outlier_replace_value = outlier_replace_value
        self.with_label = with_label
        self.label_name = label_name
        self.label_type = label_type
        self.output_format = output_format

    def check(self):
        descr = "dataio param's"
        self.input_format = self.check_and_change_lower(self.input_format, [
         'dense', 'sparse', 'tag'], descr)
        self.output_format = self.check_and_change_lower(self.output_format, [
         'dense', 'sparse'], descr)
        self.data_type = self.check_and_change_lower(self.data_type, [
         'int', 'int64', 'float', 'float64', 'str', 'long'], descr)
        if type(self.missing_fill).__name__ != 'bool':
            raise ValueError("dataio param's missing_fill {} not supported".format(self.missing_fill))
        if self.missing_fill_method is not None:
            self.missing_fill_method = self.check_and_change_lower(self.missing_fill_method, [
             'min', 'max', 'mean', 'designated'], descr)
        if self.outlier_replace_method is not None:
            self.outlier_replace_method = self.check_and_change_lower(self.outlier_replace_method, [
             'min', 'max', 'mean', 'designated'], descr)
        if type(self.with_label).__name__ != 'bool':
            raise ValueError("dataio param's with_label {} not supported".format(self.with_label))
        if self.with_label:
            if not isinstance(self.label_name, str):
                raise ValueError("dataio param's label_name {} should be str".format(self.label_name))
            self.label_type = self.check_and_change_lower(self.label_type, [
             'int', 'int64', 'float', 'float64', 'str', 'long'], descr)
        if self.exclusive_data_type is not None and not isinstance(self.exclusive_data_type, dict):
            raise ValueError('exclusive_data_type is should be None or a dict')
        return True