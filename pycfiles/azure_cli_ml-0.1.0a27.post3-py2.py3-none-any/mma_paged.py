# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\GitCode\trangevi-azurecli\azure\cli\command_modules\ml\_mma\models\mma_paged.py
# Compiled at: 2017-09-20 13:50:34
from msrest.paging import Paged

class ModelManagementAccountPaged(Paged):
    """
    A paging container for iterating over a list of ModelManagementAccount object
    """
    _attribute_map = {'next_link': {'key': 'nextLink', 'type': 'str'}, 'current_page': {'key': 'value', 'type': '[ModelManagementAccount]'}}

    def __init__(self, *args, **kwargs):
        super(ModelManagementAccountPaged, self).__init__(*args, **kwargs)