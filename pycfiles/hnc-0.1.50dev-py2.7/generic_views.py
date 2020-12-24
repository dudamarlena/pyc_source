# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\hnc\tools\generic_views.py
# Compiled at: 2013-10-17 07:54:00
from pyramid.decorator import reify
from pyramid.httpexceptions import HTTPFound

def logout_func(TOKEN, AnonUserCls):

    def logout(ctxt, req):
        if TOKEN in req.session:
            del req.session[TOKEN]
        ctxt.user = AnonUserCls()
        raise HTTPFound(location=req.resource_url(ctxt))

    return logout


class BaseContext(object):
    children = {}
    workflow = None

    def __init__(self, parent, name):
        self.__name__ = name
        self.__parent__ = parent

    def __getitem__(self, item):
        return self.children[item](self, item)

    @reify
    def settings(self):
        return self.__parent__.settings

    @reify
    def request(self):
        return self.__parent__.request

    @reify
    def __hierarchy__(self):
        result = []
        p = self
        while p:
            result.append(p)
            p = p.__parent__

        return result[::-1]

    def get_main_area(self):
        if len(self.__hierarchy__) > 1:
            return self.__hierarchy__[1]
        else:
            return

    main_area = reify(get_main_area)

    def get_area_url(self, *args, **kwargs):
        return self.request.resource_url(self.main_area, *args, **kwargs)

    def get_sub_area(self):
        if len(self.__hierarchy__) > 2:
            return self.__hierarchy__[2]
        else:
            return

    sub_area = reify(get_sub_area)