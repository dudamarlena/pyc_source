# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/containerdiff/filter.py
# Compiled at: 2016-05-22 16:04:40
# Size of source mod 2**32: 2874 bytes
"""Filter an output of modules."""
import logging, re
logger = logging.getLogger(__name__)

def filter_output(data, options):
    """Filter an output of a module.

    'data' - data to filter (dict or list)
    'option' - filtering options (see filter.json for example or
               documentation of containerdiff)

    Return value are filtered data. In case of any error it returns
    unmodified data.
    """
    if 'action' not in options or not isinstance(options['action'], str):
        logger.error('Filter: wrong or missing "action" key in filter options')
        return data
    if 'data' not in options or not isinstance(options['data'], list):
        logger.error('Filter: wrong or missing "data" key in filter options')
        return data
    if 'keys' in options:
        if not isinstance(data, dict):
            logger.error('Filter: "keys" filter option specified but filtered data is not dictionary')
            return data
        for key in options['keys']:
            if key not in data:
                logger.warning('Filter: in filtered data there is no key ' + key)
                break
            data[key] = filter_output(data[key], {'action': options['action'],  'data': options['data']})

    else:
        if not isinstance(data, list):
            logger.error('Filter: output of the module is not a list')
            return data
        if len(options['data']) == 0:
            logger.warning('Filter: "data" filter option is empty')
            return data
        pattern = re.compile('|'.join(options['data']))
        if options['action'] == 'include':
            data = list(filter(lambda item: pattern.search(str(item)), data))
        elif options['action'] == 'exclude':
            data = list(filter(lambda item: not pattern.search(str(item)), data))
    return data