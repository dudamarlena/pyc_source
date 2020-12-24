# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/blogdegins-data/www.artgins.es/htmlrendercode/page.py
# Compiled at: 2012-08-22 10:25:33
from ginsfsm.gobj import GObj
from ghtml.c_ghtml import GHtml
from ginsfsm.gconfig import add_gconfig
from assets import get_assets_env
from mymako import get_mako_lookup
page_data = {'title': 'ArtGins', 
   'base': 'http://www.artgins.com/', 
   'metadata': {'application-name': 'blog', 
                'description': '', 
                'keywords': ''}}

class Root(GObj):

    def __init__(self):
        super(Root, self).__init__({})


PAGE_GCONFIG = {'debug': [
           bool, False, 0, None, 'Debugging mode'], 
   'output_path': [
                 str, '', 0, None, 'Output directory (current tag).'], 
   'code_path': [
               str, '', 0, None, 'Code path.']}

class Page(GHtml):

    def __init__(self, fsm=None, gconfig=None):
        gconfig = add_gconfig(gconfig, PAGE_GCONFIG)
        super(Page, self).__init__(fsm=fsm, gconfig=gconfig)

    def render(self, **kw):
        mako_lookup = get_mako_lookup(self.code_path, self.output_path)
        assets_env = get_assets_env(self.code_path, self.output_path, self.debug)
        kw.update(**page_data)
        kw.update(assets_env=assets_env)
        return super(Page, self).render(mako_lookup=mako_lookup, **kw)


def get_page(code_path, output_path, debug):
    """ This is the only function being called from blogdegins.
        The rest is up to you.
        This function must return a class with a render method.
        The render method must return a string with the html code.
        :param code_path: path where python and templates code reside.
        :param output_path: current output tag directory.
        :param debug: True if you want debug.
    """
    gobj_root = Root()
    page = gobj_root.create_gobj(None, Page, gobj_root, template='page.mako', code_path=code_path, output_path=output_path, debug=debug)
    from content import create_content
    create_content(page)
    return page