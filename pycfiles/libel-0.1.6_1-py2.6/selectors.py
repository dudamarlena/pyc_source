# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libel/selectors.py
# Compiled at: 2010-08-28 19:20:07


class BaseSelector:
    parameter = None

    def __init__(self, Parameter):
        self.parameter = Parameter

    def test(self, Against):
        pass


class EQUALS(BaseSelector):

    def test(self, Against):
        if Against == self.parameter:
            return True
        return False


class IN(BaseSelector):

    def __init__(self, Parameter):
        if not hasattr(Parameter, '__iter__'):
            Parameter = [
             Parameter]
        BaseSelector.__init__(self, Parameter)

    def test(self, Against):
        if not hasattr(Against, '__iter__'):
            Against = [
             Against]
        for item in Against:
            if item in self.parameter:
                return True

        return False


class ALL(IN):

    def test(self, Against):
        if not hasattr(Against, '__iter__'):
            Against = [
             Against]
        all_ = []
        for parameter in self.parameter:
            if parameter not in Against:
                all_.append(False)

        return False not in all_