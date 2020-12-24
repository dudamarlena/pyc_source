# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/nacc/uds3/packet.py
# Compiled at: 2019-12-05 17:01:18
# Size of source mod 2**32: 1384 bytes


class Packet(list):
    __doc__ = '\n    A collection of UDS Forms\n\n    This class is makes it convenient to access a field, which are all uniquely\n    named, regardless of which form they are in with the exception of A4D.\n    '

    def __init__(self):
        self._cache = dict()

    def __getitem__(self, key):
        """
        Searches through each form in the packet for the field, `key`

        Note: you cannot access fields in A4D in this manner since there is no
        guarantee there will only be one; a KeyError will be raised.

        Example:
            packet['RESTTRL'] is equivalent to:
            packet.__getitem__('RESTTRL')
        """
        if key in self._cache:
            return self._cache[key]
        for form in self:
            if key in form.fields:
                if 'A4D' in str(form.__class__):
                    raise KeyError('Form A4D is unsupported')
                self._cache[key] = form.fields[key]
                return self._cache[key]

        raise KeyError(key)