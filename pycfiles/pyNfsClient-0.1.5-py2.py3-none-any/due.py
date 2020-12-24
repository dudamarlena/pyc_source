# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pynfold/due.py
# Compiled at: 2018-05-16 09:58:33
__doc__ = '\n\nuse in your code as\n\n    from .due import due, Doi, BibTeX\n\nSee  https://github.com/duecredit/duecredit/blob/master/README.md for examples.\n\nOrigin:     Originally a part of the duecredit\nCopyright:  2015-2016  DueCredit developers\nLicense:    BSD-2\n'
from __future__ import absolute_import, division, print_function
__version__ = '0.0.5'

class InactiveDueCreditCollector(object):
    """Just a stub at the Collector which would not do anything"""

    def _donothing(self, *args, **kwargs):
        """Perform no good and no bad"""
        pass

    def dcite(self, *args, **kwargs):
        """If I could cite I would"""

        def nondecorating_decorator(func):
            return func

        return nondecorating_decorator

    cite = load = add = _donothing

    def __repr__(self):
        return self.__class__.__name__ + '()'


def _donothing_func(*args, **kwargs):
    """Perform no good and no bad"""
    pass


try:
    from duecredit import due, BibTeX, Doi, Url
    if 'due' in locals() and not hasattr(due, 'cite'):
        raise RuntimeError('Imported due lacks .cite. DueCredit is now disabled')
except Exception as e:
    if type(e).__name__ != 'ImportError':
        import logging
        logging.getLogger('duecredit').error('Failed to import duecredit due to %s' % str(e))
    due = InactiveDueCreditCollector()
    BibTeX = Doi = Url = _donothing_func