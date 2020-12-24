# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pod\list.py
# Compiled at: 2009-07-02 13:52:14
import exceptions, core, typed, query, fn

class PodListError(exceptions.BaseException):
    pass


class List(core.Object):

    def __init__(self, list=None, **kwargs):
        core.Object.__init__(self, **kwargs)
        if list:
            self.extend(list)

    def __len__(self):
        get_one = query.RawQuery(select=fn.count(ListItem.id) >> 'count', where=ListItem.parent == self).get_one()
        if get_one:
            return get_one.count

    def __contains__(self, x):
        get_one = query.RawQuery(where=(ListItem.parent == self) & (ListItem.value == x)).get_one(error_on_multiple=False)
        return True if get_one else False

    def __iter__(self):
        return (item.value for item in query.Query(select=ListItem.value, where=ListItem.parent == self))

    def __getitem__(self, i):
        if isinstance(i, int):
            return self.get_set_del_item(i)
        elif isinstance(i, slice):
            start, stop, step = i.start, i.stop, i.step
            if (start >= 0 or start is None) and (stop >= 0 or stop is None):
                start = 0 if start is None else start
                offset = start if start > 0 else None
                if stop is None:
                    limit = -1
                elif stop - start < 0:
                    return []
                else:
                    limit = stop - start if stop is not None else -1
                new_list = [ item.value for item in query.Query(select=ListItem.value, where=ListItem.parent == self, limit=limit, offset=offset) ]
                if i.step is None:
                    return new_list
                else:
                    return new_list[::i.step]
            return [ value for value in self ][i]
        else:
            raise PodListError, "'" + str(i) + "' not allowed as index, only int/slices allowed . . ."
        return

    def __setitem__(self, i, item):
        if isinstance(i, int):
            self.get_set_del_item(i, item)
        else:
            setted = [ e for e in self ]
            setted.__setitem__(i, item)
            self.clear()
            self.extend(setted)

    def __delitem__(self, i):
        if isinstance(i, int):
            self.get_set_del_item(i, delete=True)
        else:
            deleted = [ item for item in self ]
            deleted.__delitem__(i)
            self.clear()
            self.extend(deleted)

    def get_set_del_item(self, i, item=None, delete=False, return_node=False):
        if i < 0:
            order_by = ListItem.id.desc()
            offset = -1 * i + -1
        else:
            order_by = None
            offset = i
        if item is None:
            selector = ListItem.value if delete is False else None
            list_item = query.Query(select=selector, limit=1, where=ListItem.parent == self, order_by=order_by, offset=offset).get_one()
            return list_item and item is None and delete is False and list_item.value if return_node is False else list_item
        elif list_item and item and delete is False:
            list_item.value = item
        elif list_item and delete:
            list_item.delete()
        else:
            raise IndexError, 'list index out of range'
        return

    def copy(self):
        return [ i for i in self ]

    def clear(self):
        (ListItem.parent == self).delete()

    def append(self, value):
        ListItem(parent=self, value=value)

    def extend(self, L):
        for value in L:
            ListItem(parent=self, value=value)

    def pre_delete(self):
        self.clear()

    def pop(self, i=-1):
        item = self.get_set_del_item(i=i, return_node=True)
        value = item.value
        item.delete()
        return value

    def remove(self, x):
        get_one = query.Query(where=(ListItem.parent == self) & (ListItem.value == x)).get_one(error_on_multiple=False)
        if get_one:
            get_one.delete()
        else:
            raise PodListError, "Item '" + str(x) + "' not in list . . ."

    def count(self, x):
        return query.RawQuery(select=fn.count(ListItem.id) >> 'count', where=(ListItem.parent == self) & (ListItem.value == x)).get_one().count

    def index(self, x):
        get_one = query.RawQuery(where=(ListItem.parent == self) & (ListItem.value == x)).get_one(error_on_multiple=False)
        if get_one:
            return query.RawQuery(select=fn.count(ListItem.id) >> 'count', where=(ListItem.parent == self) & (ListItem.id < get_one.id)).get_one().count
        else:
            raise PodListError, "Item '" + str(x) + "' not in list . . ."

    def insert(self, i, x):
        inserted = [ item for item in self ]
        inserted.insert(i, x)
        self.clear()
        self.extend(inserted)

    def sort(self):
        sorted = [ item for item in self ]
        sorted.sort()
        self.clear()
        self.extend(sorted)

    def reverse(self):
        reversed = [ item for item in self ]
        reversed.reverse()
        self.clear()
        self.extend(reversed)


class ListItem(core.Object):
    parent = typed.PodObject(index=True)
    value = typed.Object(index=False)