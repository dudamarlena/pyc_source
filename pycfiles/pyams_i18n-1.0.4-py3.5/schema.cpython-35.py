# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_i18n/schema.py
# Compiled at: 2020-02-20 11:01:05
# Size of source mod 2**32: 4959 bytes
"""PyAMS_i18n.schema module

This module provides custom schema fields to support contents internationalization.
"""
from persistent.mapping import PersistentMapping
from zope.interface import implementer
from zope.schema import Dict, Text, TextLine
from zope.schema.interfaces import IDict, RequiredMissing
from pyams_utils.schema import HTMLField
__docformat__ = 'restructuredtext'
_MARKER = object()

class DefaultValueDict(PersistentMapping):
    __doc__ = 'Persistent mapping with default value'

    def __init__(self, default=None, *args, **kwargs):
        super(DefaultValueDict, self).__init__(*args, **kwargs)
        self._default = default

    def __missing__(self, key):
        return self._default

    def get(self, key, default=None):
        result = super(DefaultValueDict, self).get(key, _MARKER)
        if result is _MARKER:
            if default is not None:
                return default
            return self._default
        return result

    def copy(self):
        return DefaultValueDict(default=self._default, **self)


class II18nField(IDict):
    __doc__ = 'I18n field marker interface'


@implementer(II18nField)
class I18nField(Dict):
    __doc__ = 'I18n base field class'

    def __init__(self, key_type=None, value_type=None, **kwargs):
        Dict.__init__(self, key_type=TextLine(), value_type=value_type, **kwargs)

    def _validate(self, value):
        super(I18nField, self)._validate(value)
        if self.required:
            if self.default:
                return
            if not value:
                raise RequiredMissing
            for lang in value.values():
                if lang:
                    return

            raise RequiredMissing


class II18nTextLineField(II18nField):
    __doc__ = 'I18n text line field marker interface'


@implementer(II18nTextLineField)
class I18nTextLineField(I18nField):
    __doc__ = 'I18n text line field'

    def __init__(self, key_type=None, value_type=None, default=None, value_constraint=None, value_min_length=0, value_max_length=None, **kwargs):
        super(I18nTextLineField, self).__init__(value_type=TextLine(constraint=value_constraint, min_length=value_min_length, max_length=value_max_length, default=default, required=False), **kwargs)


class II18nTextField(II18nField):
    __doc__ = 'I18n text field marker interface'


@implementer(II18nTextField)
class I18nTextField(I18nField):
    __doc__ = 'I18n text field'

    def __init__(self, key_type=None, value_type=None, default=None, value_constraint=None, value_min_length=0, value_max_length=None, **kwargs):
        super(I18nTextField, self).__init__(value_type=Text(constraint=value_constraint, min_length=value_min_length, max_length=value_max_length, default=default, required=False), **kwargs)


class II18nHTMLField(II18nField):
    __doc__ = 'I18n HTML field marker interface'


@implementer(II18nHTMLField)
class I18nHTMLField(I18nField):
    __doc__ = 'I18n HTML field'

    def __init__(self, key_type=None, value_type=None, default=None, value_constraint=None, value_min_length=0, value_max_length=None, **kwargs):
        super(I18nHTMLField, self).__init__(value_type=HTMLField(constraint=value_constraint, min_length=value_min_length, max_length=value_max_length, default=default, required=False), **kwargs)