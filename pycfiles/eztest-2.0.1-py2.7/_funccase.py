# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\eztest\_funccase.py
# Compiled at: 2018-06-21 22:15:50
"""Internal Class for building case object for functions."""
import datetime, sys
from .testcase import BaseCase, ERROR, INFO

class BuildCase(BaseCase):
    """Build case for external function."""

    def __init__(self):
        super(BuildCase, self).__init__()

    def __deepcopy__(self, obj):
        new = super(BuildCase, self).__deepcopy__(obj)
        new.initialize = self.initialize
        new.run = self.run
        new.dispose = self.dispose
        return new

    def log(self, message, to_console=False, level=INFO, no_format=False):
        """Output log message to sys.stdout.

        :param str message: message.
        :param bool to_console: print to console.
        :param str level: log level.
        :param bool no_format: print log message without format, otherwise the format will be "datetime level message"
        """
        if message and to_console:
            msg = ('{}\t{}\t{}\t{}').format(datetime.datetime.now().strftime('%Y-%d-%m %H:%M:%S.%f'), level, self.id, message) if not no_format else str(message)
            sys.stdout.write(msg + '\n')
            sys.stdout.flush()

    def do_case(self):
        """Will call initialize, run if initialize is True, verify if run is True, and dispose in sequence."""
        try:
            try:
                flag = self.initialize()
                if flag is None or flag:
                    self.start_datetime = datetime.datetime.now()
                    self.run()
                    self.end_datetime = datetime.datetime.now()
                    self.set_status(True)
                else:
                    self.set_status(False)
            except Exception:
                self.end_datetime = datetime.datetime.now()
                self.status = False
                self.log_exception()

        finally:
            try:
                self.dispose()
            except Exception:
                pass

            self.log('-' * 40)
            if self.status:
                self.log('Case is Pass.', True)
            else:
                self.log('Case is Fail.', True, ERROR)
            if self.on_finished:
                self.on_finished(self)

        return