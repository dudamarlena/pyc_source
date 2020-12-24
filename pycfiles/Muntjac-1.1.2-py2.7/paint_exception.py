# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/paint_exception.py
# Compiled at: 2013-04-04 15:36:36


class PaintException(IOError):
    """C{PaintExcepection} is thrown if painting of a
    component fails.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, arg):
        """Constructs an instance of C{PaintExeception} with the specified
        detail message or an instance of C{PaintExeception} from IOException.

        @param arg:
                   the detail message or the original exception
        """
        super(PaintException, self).__init__(str(arg))