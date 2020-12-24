# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/service/beans_service.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 1269 bytes
import domain.exceptions, types

class BeanFactory(object):

    def __init__(self, app=None, *args, **kwargs):
        self._BeanFactory__app = app
        self._BeanFactory__beans = {}
        m = __import__('persist.beans', fromlist='persist')
        d = getattr(m, 'beans')
        self._BeanFactory__beans.update(d)
        m = __import__('service.beans', fromlist='service')
        d = getattr(m, 'beans')
        self._BeanFactory__beans.update(d)
        m = __import__('rest.beans', fromlist='rest')
        d = getattr(m, 'beans')
        self._BeanFactory__beans.update(d)

    def start(self, *args, **kwargs):
        for k, v in self._BeanFactory__beans.items():
            my_kwargs = {}
            init_method = v.__init__
            if isinstance(init_method, types.FunctionType):
                vn = init_method.__code__.co_varnames
                if 'app' in vn:
                    my_kwargs['app'] = self._BeanFactory__app
                self._BeanFactory__beans[k] = v(**my_kwargs)

    def get_bean(self, key, singleton=True, silence=False):
        bean = self._BeanFactory__beans.get(key, None)
        if bean is None:
            if not silence:
                raise domain.exceptions.NotFoundException('bean not found : ' + str(key))
            if singleton:
                pass
            return bean
        else:
            return bean.__class__()