# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ropgadget/rgutils.py
# Compiled at: 2018-03-17 16:59:29


def deleteDuplicateGadgets(currentGadgets):
    gadgets_content_set = set()
    unique_gadgets = []
    for gadget in currentGadgets:
        gad = gadget['gadget']
        if gad in gadgets_content_set:
            continue
        gadgets_content_set.add(gad)
        unique_gadgets += [gadget]

    return unique_gadgets


def alphaSortgadgets(currentGadgets):
    return sorted(currentGadgets, key=lambda key: key['gadget'])