# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/silme/format/properties/parser.py
# Compiled at: 2010-06-12 17:55:55
from ...core import EntityList, Entity, Comment
from .structure import PropertiesStructure
import re

class PropertiesParser:
    patterns = {}
    patterns['entity'] = re.compile('^[ \t]*([^#!\\s\n][^=:\n]*?)[ \t]*[:=][ \t]*(.*?)(?<!\\\\)(?=\n|\\Z|\r)', re.S | re.M)
    patterns['comment'] = re.compile('^(#[^\n]*\n?)+', re.M | re.S)

    @classmethod
    def parse(cls, text, code='default'):
        prop = PropertiesStructure()
        cls.build_element_list(text, prop, code=code)
        prop.fallback = code
        return prop

    @classmethod
    def parse_to_entitylist(cls, text, code='default'):
        entitylist = EntityList()
        text = cls.patterns['comment'].sub('', text)
        matchlist = cls.patterns['entity'].findall(text)
        for match in matchlist:
            entitylist.add_entity(Entity(match[0], match[1], code))

        return entitylist

    @classmethod
    def parse_entity(cls, text, code='default'):
        match = self.patterns['entity'].match(text)
        if not match:
            raise Exception()
        entity = Entity(match.group(1))
        entity.set_value(match.group(2), code=code)
        return entity

    @classmethod
    def build_element_list(cls, text, object, type='comment', code='default', pointer=0, end=None):
        cls.split_comments(text, object, code=code)

    @classmethod
    def split_comments(cls, text, object, code='default', pointer=0, end=None):
        pattern = cls.patterns['comment']
        if end:
            match = pattern.search(text, pointer, end)
        else:
            match = pattern.search(text, pointer)
        while match:
            st0 = match.start(0)
            if st0 > pointer:
                cls.split_entities(text, object, code=code, pointer=pointer, end=st0)
            groups = match.groups()
            comment = Comment()
            cls.split_entities(match.group(0)[1:].replace('\n#', '\n'), comment, code=code)
            object.append(comment)
            pointer = match.end(0)
            if end:
                match = pattern.search(text, pointer, end)
            else:
                match = pattern.search(text, pointer)

        if (not end or end > pointer) and len(text) > pointer:
            cls.split_entities(text, object, code=code, pointer=pointer)

    @classmethod
    def split_entities(cls, text, object, code='default', pointer=0, end=None):
        pattern = cls.patterns['entity']
        if end:
            match = pattern.search(text, pointer, end)
        else:
            match = pattern.search(text, pointer)
        while match:
            st0 = match.start(0)
            if st0 > pointer:
                object.append(text[pointer:st0])
            groups = match.groups()
            entity = Entity(groups[0])
            entity.set_value(groups[1], code)
            entity.params['source'] = {'type': 'properties', 'string': match.group(0), 
               'valpos': match.start(2) - st0}
            object.append(entity)
            pointer = match.end(0)
            if end:
                match = pattern.search(text, pointer, end)
            else:
                match = pattern.search(text, pointer)

        if (not end or end > pointer) and len(text) > pointer:
            if end:
                object.append(text[pointer:end])
            else:
                object.append(text[pointer:])