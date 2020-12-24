# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/xml_utils.py
# Compiled at: 2014-12-14 23:52:40
from xml.etree import ElementTree
from cStringIO import StringIO
from xml.dom.minidom import parseString
from lxml import etree

def prettify(root, encoding='utf-8'):
    """
    Return a pretty-printed XML string for the Element.

    @see: http://www.doughellmann.com/PyMOTW/xml/etree/ElementTree/create.html
    """
    if isinstance(root, ElementTree.Element):
        node = ElementTree.tostring(root, 'utf-8')
    else:
        node = root
    return etree.tostring(etree.fromstring(node), pretty_print=True, xml_declaration=True, encoding='utf-8')