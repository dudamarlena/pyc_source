# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/oozie/reader/reader.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 2992 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import xml.etree.ElementTree as ET, sys, re
from vipe.oozie.graph import OozieGraph
from vipe.oozie.reader.handlers import handle_fork, handle_decision, handle_action, handle_join, handle_start, handle_end, handle_kill
from vipe.oozie.reader.utils import properties_to_dict

def read(xml_string):
    """ Read Oozie XML workflow definition

    Args:
        xml_string (string): Oozie XML

    Returns:
        OozieGraph
    """
    root = ET.fromstring(__remove_namespaces(xml_string))
    ignore_tags = ['global']
    independently_handled_tags = ['parameters']
    handlers_register = {'fork': handle_fork,  'decision': handle_decision, 
     'action': handle_action, 
     'join': handle_join, 
     'start': handle_start, 
     'end': handle_end, 
     'kill': handle_kill}
    nodes_register = {}
    parameters = {}
    for child in root:
        tag_name = child.tag
        if tag_name not in list(handlers_register.keys()) + independently_handled_tags + ignore_tags:
            raise Exception('tag "{}" encountered which is neither ignored nor handled'.format(tag_name))
        if tag_name in ignore_tags:
            pass
        elif tag_name in independently_handled_tags:
            if tag_name == 'parameters':
                parameters = properties_to_dict(child)
        else:
            try:
                name, node = handlers_register[tag_name](child)
                nodes_register[name] = node
            except Exception:
                tag_string = ET.tostring(child, encoding='utf8', method='xml')
                print('Error occurred while analyzing tag "{}"'.format(tag_string), file=sys.stderr)
                raise

    return OozieGraph(parameters, nodes_register)


def __remove_namespaces(xml_string):
    xml_string_no_namespaces1 = re.sub('xmlns="[^"]+"', '', xml_string)
    xml_string_no_namespaces2 = re.sub("xmlns='[^']+'", '', xml_string_no_namespaces1)
    return xml_string_no_namespaces2