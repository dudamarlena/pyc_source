# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.openbsd-4.7-i386/egg/ptemplate/util.py
# Compiled at: 2011-08-05 08:06:41
__license__ = 'Copyright (c) 2010 Will Maier <will@m.aier.us>\n\nPermission to use, copy, modify, and distribute this software for any\npurpose with or without fee is hereby granted, provided that the above\ncopyright notice and this permission notice appear in all copies.\n\nTHE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES\nWITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF\nMERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR\nANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES\nWHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN\nACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF\nOR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.\n\n'
import logging
__all__ = [
 'logger']

def logger(base, cls):
    """Return a logger.

    The logger's name is constructed from *base* (usually :data:`__name__` of
    the calling module) and the :attr:`__name__` attribute of
    :attr:`cls.__class__`.
    """
    name = '%s.%s' % (base, cls.__class__.__name__)