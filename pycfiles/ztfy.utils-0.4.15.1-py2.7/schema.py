# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/timezone/schema.py
# Compiled at: 2012-06-20 10:07:04
__docformat__ = 'restructuredtext'
import pytz
from zope.schema.interfaces import IChoice, IVocabularyFactory
from zope.interface import implements, classProvides
from zope.schema import Choice
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

class TimezonesVocabulary(SimpleVocabulary):
    classProvides(IVocabularyFactory)

    def __init__(self, *args, **kw):
        terms = [ SimpleTerm(t, t, t) for t in pytz.all_timezones ]
        super(TimezonesVocabulary, self).__init__(terms)


class ITimezone(IChoice):
    """Marker interface for timezone field"""
    pass


class Timezone(Choice):
    """Timezone choice field"""
    implements(ITimezone)

    def __init__(self, **kw):
        if 'vocabulary' in kw:
            kw.pop('vocabulary')
        if 'default' not in kw:
            kw['default'] = 'GMT'
        super(Timezone, self).__init__(vocabulary='ZTFY timezones', **kw)