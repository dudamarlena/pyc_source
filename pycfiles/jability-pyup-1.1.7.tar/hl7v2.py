# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/hl7/hl7v2.py
# Compiled at: 2013-05-25 04:38:30
import os.path

class hl7Container:
    DEFAULT_LEVEL_SEPARATOR = None

    def __init__(self, hl7string='', separator=None):
        self.value = hl7string
        self.sublevel_separator = separator

    def split(self):
        self.value = hl7string

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def __unicode__(self):
        return unicode(self.value)

    @staticmethod
    def set_default_separator(separator=None):
        DEFAULT_LEVEL_SEPARATOR = separator


class hl7SubComponent(hl7Container):
    DEFAULT_LEVEL_SEPARATOR = '&'

    def __init__(self, hl7string):
        hl7Container.__init__(self, hl7string)


class hl7Component(hl7Container):
    DEFAULT_LEVEL_SEPARATOR = '^'

    def __init__(self, hl7string, separator=hl7SubComponent.DEFAULT_LEVEL_SEPARATOR):
        hl7Container.__init__(self, hl7string, separator)
        self.split()

    def split(self):
        self.subcomponents = list()
        partslist = self.value.split(self.sublevel_separator)
        for v in partslist:
            self.subcomponents.append(hl7SubComponent(v))

    def is_multivalue(self):
        if len(self.subcomponents) > 1:
            return True
        return False

    def __len__(self):
        return len(self.subcomponents)

    def __getitem__(self, index):
        return self.subcomponents[index]

    def is_empty(self):
        if self.__len__() > 0:
            return False
        return True


class hl7Value(hl7Container):
    DEFAULT_LEVEL_SEPARATOR = '~'

    def __init__(self, hl7string, separator=hl7Component.DEFAULT_LEVEL_SEPARATOR):
        hl7Container.__init__(self, hl7string, separator)
        self.split()

    def split(self):
        self.components = list()
        partslist = self.value.split(self.sublevel_separator)
        for v in partslist:
            self.components.append(hl7Component(v))

    def is_multivalue(self):
        if len(self.components) > 1:
            return True
        return False

    def __len__(self):
        return len(self.components)

    def __getitem__(self, index):
        return self.components[index]

    def is_empty(self):
        if self.__len__() > 0:
            return False
        return True


class hl7Field(hl7Container):
    DEFAULT_LEVEL_SEPARATOR = '|'

    def __init__(self, hl7string, separator=hl7Value.DEFAULT_LEVEL_SEPARATOR):
        hl7Container.__init__(self, hl7string, separator)
        self.split()

    def split(self):
        self.values = list()
        partslist = self.value.split(self.sublevel_separator)
        for v in partslist:
            self.values.append(hl7Value(v))

    def is_multivalue(self):
        if len(self.values) > 1:
            return True
        return False

    def __len__(self):
        return len(self.values)

    def __getitem__(self, index):
        return self.values[index]

    def is_empty(self):
        if self.__len__() > 0:
            return False
        return True


class hl7Segment(hl7Container):
    DEFAULT_LEVEL_SEPARATOR = '\r'

    def __init__(self, hl7string, separator=hl7Field.DEFAULT_LEVEL_SEPARATOR):
        hl7Container.__init__(self, hl7string, separator)
        self.name = None
        self.split()
        return

    def split(self):
        self.fields = list()
        partslist = self.value.split(self.sublevel_separator)
        for v in partslist:
            self.fields.append(hl7Field(v))

        if len(self.fields) > 0:
            self.name = self.fields[0].value

    def is_multivalue(self):
        if len(self.fields) > 1:
            return True
        return False

    def __len__(self):
        return len(self.fields)

    def __getitem__(self, index):
        return self.fields[index]

    def is_empty(self):
        if self.__len__() > 0:
            return False
        return True


class hl7Message(hl7Container):
    DEFAULT_LEVEL_SEPARATOR = None

    def __init__(self, hl7string='', separator=hl7Segment.DEFAULT_LEVEL_SEPARATOR):
        hl7Container.__init__(self, hl7string, separator)
        self.segments = list()
        self.type = None
        self.event = None
        self.datetime = None
        self.id = None
        self.charset = None
        self.version = None
        self.split()
        return

    def split(self):
        self.segments = list()
        partslist = self.value.strip().split(self.sublevel_separator)
        for v in partslist:
            if not v.strip() == '':
                self.segments.append(hl7Segment(v.strip()))

        if len(self.segments) > 0:
            if len(self.segments[0]) > 6:
                self.datetime = self.segments[0].fields[6].value
                if len(self.segments[0]) > 8:
                    self.type = self.segments[0].fields[8].values[0].components[0].value
                    self.event = self.segments[0].fields[8].values[0].components[1].value
                    if len(self.segments[0]) > 9:
                        self.id = self.segments[0].fields[9].value
                        if len(self.segments[0]) > 11:
                            self.version = self.segments[0].fields[11].value
                            if len(self.segments[0]) > 17:
                                self.charset = self.segments[0].fields[17].value

    def get_data(self, indexexpression, defaultvalue=''):
        return hl7Message._ensure_listindex(self.segments, indexexpression, defaultvalue)

    def get_data_for_segment(self, segment_name, indexexpression, defaultvalue=''):
        segindex = self.get_segmentindex(segment_name)
        if not segindex == None:
            return self.get_data('[' + str(segindex) + ']' + indexexpression, defaultvalue)
        else:
            return defaultvalue

    def get_segmentindex(self, segment_name):
        i = 0
        for segment in self.segments:
            if segment_name == segment.fields[0].value:
                return i
            i += 1

        return

    def get_segment_by_name(self, segment_name):
        for segment in self.segments:
            if segment_name == segment.fields[0].value:
                return segment

        return

    def load(self, filepath, segment_separator='\r'):
        if not os.path.exists(filepath):
            return False
        fileobj = open(filepath, 'r')
        filedata = fileobj.read()
        fileobj.close()
        filedata = filedata.replace('\n', '\r')
        filedata = filedata.replace('\r\r', '\r')
        if len(filedata) > 8 and filedata[0:3] == 'MSH':
            hl7Segment.set_default_separator = segment_separator
            hl7Field.set_default_separator = filedata[3]
            hl7Value.set_default_separator = filedata[5]
            hl7Component.set_default_separator = filedata[4]
            hl7SubComponent.set_default_separator = filedata[7]
            self.value = filedata
            self.split()
            return True
        return False

    def is_hl7v2(self):
        if len(self.segments) > 0 and len(self.segments[0].fields) > 0 and self.segments[0].fields[0].value == 'MSH':
            return True
        return False

    def is_empty(self):
        if self.__len__() > 0:
            return False
        return True

    def is_multivalue(self):
        if self.__len__() > 1:
            return True
        return False

    def __len__(self):
        return len(self.segments)

    def __repr__(self):
        return str(self.value)

    def __getitem__(self, index):
        return self.segments[index]

    @staticmethod
    def _ensure_listindex(listobj, index_expression, default=''):
        u"""Permet d'�viter les IndexError déclenchés par l'absence d'un indice 
            dans une expression représentant l'appel d'un élément de liste/tuple.
            Si l'indice existe, la valeur correspondante est renvoyée.
            Si l'indice n'existe pas, la fonction renvoie la valeur par défaut.
        """
        mylocallist = listobj
        try:
            res = eval('mylocallist' + index_expression)
        except IndexError:
            return default

        return res