# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/Obsidian/ddsourcejsonconfig.py
# Compiled at: 2016-09-12 07:33:36
# Size of source mod 2**32: 856 bytes
import json
from Obsidian.ddsourceconfig import DDSourceConfig

class DDSourceJsonConfig(DDSourceConfig):

    def __init__(self, filename=''):
        if len(filename) == 0:
            return
        with open(filename) as (data_file):
            config = json.load(data_file)
            self.name = config['name']
            self.allowed_domains = config['allowed_domains']
            self.start_urls = config['start_urls']
            self.prefix = config['prefix']
            self.link_array_pipline = config['link_array_pipline']
            self.main_content_pipline = config['main_content_pipline']
            self.item_pipline = config['item_pipline']
            self.entry = config['entry']