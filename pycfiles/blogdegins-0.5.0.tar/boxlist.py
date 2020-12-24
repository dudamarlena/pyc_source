# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/blogdegins-data/www.artgins.es/htmlrendercode/widgets/boxlist/boxlist.py
# Compiled at: 2012-08-22 05:05:21
from ghtml.c_ghtml import GHtml
boxlist_data = {'myname': 'Blogdegins.'}

class Boxlist(GHtml):

    def __init__(self, fsm=None, gconfig=None):
        super(Boxlist, self).__init__(fsm=fsm, gconfig=gconfig)

    def render(self, **kw):
        kw.update(**boxlist_data)
        return super(Boxlist, self).render(**kw)


def create_boxlist(parent):
    boxlist = parent.create_gobj(None, Boxlist, parent, template='widgets/boxlist/boxlist.mako')
    return boxlist