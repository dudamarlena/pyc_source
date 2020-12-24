# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1/compat/octets.py
# Compiled at: 2019-10-17 01:00:19
from sys import version_info
if version_info[0] <= 2:
    int2oct = chr
    ints2octs = lambda s: ('').join([ int2oct(x) for x in s ])
    null = ''
    oct2int = ord
    octs2ints = lambda s: [ oct2int(x) for x in s ]
    str2octs = lambda x: x
    octs2str = lambda x: x
    isOctetsType = lambda s: isinstance(s, str)
    isStringType = lambda s: isinstance(s, (str, unicode))
    ensureString = str
else:
    ints2octs = bytes
    int2oct = lambda x: ints2octs((x,))
    null = ints2octs()
    oct2int = lambda x: x
    octs2ints = lambda x: x
    str2octs = lambda x: x.encode('iso-8859-1')
    octs2str = lambda x: x.decode('iso-8859-1')
    isOctetsType = lambda s: isinstance(s, bytes)
    isStringType = lambda s: isinstance(s, str)
    ensureString = bytes