# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aestrivex/anaconda3/lib/python3.7/site-packages/bct/due.py
# Compiled at: 2020-04-27 14:47:22
# Size of source mod 2**32: 2018 bytes
"""

Stub file for a guaranteed safe import of duecredit constructs:  if duecredit
is not available.

To use it, place it into your project codebase to be imported, e.g. copy as

    cp stub.py /path/tomodule/module/due.py

Note that it might be better to avoid naming it duecredit.py to avoid shadowing
installed duecredit.

Then use in your code as

    from .due import due, Doi, BibTeX, Text

See  https://github.com/duecredit/duecredit/blob/master/README.md for examples.

Origin:     Originally a part of the duecredit
Copyright:  2015-2019  DueCredit developers
License:    BSD-2
"""
__version__ = '0.0.8'

class InactiveDueCreditCollector(object):
    __doc__ = 'Just a stub at the Collector which would not do anything'

    def _donothing(self, *args, **kwargs):
        """Perform no good and no bad"""
        pass

    def dcite(self, *args, **kwargs):
        """If I could cite I would"""

        def nondecorating_decorator(func):
            return func

        return nondecorating_decorator

    active = False
    activate = add = cite = dump = load = _donothing

    def __repr__(self):
        return self.__class__.__name__ + '()'


def _donothing_func(*args, **kwargs):
    """Perform no good and no bad"""
    pass


try:
    from duecredit import due, BibTeX, Doi, Url, Text
    if 'due' in locals():
        if not hasattr(due, 'cite'):
            raise RuntimeError('Imported due lacks .cite. DueCredit is now disabled')
except Exception as e:
    try:
        if not isinstance(e, ImportError):
            import logging
            logging.getLogger('duecredit').error('Failed to import duecredit due to %s' % str(e))
        due = InactiveDueCreditCollector()
        BibTeX = Doi = Url = Text = _donothing_func
    finally:
        e = None
        del e