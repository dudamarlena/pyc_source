# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/sspy/plugins/inputs/pulsegen/input.py
# Compiled at: 2011-09-15 17:42:41


class Input:

    def __init__(self):
        pass

    def Format(self):
        """
        @brief Prints the text block format that is parsed for the input
        """
        return self._plugin_data.GetFormat()

    def Add(self, input=None, options=None):
        pass

    def Advance(self, options=None):
        pass

    def Step(self, options=None):
        """
        @brief An alias for the advance method.
        @sa Advance
        
        """
        self.Advance(options)

    def Connect(self):
        pass

    def Finish(self):
        pass

    def Initiate(self):
        pass

    def New(self):
        pass

    def Step(self):
        pass

    def GetCore(self):
        pass