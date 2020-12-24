# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/MoinMoin/macro/LinkExchangeBlock.py
# Compiled at: 2011-05-12 16:28:43
import logging
from linkexchange.MoinMoin import support
from linkexchange.utils import rearrange_blocks, parse_rearrange_map
log = logging.getLogger('linkexchange.MoinMoin')
Dependencies = [
 'time']

def execute(macro, num):
    request = macro.request
    cfg = request.cfg
    try:
        num = int(num)
    except (TypeError, ValueError):
        log.error('LinkExchangeBlock requires a single numeric argument')
        return 'Required single numeric argument!'

    try:
        platform = cfg.linkexchange_platform
    except AttributeError:
        support.configure(cfg)
        platform = cfg.linkexchange_platform

    if platform is None:
        return ''
    else:
        formatters = getattr(cfg, 'linkexchange_formatters', None)
        if not formatters:
            log.error('No formatters defined for LinkExchangeBlock')
            return 'No formatters defined!'
        try:
            return request.linkexchange_blocks[num]
        except AttributeError:
            pass

        page_request = support.convert_request(request)
        request.linkexchange_blocks = platform.get_blocks(page_request, formatters)
        try:
            rearrange_map = parse_rearrange_map(cfg.linkexchange_options['rearrange_map'])
        except KeyError:
            pass
        except ValueError:
            log.warning('Unable to parse rearrange_map')
        else:
            request.linkexchange_blocks = rearrange_blocks(page_request, request.linkexchange_blocks, rearrange_map)

        return request.linkexchange_blocks[num]