# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/utils/urls.py
# Compiled at: 2015-08-17 17:37:49


class UrlPatterns(object):
    """
        Возвращает патерн урлов с прописанным приложением и пространством
    имён
        Приложение и пространство имён по умолчанию равно названию приложения
    приведённому к нижнему регистру и заменёнными точками на нижние
    подчёркивания (если приложение часть иного модуля)

        При инициализации можно задать свои namespace и app_name
    """

    def __init__(self, namespace=None, app_name=None):
        self.app_name = app_name or ('_').join(self.__module__.split('.')[:-1]).lower()
        self.namespace = namespace or self.app_name

    def __call__(self):
        return (
         self.get_urlpatterns(), self.app_name, self.namespace)

    def get_urlpatterns(self):
        return self.urlpatterns