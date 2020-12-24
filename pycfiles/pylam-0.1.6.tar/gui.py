# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/utils/gui/gui.py
# Compiled at: 2011-02-04 03:54:22
import weakref, types

def popcnf(key, cnf):
    item = None
    if cnf.has_key(key):
        item = cnf[key]
        del cnf[key]
    return item


def convweak(method):

    class Dummy:
        pass

    result = (
     weakref.ref(Dummy()), '')
    if method == None:
        return result
    else:
        if type(method) == tuple:
            result = method
        if type(method) == types.MethodType:
            result = (
             weakref.ref(method.__self__), method.__name__)
        return result


def kw(**kw):
    return kw


class SyncVarPort:

    def _backward(self, *args):
        try:
            self._backward_called
        except AttributeError:
            self._backward_called = True
            self.value.set(self.var.get())
            del self._backward_called

    def _forward(self):
        try:
            self._forward_called
        except AttributeError:
            self._forward_called = True
            self.var.set(self.value.get())
            del self._forward_called


class WithGUI:
    u"""
    GUIとの寿命同期機構など、GUIとの連携に必要な機構を格納する。
    def destroy(self):
        if self._dying: return
        self._dying = True
        WithGUI.destroy(self)
        core.Component.destroy(self)
    """

    def __init__(self):
        self._guis = weakref.WeakValueDictionary()
        self._dying = False

    def destroy(self):
        for key in self._guis:
            gui = self._guis[key]
            if gui._sync:
                gui.destroy()