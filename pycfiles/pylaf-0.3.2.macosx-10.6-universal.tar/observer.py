# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/utils/core/observer.py
# Compiled at: 2011-02-04 03:54:22
import weakvaluelist

class Observer:
    """Subjectの監視者。単一のSubjectを監視する。メンバ変数による参照禁止"""

    def __init__(self, subject):
        self.subject = None
        self.register(subject)
        return

    def register(self, subject):
        self.unregister()
        subject.register(self)
        self.subject = subject

    def unregister(self):
        if not self.subject == None:
            self.subject.unregister(self)
            self.subject = None
        return

    def update(self, *args, **kw):
        pass


class Subject:
    """監視対象。いずれからも監視されなくなったら自動的に削除される。メンバ変数による参照禁止"""

    def __init__(self):
        self.observers = weakvaluelist.WeakValueList()

    def register(self, observer):
        if not self.observers.count(observer):
            self.observers.append(observer)

    def unregister(self, observer):
        self.observers.cleanup()
        self.observers.remove(observer)

    def notify(self, *args, **kw):
        u"""監視者へ変更を通知する。Observer.update()を起動する。起動の順番は登録順。"""
        self.observers.cleanup()
        for o in self.observers.tolist():
            o.update(*args, **kw)


import weakref
if __name__ == '__main__':
    s1 = Subject()
    o1a = Observer(s1)
    o1b = Observer(s1)
    ws1 = weakref.ref(s1)
    s1 = None
    print ws1()
    (o1a, o1b) = (None, None)
    print ws1()