# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dora/interface/generic.py
# Compiled at: 2020-01-16 10:25:08
# Size of source mod 2**32: 318 bytes
import os

class Generic:

    def __init__(self, *args, **kargs):
        pass

    def get_user(self):
        return dict(user=(os.environ.get('DORA_USER')))

    def show(self, dataframe):
        dataframe.show()

    def command_aux(self, ISAContext):
        pass

    def command_ml(self, MLContext):
        pass