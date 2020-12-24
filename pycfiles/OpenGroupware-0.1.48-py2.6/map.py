# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/format/map.py
# Compiled at: 2012-10-12 07:02:39
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class MapAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'map'
    __aliases__ = ['mapAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def _map(self, tag_dict):
        if tag_dict['system_source'].text == 'MS':
            tag_dict['oem_code'].text = 'XYZ'
            tag_dict['sale_amount'].text = unicode(float(tag_dict['sale_amount'].text) * float(tag_dict['quantity'].text))
        tag_dict['source'].text = ('PS{0}').format(tag_dict['source'].text)

    def do_action(self):
        self._state = {}
        self.rfile.seek(0)
        table_name = None
        format_name = None
        format_class = None
        for (event, element) in etree.iterparse(self.rfile, events=('start', )):
            if event == 'start' and element.tag == 'ResultSet':
                table_name = element.attrib.get('tableName')
                format_name = element.attrib.get('formatName')
                format_class = element.attrib.get('className')
                element.clear()
                break

        self.wfile.write('<?xml version="1.0" encoding="UTF-8"?>')
        self.wfile.write(('<ResultSet formatName="{0}" className="{1}" tableName="{2}">').format(format_name, format_class, table_name))
        self.rfile.seek(0)
        tag_dict = {}
        for (event, element) in etree.iterparse(self.rfile, events=('end', )):
            if event == 'end' and element.tag == 'row':
                self._map(tag_dict)
                self.wfile.write(etree.tostring(element))
                tag_dict = {}
            elif event == 'end':
                tag_dict[element.tag] = element

        self.wfile.write('</ResultSet>')
        return

    def parse_action_parameters(self):
        pass

    def do_epilogue(self):
        pass