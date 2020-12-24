# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dora/interface/zeppelin.py
# Compiled at: 2020-01-16 10:25:08
# Size of source mod 2**32: 843 bytes
import configparser, os
from ..isa import ISAMagic
from ..ml import MLMagic
from .generic import Generic
ZEPPELIN_HOME = '/usr/lib/zeppelin'

class Zeppelin(Generic):

    def __init__(self, zeppelin, *args, **kargs):
        self.zeppelin = zeppelin
        self.shiro = configparser.ConfigParser()
        self.shiro.read(os.path.join(ZEPPELIN_HOME, '/conf/shiro.ini'))
        (super().__init__)(*args, **kargs)

    def get_user(self):
        user = self.zeppelin.getInterpreterContext().getAuthenticationInfo().getUser()
        pwd = self.shiro['users'][user].split(',')[0]
        return dict(userName=user, password=pwd)

    def show(self, dataframe):
        self.zeppelin.show(dataframe)

    def command_aux(self, ISAContext):
        ISAMagic(ISAContext)

    def command_ml(self, MLContext):
        MLMagic(MLContext)