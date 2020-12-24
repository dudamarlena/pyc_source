# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tramline/interfaces.py
# Compiled at: 2006-11-08 05:39:19


class IInputFilterProcessor:
    __module__ = __name__

    def pushInput(data, out):
        """Push block of inputted data into processor.

        Processor writes data to pass along on input stream to
        out, using .write().
        """
        pass

    def finalizeInput(out):
        """Notify processor that input data is now complete.

        Processor can still choose to write data to pass along input
        stream to out, using .write().
        """
        pass

    def commit():
        """Commit any action taken during the input phase.
        """
        pass

    def abort():
        """"Abort action taken in the input phase.
        """
        pass


class IOutputFilterProcessor:
    __module__ = __name__

    def pushOutput(data, out):
        """Push block of outputted data into processor.

        Processor writes data to pass along on output stream to
        out, using .write().
        """
        pass

    def finalizeOutput(self, out):
        """Notify processor that output data is now complete.

        Processor can still choose to write data to pass along output
        stream to out, using .write().
        """
        pass