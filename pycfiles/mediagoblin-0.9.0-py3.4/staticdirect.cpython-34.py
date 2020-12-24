# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/staticdirect.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 3615 bytes
import logging, six
_log = logging.getLogger(__name__)

class StaticDirect(object):
    __doc__ = '\n    Direct to a static resource.\n\n    This StaticDirect class can take a series of "domains" to\n    staticdirect to.  In general, you should supply a None domain, as\n    that\'s the "default" domain.\n\n    Things work like this::\n\n      >>> staticdirect = StaticDirect(\n      ...     {None: "/static/",\n      ...      "theme": "http://example.org/themestatic/"})\n      >>> staticdirect("css/monkeys.css")\n      "/static/css/monkeys.css"\n      >>> staticdirect("images/lollerskate.png", "theme")\n      "http://example.org/themestatic/images/lollerskate.png"\n    '

    def __init__(self, domains):
        self.domains = dict([(key, value.rstrip('/')) for key, value in six.iteritems(domains)])
        self.cache = {}

    def __call__(self, filepath, domain=None):
        if domain in self.cache and filepath in self.cache[domain]:
            return self.cache[domain][filepath]
        static_direction = self.cache.setdefault(domain, {})[filepath] = self.get(filepath, domain)
        return static_direction

    def get(self, filepath, domain=None):
        return '%s/%s' % (
         self.domains[domain], filepath.lstrip('/'))


class PluginStatic(object):
    __doc__ = 'Pass this into the ``\'static_setup\'`` hook to register your\n    plugin\'s static directory.\n\n    This has two mandatory attributes that you must pass in on class\n    init:\n\n    - *name:* this name will be both used for lookup in "urlgen" for\n      your plugin\'s static resources and for the subdirectory that\n      it\'ll be "mounted" to for serving via your web browser.  It\n      *MUST* be unique.  If writing a plugin bundled with MediaGoblin\n      please use the pattern \'coreplugin__foo\' where \'foo\' is your\n      plugin name.  All external plugins should use their modulename,\n      so if your plugin is \'mg_bettertags\' you should also call this\n      name \'mg_bettertags\'.\n    - *file_path:* the directory your plugin\'s static resources are\n      located in.  It\'s recommended that you use\n      pkg_resources.resource_filename() for this.\n\n    An example of using this::\n\n      from pkg_resources import resource_filename\n      from mediagoblin.tools.staticdirect import PluginStatic\n\n      hooks = {\n          \'static_setup\': lambda: PluginStatic(\n              \'mg_bettertags\',\n              resource_filename(\'mg_bettertags\', \'static\'))\n      }\n\n    '

    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path

    def __call__(self):
        return self