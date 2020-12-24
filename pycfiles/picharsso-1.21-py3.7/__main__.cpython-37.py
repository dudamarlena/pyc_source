# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/picharsso/__main__.py
# Compiled at: 2019-11-08 16:27:15
# Size of source mod 2**32: 723 bytes
from .configer import Configer
from .interface import Interface
from .loader import Loader
from .resizer import Resizer
from .processor import Processor
from .colorizer import Colorizer
from .displayer import Displayer

class Session(Configer, Interface, Loader, Resizer, Processor, Colorizer, Displayer):
    __doc__ = 'A wrapper for the program\n    '

    def __init__(self):
        Configer.__init__(self)
        Interface.__init__(self)
        Loader.__init__(self)
        Resizer.__init__(self)
        Processor.__init__(self)
        Colorizer.__init__(self)
        Displayer.__init__(self)
        getattr(self, self.args.command)()


def main():
    sess = Session()


if __name__ == '__main__':
    main()