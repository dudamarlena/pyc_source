# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/entity/entity_tool.py
# Compiled at: 2020-01-28 21:01:02
# Size of source mod 2**32: 640 bytes


class EntityConfig:

    class Field:
        LOCALE = 'locale'

    F = Field

    @classmethod
    def j2locale(cls, j):
        if not j:
            return
        return j.get(cls.F.LOCALE)


class Entity:

    class Field:
        SPAN = 'span'
        VALUE = 'value'
        TEXT = 'text'

    F = Field

    @classmethod
    def j2span(cls, j):
        return j[cls.F.SPAN]

    @classmethod
    def j2value(cls, j):
        return j[cls.F.VALUE]

    @classmethod
    def j_pair2span(cls, j_pair):
        return (Entity.j2span(j_pair[0])[0], Entity.j2span(j_pair[1])[1])