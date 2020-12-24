# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mysqlmapper\mysql\builder\xml_config.py
# Compiled at: 2020-04-03 04:05:31
# Size of source mod 2**32: 1370 bytes
from xml.dom.minidom import parse, parseString

def parse_config_from_string(xml_string):
    """
    Parsing XML configuration string
    :param xml_string: XML configuration string
    :return: Profile information dictionary
    """
    return _parse_config_from_doc(parseString(xml_string))


def parse_config_from_file(file_path):
    """
    Parsing XML configuration file
    :param file_path: Profile path
    :return: Profile information dictionary
    """
    return _parse_config_from_doc(parse(file_path))


def _parse_config_from_doc(doc):
    """
    Parsing DOC documents
    :param doc: Doc document
    :return: Profile information dictionary
    """
    return_dict = {}
    root = doc.documentElement
    return_dict['mappers'] = {}
    for mapper in root.getElementsByTagName('mapper'):
        column = mapper.getAttribute('column')
        parameter = mapper.getAttribute('parameter')
        return_dict['mappers'][column] = parameter

    return_dict['sqls'] = {}
    for sql in root.getElementsByTagName('sql'):
        key = sql.getElementsByTagName('key')[0].childNodes[0].data
        value = sql.getElementsByTagName('value')[0].childNodes[0].data
        return_dict['sqls'][key] = value

    return return_dict