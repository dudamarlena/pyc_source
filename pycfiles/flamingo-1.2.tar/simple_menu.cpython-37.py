# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/simple_menu/simple_menu.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 2757 bytes
import logging, os
from flamingo.core.errors import MultipleObjectsReturned, ObjectDoesNotExist
from flamingo.core.data_model import Content, Q
logger = logging.getLogger('flamingo.plugins.SimpleMenu')

class SimpleMenu:
    THEME_PATHS = [
     os.path.join(os.path.dirname(__file__), 'theme')]

    def templating_engine_setup(self, context, templating_engine):

        def is_active(content, menu_item):
            return False

        def is_dict(v):
            return isinstance(v, dict)

        def is_list(v):
            return isinstance(v, list)

        templating_engine.env.globals['is_active'] = is_active
        templating_engine.env.globals['is_dict'] = is_dict
        templating_engine.env.globals['is_list'] = is_list

    def contents_parsed(self, context):

        def resolve_links(menu):
            for item in menu:
                name, url = item
                if isinstance(url, list):
                    resolve_links(url)
                else:
                    logger.debug('resolving %s', item[1])
                    try:
                        if isinstance(item[1], Content):
                            logger.debug('resolving skipped')
                            return
                        if isinstance(item[1], str):
                            lookup = Q(path=(item[1]))
                        else:
                            if not isinstance(item[1], Q):
                                lookup = Q(item[1])
                            else:
                                lookup = item[1]
                        item[1] = context.contents.get(lookup)
                        logger.debug('%s -> %s', lookup, item[1])
                    except ObjectDoesNotExist:
                        logger.error('no content with %s %s found', 'path' if isinstance(lookup, str) else 'lookup', lookup or repr(lookup))
                    except MultipleObjectsReturned:
                        logger.error('multiple contents found with %s %s found', 'path' if isinstance(lookup, str) else 'lookup', lookup or repr(lookup))

        if not hasattr(context.settings, 'MENU'):
            context.settings.MENU = {'main': []}
        else:
            if isinstance(context.settings.MENU, list):
                context.settings.MENU = {'main': context.settings.MENU}
            else:
                if 'main' not in context.settings.MENU:
                    context.settings.MENU['main'] = []
        for menu_name, menu in context.settings.MENU.items():
            resolve_links(menu)