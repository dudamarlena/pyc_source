# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spotsh/utils.py
# Compiled at: 2011-02-23 00:28:13
CHARSET = 'utf-8'

def to_str(s, errors='strict'):
    """
    Theoretically http://www.python.org/dev/peps/pep-0263/ for this and 
    # -*- coding: utf-8 -*-
    should help. But it don't .
    """
    if not isinstance(s, basestring):
        try:
            return str(s)
        except UnicodeEncodeError:
            return unicode(s).encode(CHARSET, errors)

    else:
        if isinstance(s, unicode):
            return s.encode(CHARSET, errors)
        else:
            return s