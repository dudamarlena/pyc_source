# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange_django/context_processors.py
# Compiled at: 2011-05-12 16:12:43
from linkexchange_django import support
from linkexchange.utils import rearrange_blocks, parse_rearrange_map

def linkexchange(request):
    if support.platform is None:
        return {}
    else:
        page_request = support.convert_request(request)
        result = {}
        if support.formatters:
            result['linkexchange_blocks'] = support.platform.get_blocks(page_request, support.formatters)
            try:
                rearrange_map = parse_rearrange_map(support.options['rearrange_map'])
            except KeyError:
                pass
            except ValueError:
                log.warning('Unable to parse rearrange_map')
            else:
                result['linkexchange_blocks'] = rearrange_blocks(page_request, result['linkexchange_blocks'], rearrange_map)

        if support.options.get('use_raw_links', False):
            result['linkexchange_links'] = support.platform.get_raw_links(page_request)
        return result