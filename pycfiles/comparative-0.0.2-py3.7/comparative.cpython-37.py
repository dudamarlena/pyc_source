# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\comparative.py
# Compiled at: 2019-03-16 17:38:32
# Size of source mod 2**32: 1508 bytes
import operator, logging
COMPARISONS = ('__lt__', '__le__', '__eq__', '__ne__', '__ge__', '__gt__')
logging.basicConfig(level=(logging.INFO))
LOGGER = logging.getLogger(__name__)

def comparison_factory(op_name, strict, *attrs):
    comparable_attrs = (operator.attrgetter)(*attrs)

    def comparison(self, other):
        if strict:
            if not isinstance(other, type(self)):
                return NotImplemented
        op_fn = getattr(operator, op_name)
        return op_fn(comparable_attrs(self), comparable_attrs(other))

    return comparison


def compare_by(*attrs, strict=True):
    if not attrs:
        raise TypeError('no attribute supplied')

    def decorator(cls):
        for op_name in COMPARISONS:
            op_fn = comparison_factory(op_name, strict, *attrs)
            setattr(cls, op_name, op_fn)

        return cls

    return decorator


if __name__ == '__main__':

    @compare_by('hour', 'minute')
    class Clock:

        def __init__(self, hour=0, minute=0):
            self.hour = hour
            self.minute = minute

        def __str__(self):
            return '{0.hour:02d}:{0.minute:02d}'.format(self)

        def __repr__(self):
            return 'Clock(h={0.hour:}, m={0.minute:02d})'.format(self)


    clock1 = Clock(12, 0)
    clock2 = Clock(12, 1)
    print('clock1 < clock2', clock1 < clock2)
    print('clock1 <= clock2', clock1 <= clock2)
    print('clock1 != clock2', clock1 != clock2)