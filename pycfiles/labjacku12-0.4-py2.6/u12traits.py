# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/labjack/u12traits.py
# Compiled at: 2009-07-24 09:07:43
from u12 import LabjackU12
from enthought.traits.api import HasTraits
from enthought.traits.api import Str, List as TList, Instance, Bool
from enthought.traits.api import Str, Float, Int, File, List, Instance, Tuple, Property
from enthought.traits.ui.api import View, Item, Group

class LabjackU12g(LabjackU12, HasTraits):
    pass


def main():
    for l in LabjackU12g.find_all():
        l.configure_traits()


if __name__ == '__main__':
    main()