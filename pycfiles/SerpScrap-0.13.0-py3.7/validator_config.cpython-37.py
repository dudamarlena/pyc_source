# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\scrapcore\validator_config.py
# Compiled at: 2017-08-18 10:54:52
# Size of source mod 2**32: 1062 bytes
import scrapcore.tools as Error

class ValidatorConfig:

    def validate(self, config):
        if not isinstance(config, dict):
            raise Error('config is not a dict')
        else:
            if config.get('num_results_per_page') > 100:
                raise Error('num_results_per_page must be lower then 100')
            else:
                valid_search_types = [
                 'normal', 'video', 'news', 'image']
                if config.get('search_type') not in valid_search_types:
                    raise Error('Invalid search type!')
                if config.get('use_own_ip') != True and len(config.get('proxy_file')) == 0:
                    raise Error('No proxy_file provided and using own IP is disabled.')
            if config.get('scrape_method') not in 'selenium':
                raise Error('No such scrape_method {}'.format(config.get('scrape_method')))
            if not config.get('screenshot') is True or config.get('dir_screenshot') is None or len(config.get('dir_screenshot')) < 1:
                raise Error('No config dir_screenshot found')