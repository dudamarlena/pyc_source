# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cblog/widgets/gravatar/gravatar.py
# Compiled at: 2006-12-15 15:44:26
__doc__ = "TurboGears widget for gravatars (globally recognized user icons).\n\nSee <http://gravatar.com/implement.php> for more info.\n\nUsage\n-----\n\nController::\n\n    from gravatar import Gravatar\n\n    class Root:\n        @expose()\n        def index(self):\n            return {'gravatar': Gravatar(size=50)}\n\nTemplate::\n\n    ${gravatar.display('joe@foo.com')}\n"
__all__ = [
 'Gravatar', 'GravatarController']
import md5, os
from os.path import exists, join
from urllib import quote_plus, unquote
import pkg_resources, cherrypy
from turbogears import config, controllers, expose, redirect, url
from turbogears.widgets import *
from cblog.widgets import jslibs
js_dir = pkg_resources.resource_filename('cblog.widgets.gravatar', 'static/javascript')
register_static_directory('gravatar', js_dir)
GRAVATAR_WIDGET_JS = "\n/* Hide gravatar icons initially only when Javascript is enabled */\ndocument.write('<style>.gravatar {display: none;}</style>');\n"

class Gravatar(Widget):
    """A gravatar icon representing a user in a blog comment/forum post/etc."""
    __module__ = __name__
    name = 'gravatar'
    template = '    <img xmlns:py="http://purl.org/kid/ns#" py:if="hash"\n      width="${size}" height="${size}" py:attrs="attrs"\n      src="${url}?gravatar_id=${hash}&amp;size=${size}${rating}${default}" />\n    '
    params = [
     'attrs', 'default', 'rating', 'size', 'url']
    attrs = {}
    rating = 'R'
    default = None
    url = 'http://www.gravatar.com/avatar.php'
    size = 80
    javascript = [
     jslibs.events, JSLink('gravatar', 'gravatar.js'), JSSource(GRAVATAR_WIDGET_JS, js_location.head)]
    params_doc = dict(attrs='Dictionary containing extra (X)HTML attributes for the IMG tag', default='URL of default image to return if gravatar is not available.', rating='Highest acceptable rating of returned gravatar (G|PG|R|X)', size='Size of returned gravatar image in pixels.', url='URL of gravatar server. Default: %s' % url)

    def update_params(self, params):
        """Builds hash from email given on widget display & creates gravatar URL.
        """
        super(Gravatar, self).update_params(params)
        email = params.get('value')
        if email:
            params['hash'] = md5.new(email).hexdigest()
        else:
            params['hash'] = None
        default = params.get('default')
        if default:
            params['default'] = '&default=%s' % quote_plus(default)
        rating = params.get('rating')
        if rating in ['G', 'PG', 'R', 'X']:
            params['rating'] = '&rating=%s' % rating
        else:
            params['rating']
        params['url'] = url(params['url'])
        params['attrs'].setdefault('class', 'gravatar')
        return


import logging
log = logging.getLogger('cblog.controllers')

class GravatarController(controllers.Controller):
    __module__ = __name__

    def __init__(self, cache_dir=None, mirror=Gravatar.url):
        self.cache_dir = cache_dir
        if not cache_dir:
            self.cache_dir = join(config.get('static_filter.dir', path='/static'), 'images', 'gravatars')
        self.mirror = mirror
        if self.cache_dir:
            cherrypy.config.update({'/gravatars': {'static_filter.on': True, 'static_filter.dir': self.cache_dir}})
        self.on_cache_miss = config.get('gravatars.on_cache_miss', 'redirect')

    expose()

    def default(self, gravatar_id=None, size=80, rating='R', default=None):
        if not gravatar_id:
            raise cherrypy.NotFound
        suffix = '?gravatar_id=%s&size=%s&rating=%s' % (gravatar_id, size, rating)
        gid = md5.new(suffix).hexdigest()
        if not self.cache_dir or not os.access(join(self.cache_dir, gid + '.png'), os.R_OK):
            log.info('Gravatar request: %s' % suffix)
            if default:
                if self.on_cache_miss == 'default':
                    redirect(default)
                suffix += '&default=%s' % default
            redirect(self.mirror + suffix)
        else:
            redirect('/gravatars/%s.png' % gid)