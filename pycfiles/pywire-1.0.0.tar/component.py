# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/2017-A/Dropbox/python_libraries/Pywire/pywire/component.py
# Compiled at: 2018-02-04 13:22:40
from .main import *
import math

class Component:
    all_components = []

    def __init__(self):
        self.all_components.append(self)
        self.links = []

    def instance(self, links):
        self.links.append(links)

    def body(self):
        pass

    def header(self):
        pass


class FromText(Component):

    def __init__(self, text):
        self.links = {}
        Component.__init__(self)
        flat_text = text.replace('\n', ' ').replace('\t', '').replace(')', ' ) ').replace('(', ' ( ').replace(';', ' ; ').split(' ')
        while '' in flat_text:
            flat_text.remove('')

        if 'entity' not in flat_text:
            raise Exception('Could not find entity name')
        self.name = flat_text[(flat_text.index('entity') + 1)]
        self.signals = {}
        all_in_indexes = [ i for i, x in enumerate(flat_text) if x == 'in' ]
        all_out_indexes = [ i for i, x in enumerate(flat_text) if x == 'out' ]
        for x in all_in_indexes + all_out_indexes:
            signal_name = flat_text[(x - 2)]
            signal_io = flat_text[x]
            vector_type = flat_text[(x + 1)]
            if vector_type == 'std_logic':
                signal_size = 0
            elif vector_type == 'std_logic_vector':
                if flat_text[(x + 4)] == 'to':
                    signal_size = int(flat_text[(x + 5)]) - int(flat_text[(x + 3)]) + 1
                else:
                    signal_size = int(flat_text[(x + 3)]) - int(flat_text[(x + 5)]) + 1
            else:
                raise Exception('Only std_logic and std_logic_vector are supported by Pywire as IO types')
            self.signals[signal_name] = {'size': signal_size, 'io': signal_io}

        header_text = (' ').join(flat_text[flat_text.index('port') + 2:flat_text.index('end')]).replace(' ; ', ';\n').replace('is ', 'is\n').replace('( ', '(').replace(' )', ')').replace(' ;', ';')
        self.header_text = 'component ' + self.name + ' is\n' + header_text + '\nend component;'

    def link(self, links):
        self.links = links

    def body(self):
        text = ''
        text += 'COMPONENT_' + str(len(Component.all_components)) + ' : ' + self.name + '\nport map (\n'
        for x in self.links.keys():
            if self.signals[x]['size'] == 0:
                text += x + ' => ' + self.links[x].name + '(0);\n'
            else:
                text += x + ' => ' + self.links[x].name + ';\n'

        text += 'clock => clock;\n'
        text += ');'
        return text

    def header(self):
        return self.header_text