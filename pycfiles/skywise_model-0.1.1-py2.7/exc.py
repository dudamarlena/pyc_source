# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skywisemodel/exc.py
# Compiled at: 2017-05-19 14:29:52


class SkyWiseModelException(Exception):
    pass


class ModelAlreadyExistsException(SkyWiseModelException):
    pass


class ModelNotFound(SkyWiseModelException):
    pass


class ModelPlatformForecastProductAlreadyExists(SkyWiseModelException):
    pass