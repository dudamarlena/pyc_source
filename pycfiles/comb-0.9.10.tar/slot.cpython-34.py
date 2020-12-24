# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breezekay/Dropbox/Codes/nextoa/comb/comb/slot.py
# Compiled at: 2014-10-21 10:31:00
# Size of source mod 2**32: 2027 bytes


class Slot(object):
    __doc__ = "\n    To use comb, you should create a python module file. we named *slot*.\n\n    A legal slot must be named 'Slot' in your module file and it must be at least contain four method:\n\n    * `initialize`\n\n    initial resource, e.g: database handle\n\n    * `__enter__`\n\n    get next data to do,you can fetch one or more data.\n\n    * `slot`\n\n    user custom code\n\n    * `__exit__`\n\n    when slot finished, call this method\n\n    "

    def __init__(self, combd):
        """Don't override this method unless what you're doing.

        """
        self.threads_num = combd.threads_num
        self.sleep = combd.sleep
        self.sleep_max = combd.sleep_max
        self.debug = combd.debug
        self.combd = combd
        self.initialize()

    def initialize(self):
        """Hook for subclass initialization.
        
        This block is execute before thread initial
        
        Example::

            class UserSlot(Slot):
                def initialize(self):
                    self.threads_num = 10 

                def slot(self, result):
                    ...
        
        """
        pass

    def __enter__(self):
        """You **MUST** return False when no data to do.

        The return value will be used in `Slot.slot`
        """
        print('You should override __enter__ method by subclass')
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        """When slot done, will call this method.
        """
        print('You should override __exit__ method by subclass')

    def slot(self, msg):
        """
        Add your custom code at here.

        For example, look at:

        * `comb.demo.list`

        * `comb.demo.mongo`

        * `comb.demo.redis`

        """
        pass