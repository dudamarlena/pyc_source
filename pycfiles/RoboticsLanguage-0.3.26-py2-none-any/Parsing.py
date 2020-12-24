# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Tools/Parsing.py
# Compiled at: 2019-09-09 15:48:17
from lxml import etree
from RoboticsLanguage.Base import Utilities

def xml(tag, content=[], attributes={}, text='', namespace=''):
    if namespace == '':
        code = etree.Element(tag, attributes)
    else:
        code = etree.Element('{' + namespace + '}' + str(tag), attributes, nsmap={namespace: namespace})
    code.text = str(text)
    [ code.insert(0, x) for x in reversed(Utilities.ensureList(content)) ]
    return code


def xmlNamespace(name):
    return lambda *arguments, **options: xml(namespace=name, *arguments, **options)