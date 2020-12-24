# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/html5_file.py
# Compiled at: 2013-04-04 15:36:35


class Html5File(object):
    """L{DragAndDropWrapper} can receive also files from client computer
    if appropriate HTML 5 features are supported on client side. This class
    wraps information about dragged file on server side.
    """

    def __init__(self, name, size, mimeType):
        self._name = name
        self._size = size
        self._type = mimeType
        self._streamVariable = None
        return

    def getFileName(self):
        return self._name

    def getFileSize(self):
        return self._size

    def getType(self):
        return self._type

    def setStreamVariable(self, streamVariable):
        """Sets the L{StreamVariable} that into which the file contents
        will be written. Usage of StreamVariable is similar to L{Upload}
        component.

        If the L{StreamVariable} is not set in the L{DropHandler}
        the file contents will not be sent to server.

        I{Note!} receiving file contents is experimental feature
        depending on HTML 5 API's. It is supported only by modern web browsers
        like Firefox 3.6 and above and recent webkit based browsers (Safari 5,
        Chrome 6) at this time.

        @param streamVariable:
                   the callback that returns stream where the implementation
                   writes the file contents as it arrives.
        """
        self._streamVariable = streamVariable

    def getStreamVariable(self):
        return self._streamVariable