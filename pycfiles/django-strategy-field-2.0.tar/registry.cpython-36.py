# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-strategy-field/src/strategy_field/registry.py
# Compiled at: 2018-02-11 06:48:34
# Size of source mod 2**32: 2159 bytes
import logging, six
from inspect import isclass
from django.utils.functional import cached_property
from .utils import fqn, get_attr, import_by_name, get_display_string
logger = logging.getLogger(__name__)

class Registry(list):

    def __init__(self, base_class, *args, **kwargs):
        self._klass = base_class
        self._label_attribute = kwargs.get('label_attribute', None)
        self._choices = None
        (list.__init__)(self, *args[:])

    @cached_property
    def klass(self):
        if isinstance(self._klass, six.string_types):
            return import_by_name(self._klass)
        else:
            return self._klass

    def get_name(self, entry):
        return get_display_string(entry, self._label_attribute)

    def is_valid(self, value):
        if value:
            if isinstance(value, six.string_types):
                try:
                    value = import_by_name(value)
                except (ImportError, ValueError, AttributeError):
                    return False

        if self.klass:
            return isclass(value) and issubclass(value, self.klass) or isinstance(value, self.klass)
        else:
            return True

    def as_choices(self):
        if not self._choices:
            self._choices = sorted((fqn(klass), self.get_name(klass)) for klass in self)
        return self._choices

    def append(self, class_or_fqn):
        if isinstance(class_or_fqn, six.string_types):
            cls = import_by_name(class_or_fqn)
        else:
            cls = class_or_fqn
        if cls == self.klass:
            return
        else:
            if self.klass:
                if not issubclass(cls, self.klass):
                    raise ValueError("'%s' is not a subtype of %s" % (class_or_fqn, self.klass))
            if cls in self:
                return
            super(Registry, self).append(cls)
            self._choices = None
            return class_or_fqn

    register = append

    def __contains__(self, y):
        if isinstance(y, six.string_types):
            try:
                y = import_by_name(y)
            except (ImportError, ValueError):
                return False

        return super(Registry, self).__contains__(y)