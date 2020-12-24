# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ytsub/argparse_util.py
# Compiled at: 2013-01-05 11:13:54
import argparse, sys
from argparse import Action
from argparse import ArgumentError

def _ensure_value(namespace, name, value):
    if getattr(namespace, name, None) is None:
        setattr(namespace, name, value)
    return getattr(namespace, name)


class MaxCountAction(Action):
    """Acts like _CountAction, but raises an error when max_count exceeded"""

    def __init__(self, option_strings, dest, max_count, default=None, required=False, help=None, max_exceeded_msg='flag included too many times ({count}); max is {max_count}'):
        assert max_count > 0, 'max must be > 0'
        self.max_count = max_count
        self.msg = max_exceeded_msg
        super(MaxCountAction, self).__init__(option_strings=option_strings, dest=dest, nargs=0, default=default, required=required, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        new_count = _ensure_value(namespace, self.dest, 0) + 1
        if new_count > self.max_count:
            raise ArgumentError(self, self.msg.format(count=new_count, max_count=self.max_count))
        setattr(namespace, self.dest, new_count)


class ListOrStdinAction(Action):
    """This stores a list, taking input from args or stdin if no args."""

    def __init__(self, option_strings, dest, default=None, type=None, required=False, help=None, metavar=None):
        if default is not None and required is True:
            raise ValueError('If required, default cannot be set; this actionreads from stdin if given no parameters.')
        super(ListOrStdinAction, self).__init__(option_strings=option_strings, dest=dest, nargs='*', default=default, type=type, required=required, help=help, metavar=metavar)
        return

    def __call__(self, parser, namespace, values, option_string=None):
        items = []
        if values is None or len(values) is 0:
            for line in sys.stdin:
                items.append(parser._get_value(self, line))

            setattr(namespace, self.dest, items)
            return
        else:
            items.extend(values)
            setattr(namespace, self.dest, items)
            return