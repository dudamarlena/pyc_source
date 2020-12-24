# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/DRSUpdate.py
# Compiled at: 2020-04-14 15:22:04
# Size of source mod 2**32: 3429 bytes
"""
Read a csv of DRS deposit log entries, extract fields for call to DRS db
sproc 'AddDRS'

"""
import argparse
from typing import Dict, Any
import DBApps.Writers.DbWriter as DbWriter
from DBApps.SourceProcessors import WebAdminResults
PDSHeaders = dict(object_id_num='objectid', object_huldrsadmin_ownerSuppliedName_string='OSN', object_urn_string_sort='objectUrn',
  batch_huldrsadmin_batchDirectoryName_string='DRSDir',
  batch_huldrsadmin_loadStartTime_date='IngestDate',
  object_fileCount_num='filesCount',
  object_objectSize_num='size')
PDSHeaders: Dict[(Any, str)]
RelatedHeaders = dict(file_id_num='objectid', file_huldrsadmin_ownerSuppliedName_string='OSN', file_huldrsadmin_uri_string_sort='objectUrn',
  batch_huldrsadmin_batchDirectoryName_string='DRSDir',
  batch_huldrsadmin_loadStartTime_date='IngestDate',
  file_premis_size_num='size')
RelatedHeaders: Dict[(Any, str)]
drs_params_ordered = ('IngestDate', 'objectid', 'objectUrn', 'DRSDir', 'filesCount',
                      'size', 'OSN')

class GetArgs:
    __doc__ = '\n    Holds command line arguments\n    '


def dict_to_add_DRS_param_list(dict_list: dict) -> list:
    """
    Transforms a named dictionary into a list of parameters for DRS.AddDRS
    Fills NULL for missing columns
    :return:
    :param dict_list:input file columns
    """
    rc = []
    for a_dict in dict_list:
        a_list = []
        [a_list.append(a_dict.get(s)) for s in drs_params_ordered]
        rc.append(a_list)

    return rc


def DRSUpdate():
    myArgs = GetArgs()
    parse_args(myArgs)
    if myArgs.relatedFile:
        fileColumnDict = RelatedHeaders
    else:
        fileColumnDict = PDSHeaders
    admin_results = WebAdminResults.WebAdminResults(fileColumnDict)
    param_dict_list = admin_results.csv_to_dict(myArgs.sourceFile)
    myArgs.sproc = 'AddDRS'
    writer = DbWriter(myArgs)
    param_list = dict_to_add_DRS_param_list(param_dict_list)
    writer.write_list(param_list)


def parse_args(arg_namespace: object) -> None:
    """
    :rtype: object
    :param arg_namespace. class which holds arg values
    """
    _parser = argparse.ArgumentParser(description='Reads  a raw CSV file which holds output of a HUL DRS                      WebAdmin search',
      usage="%(prog)s [ -r| --related-file ] -d | --drsDbConfig  section:configFile sourcefile                      where 'section' is a section in a python dbConfig file 'configFile' ")
    _parser.add_argument('sourceFile', help='CSV file containing search WebAdminResults.')
    _parser.add_argument('-d', '--drsDbConfig')
    _parser.add_argument('-r', '--relatedFile', action='store_true', default=False)
    _parser.parse_args(namespace=arg_namespace)


if __name__ == '__main__':
    DRSUpdate()