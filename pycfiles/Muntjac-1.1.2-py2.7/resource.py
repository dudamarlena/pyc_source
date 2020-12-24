# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/resource.py
# Compiled at: 2013-04-04 15:36:36


class IResource(object):
    """C{IResource} provided to the client terminal. Support for
    actually displaying the resource type is left to the terminal.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def getMIMEType(self):
        """Gets the MIME type of the resource.

        @return: the MIME type of the resource.
        """
        raise NotImplementedError