# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/utils/core/weakvaluelist.py
# Compiled at: 2011-02-04 03:54:22
import weakref

class WeakValueList(list):
    u"""
    オブジェクトの弱参照を保持するリスト
    """

    def count(self, x):
        return list.count(self, weakref.ref(x))

    def append(self, obj):
        u"""objへの弱参照をリストへ追加する"""
        list.append(self, weakref.ref(obj))

    def insert(self, index, obj):
        u"""objへの弱参照をindex番目に挿入する"""
        list.insert(self, index, weakref.ref(obj))

    def remove(self, obj):
        u"""objへの弱参照のうち最初のひとつをリストから削除する"""
        for ref in self:
            if obj is ref():
                list.remove(self, ref)
                return

        raise ValueError

    def tolist(self):
        u"""弱参照のリストを参照のリストへ変換する"""
        return [ ref() for ref in self ]

    def cleanup(self):
        u"""
        dead参照のアイテムを削除する
        """
        items = []
        for ref in self:
            if ref() == None:
                items.append(ref)

        for item in items:
            list.remove(self, item)

        return


if __name__ == '__main__':

    class Dummy:
        pass


    abc, defg, hijkl = Dummy(), Dummy(), Dummy()
    print abc, defg, hijkl
    l = WeakValueList()
    l.append(abc)
    l.append(defg)
    l.append(hijkl)
    print l.count(defg)
    l[0] = abc
    print l, l[0]
    for c in l:
        print c