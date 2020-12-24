# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/iberia/frontends/wibterm/wibterm/htmlrendercode/ibterm/aplic/aplic.py
# Compiled at: 2013-06-19 10:39:45
from ghtml.c_ghtml import GHtml
from ginsfsm.gconfig import add_gconfig
aplic_data = {'myname': 'Blogdegins.'}
Aplic_CONFIG = {'gxxxx_namespace': [
                     str, '', 0, None,
                     'namespace of gxxxx, to store callbacks.'], 
   'aplic_options': [
                   dict, {},
                   0,
                   None,
                   'A dictionary containing the javascript options.']}

class Aplic(GHtml):

    def __init__(self, fsm=None, gconfig=None):
        gconfig = add_gconfig(gconfig, Aplic_CONFIG)
        super(Aplic, self).__init__(fsm=fsm, gconfig=gconfig)

    def start_up(self):
        pass

    def render(self, **kw):
        kw.update(**aplic_data)
        return super(Aplic, self).render(**kw)


def create_aplic(name, parent, **kw):
    """ Remember put in parent python code:

        from aplic import create_aplic
        create_aplic(
            'aplic',  # the name you have to put in parent mako: ${aplic}
            self,
        )
    """
    aplic = parent.create_gobj(name, Aplic, parent, template=('/%s/htmlrendercode/ibterm/aplic/aplic.mako' % __package__.split('.')[0]), **kw)
    return aplic