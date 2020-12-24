# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joe/workspace/python/klient/src/django-caldav/django_caldav/__init__.py
# Compiled at: 2014-08-22 06:39:00
__author__ = 'Petr Knap <knap@wpj.cz>'

def print_xml(xml_as_string):
    if xml_as_string:
        from xml.dom import minidom
        xml_as_dom = minidom.parseString(xml_as_string)
        print xml_as_dom.toprettyxml()