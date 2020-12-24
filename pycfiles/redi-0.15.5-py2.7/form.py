# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/redi/form.py
# Compiled at: 2018-08-13 08:58:37
__author__ = 'Taeber Rapczak <taeber@ufl.edu>'

class Form(object):

    def __init__(self, data):
        try:
            data.xpath('.')
        except Exception as data_exception:
            print data_exception
            raise ValueError('"data" should be a valid lxml etree')

        self._tree = data

    def events(self):
        for node in self._tree.xpath('//event[.]'):
            yield Event(node)


class Event(object):

    def __init__(self, etree_node):
        try:
            etree_node.xpath('.')
        except Exception:
            print ValueError('"etree_node" should be a valid lxml node')

        self._node = etree_node

    def field(self, name):
        nodes = self._node.xpath('./field[./name = $fieldName]', fieldName=name)
        nodecount = len(nodes)
        if nodecount == 1:
            return Field(nodes[0])
        else:
            if nodecount == 0:
                return
            raise Exception(('Malformed XML: multiple fields with the name {0}').format(name))
            return

    def fields(self):
        for node in self._node.xpath('./field[.]'):
            yield Field(node)

    @property
    def name(self):
        return self._node.findtext('name')

    @property
    def study_id(self):
        form = self._node.getparent()
        all_form_events = form.getparent()
        person = all_form_events.getparent()
        return person.findtext('study_id', default='')

    @property
    def form_name(self):
        return self._node.getparent().findtext('name', '')

    def is_empty(self):
        return not self._node.xpath("./field/value/text() != ''")


class Field(object):

    def __init__(self, etree_node):
        try:
            etree_node.findtext('value')
        except Exception:
            print ValueError('"etree_node" should be a valid lxml node')

        self._node = etree_node

    @property
    def name(self):
        return self._node.findtext('name', default='')

    @property
    def value(self):
        return self._node.findtext('value', default='')

    @value.setter
    def value(self, value):
        self._node.find('value').text = value

    def clear_value(self):
        self.value = ''