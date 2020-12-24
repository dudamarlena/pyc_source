# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/pyramid_rewrite/__init__.py
# Compiled at: 2012-02-05 06:38:08
__doc__ = "\nThis is a small pyramid extension that allows to add rules for rewriting\nthe PATH_INFO portion of a requested URL.\n\nUsage example:\n    def main(global_config, **settings):\n        config = Configurator(settings=settings)\n        config.include('pyramid_rewrite')\n        # add url rewriting rules...\n        #   first parameter is a regular expression\n        #   second parameter is the target url\n        config.add_rewrite_rule(r'/favicon.ico', r'/static/favicon.ico')\n        config.add_rewrite_rule(r'/gallery/(?P<subpath>.*)',\n                                r'/root/%(subpath)s')\n        #\n        # ... rest of configuration\n        #\n        # return WSGI application instance\n        return config.make_wsgi_app()\n"
import logging, re
from pyramid.events import NewRequest
logger = logging.getLogger(__name__)
__version__ = 0.2

def includeme(config):
    config.add_directive('add_rewrite_rule', add_rewrite_rule)


def add_rewrite_rule(config, pattern, target):
    tpattern = pattern
    if not pattern.startswith('^'):
        tpattern = '^' + tpattern
    if not pattern.endswith('$'):
        tpattern = tpattern + '$'
    cpattern = re.compile(tpattern)
    if not hasattr(config.registry, 'rewrite_rules'):
        config.registry.rewrite_rules = []
        config.add_subscriber(rewrite_subscriber, NewRequest)
    config.registry.rewrite_rules.append((pattern, cpattern, target))


def rewrite_subscriber(event):
    request = event.request
    for (pattern, cpattern, target) in request.registry.rewrite_rules:
        path_info = request.path_info
        logger.debug('Matching pattern "%s" against "%s" ' % (
         pattern, path_info))
        mo = cpattern.match(path_info)
        if mo is not None:
            path_info = target % mo.groupdict()
            logger.debug('Rewriting url: %s --> %s' % (
             request.path_info, path_info))
            request.path_info = path_info

    return