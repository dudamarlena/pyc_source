# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/deprecated.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 725 bytes
from dexy.filter import DexyFilter
import dexy.exceptions

class Deprecated(DexyFilter):
    __doc__ = '\n    Base class for deprecated filters.\n    '
    aliases = []

    def process(self):
        msg = '%s\n%s' % (self.artifact.key, self.__doc__)
        raise dexy.exceptions.UserFeedback(msg)


class FilenameFilter(Deprecated):
    __doc__ = "\n    Deprecated. No longer needed.\n    \n    Dexy should now automatically detect new files that are created by your\n    scripts if the add-new-files setting is true (which it is by default in\n    many filters). You should remove '|fn' from your config and anywhere\n    documents are referenced, and remove the 'dexy--' prefix from filenames in\n    your scripts.\n    "
    aliases = ['fn']