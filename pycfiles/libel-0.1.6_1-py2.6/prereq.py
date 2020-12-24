# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libel/prereq.py
# Compiled at: 2010-08-24 22:16:11


def _get(Item, Options):
    order = []
    for req in Options[Item]:
        if req in Options.keys():
            prereqs = _get(req, Options)
            for prereq in prereqs:
                order.append(prereq)

        order.append(req)

    return order


def get(Options):
    order = []
    for option in Options:
        for req in Options[option]:
            if req in Options.keys():
                prereqs = _get(req, Options)
                for prereq in prereqs:
                    if req in order:
                        if prereq not in order:
                            order.insert(0, prereq)
                    elif prereq not in order:
                        order.append(prereq)

                if req not in order:
                    order.append(req)

        if option not in order:
            order.append(option)

    return order


if __name__ == '__main__':
    options = {'a': ['b', 'c'], 'd': [
           'a'], 
       'c': [
           'e'], 
       'f': [
           'a', 'd']}
    print get(options)