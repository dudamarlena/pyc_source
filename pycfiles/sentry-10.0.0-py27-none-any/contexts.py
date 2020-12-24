# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/interfaces/contexts.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six, string
from django.utils.encoding import force_text
from sentry.interfaces.base import Interface, prune_empty_keys
from sentry.utils.safe import get_path, trim
__all__ = ('Contexts', )
context_types = {}

class _IndexFormatter(string.Formatter):

    def format_field(self, value, format_spec):
        if not format_spec and isinstance(value, bool):
            return value and 'yes' or 'no'
        return string.Formatter.format_field(self, value, format_spec)


def format_index_expr(format_string, data):
    return six.text_type(_IndexFormatter().vformat(six.text_type(format_string), (), data).strip())


def contexttype(cls):
    context_types[cls.type] = cls
    return cls


class ContextType(object):
    indexed_fields = None
    type = None

    def __init__(self, alias, data):
        self.alias = alias
        ctx_data = {}
        for key, value in six.iteritems(trim(data)):
            if value is not None and value != '':
                ctx_data[force_text(key)] = value

        self.data = ctx_data
        return

    def to_json(self):
        rv = dict(self.data)
        rv['type'] = self.type
        return prune_empty_keys(rv)

    @classmethod
    def values_for_data(cls, data):
        rv = []
        for context in six.itervalues(data.get('contexts') or {}):
            if context and context.get('type') == cls.type:
                rv.append(context)

        return rv

    @classmethod
    def primary_value_for_data(cls, data):
        val = get_path(data, 'contexts', cls.type)
        if val and val.get('type') == cls.type:
            return val
        rv = cls.values_for_data(data)
        if len(rv) == 1:
            return rv[0]

    def iter_tags(self):
        if self.indexed_fields:
            for field, f_string in six.iteritems(self.indexed_fields):
                try:
                    value = format_index_expr(f_string, self.data)
                except KeyError:
                    continue

                if value:
                    if not field:
                        yield (
                         self.alias, value)
                    else:
                        yield (
                         '%s.%s' % (self.alias, field), value)


@contexttype
class DefaultContextType(ContextType):
    type = 'default'


@contexttype
class AppContextType(ContextType):
    type = 'app'
    indexed_fields = {'device': '{device_app_hash}'}


@contexttype
class DeviceContextType(ContextType):
    type = 'device'
    indexed_fields = {'': '{model}', 'family': '{family}'}


@contexttype
class RuntimeContextType(ContextType):
    type = 'runtime'
    indexed_fields = {'': '{name} {version}', 'name': '{name}'}


@contexttype
class BrowserContextType(ContextType):
    type = 'browser'
    indexed_fields = {'': '{name} {version}', 'name': '{name}'}


@contexttype
class OsContextType(ContextType):
    type = 'os'
    indexed_fields = {'': '{name} {version}', 'name': '{name}', 'rooted': '{rooted}'}


@contexttype
class GpuContextType(ContextType):
    type = 'gpu'
    indexed_fields = {'name': '{name}', 'vendor': '{vendor_name}'}


@contexttype
class MonitorContextType(ContextType):
    type = 'monitor'
    indexed_fields = {'id': '{id}'}


@contexttype
class TraceContextType(ContextType):
    type = 'trace'
    indexed_fields = {'': '{trace_id}', 'span': '{span_id}', 'ctx': '{trace_id}-{span_id}'}


class Contexts(Interface):
    """
    This interface stores context specific information.
    """
    display_score = 1100
    score = 800

    @classmethod
    def to_python(cls, data):
        rv = {}
        for alias, value in six.iteritems(data):
            if value is not None:
                rv[alias] = cls.normalize_context(alias, value)

        return cls(**rv)

    @classmethod
    def normalize_context(cls, alias, data):
        ctx_type = data.get('type', alias)
        ctx_cls = context_types.get(ctx_type, DefaultContextType)
        return ctx_cls(alias, data)

    def iter_contexts(self):
        return six.itervalues(self._data)

    def to_json(self):
        rv = {}
        for alias, inst in six.iteritems(self._data):
            rv[alias] = inst.to_json()

        return rv

    def iter_tags(self):
        for inst in self.iter_contexts():
            for tag in inst.iter_tags():
                yield tag