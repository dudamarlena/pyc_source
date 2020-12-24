# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/netappzapi/util.py
# Compiled at: 2010-10-08 17:48:52
import logging, debug
log = logging.getLogger('zapi')

def substituteVariables(str, namespace={}):
    """
    Perform variable substitution, given a string and a namespace.
    """
    try:
        str = str % namespace
        return str
    except KeyError, e:
        log.error('Cannot perform substitution on string. KeyError on: %s, %s', str, e)
        raise


def build_dict(node):
    """
    Create a dictionary representing an XML tree. Assumes
    the XML tree is only one layer deep.
    """
    result = {}
    for child in node:
        name = str(child.tag)
        result[name] = str(child.text)

    return result