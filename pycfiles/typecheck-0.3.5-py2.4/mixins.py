# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/typecheck/mixins.py
# Compiled at: 2006-05-27 18:37:17
from typecheck import _TC_NestedError, _TC_TypeError, check_type, Or
from typecheck import register_type, _TC_Exception

class _TC_IterationError(_TC_NestedError):
    __module__ = __name__

    def __init__(self, iteration, value, inner_exception):
        _TC_NestedError.__init__(self, inner_exception)
        self.iteration = iteration
        self.value = value

    def error_message(self):
        return 'at iteration %d (value: %s)' % (self.iteration, repr(self.value)) + _TC_NestedError.error_message(self)


class _UnorderedIteratorMixin(object):
    __module__ = __name__

    def __init__(self, class_name, obj):
        vals = [ o for o in obj ]
        self.type = self
        self._type = Or(*vals)
        self.__cls = obj.__class__
        self.__vals = vals
        self.__cls_name = class_name

    def __typecheck__(self, func, to_check):
        if not isinstance(to_check, self.__cls):
            raise _TC_TypeError(to_check, self)
        for (i, item) in enumerate(to_check):
            try:
                check_type(self._type, func, item)
            except _TC_Exception, e:
                raise _TC_IterationError(i, item, e)

    @classmethod
    def __typesig__(cls, obj):
        if isinstance(obj, cls):
            return obj

    def __str__(self):
        return '%s(%s)' % (self.__cls_name, str(self._type))

    __repr__ = __str__


def UnorderedIteratorMixin(class_name):

    class UIM(object):
        __module__ = __name__

        @classmethod
        def __typesig__(cls, obj):
            if isinstance(obj, cls):
                return _UnorderedIteratorMixin(class_name, obj)

        def __repr__(self):
            return '%s%s' % (class_name, str(tuple((e for e in self))))

    register_type(UIM)
    return UIM


register_type(_UnorderedIteratorMixin)