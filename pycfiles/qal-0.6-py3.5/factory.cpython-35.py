# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/qal/dataset/factory.py
# Compiled at: 2016-04-12 13:41:36
# Size of source mod 2**32: 1424 bytes
"""
Created on Jan 12, 2014

@author: Nicklas Boerjesson
"""
from qal.dataset.files import FilesDataset
from qal.dataset.flatfile import FlatfileDataset
from qal.dataset.xpath import XpathDataset
from qal.dataset.rdbms import RDBMSDataset
from qal.dataset.spreadsheet import SpreadsheetDataset

def dataset_from_resource(_resource):
    """Create a qal dataset from a resource"""
    try:
        if _resource.type.upper() == 'FLATFILE':
            _ds = FlatfileDataset(_resource=_resource)
        else:
            if _resource.type.upper() == 'XPATH':
                _ds = XpathDataset(_resource=_resource)
            else:
                if _resource.type.upper() == 'RDBMS':
                    _ds = RDBMSDataset(_resource=_resource)
                else:
                    if _resource.type.upper() == 'SPREADSHEET':
                        _ds = SpreadsheetDataset(_resource=_resource)
                    else:
                        if _resource.type.upper() == 'FILES':
                            _ds = FilesDataset(_resource=_resource)
                        else:
                            raise Exception('qal.dataset.factory.dataset_from_resource: Unsupported source resource type: ' + str(_resource.type.upper()))
    except Exception as e:
        raise Exception('qal.dataset.factory.dataset_from_resource: Failed loading resource for ' + _resource.type.upper() + '.\n' + 'Resource: ' + str(_resource.caption) + '(' + str(_resource.uuid) + ')\n' + 'Error: \n' + str(e))

    return _ds


if __name__ == '__main__':
    pass