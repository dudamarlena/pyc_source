# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/obsolete.py
# Compiled at: 2007-12-02 16:26:56
from salamoia.h2o.exception import *

def obsolete(func):
    name = func.func_name

    def obs(*args, **kwargs):
        raise ObsoleteException, '%s is obsolete' % name

    obs.func_name = name
    return obs


def willobsolete(func):
    name = func.func_name

    def obs(*args, **kwargs):
        from salamoia.h2o.logioni import Ione
        Ione.warning('%s will be obsoleted', name)
        return func(*args, **kwargs)

    obs.func_name = name
    return obs


from salamoia.tests import *
runDocTests()