# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/plugins/meta_data.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 813 bytes
import os

class MetaDataDefaults:

    def contents_parsed(self, context):
        for content in context.contents:
            if not content['output']:
                content['output'] = os.path.splitext(content['path'])[0] + '.html'
            else:
                content['url'] = os.path.join('/', content['output'])
                if not content['template']:
                    content['template'] = context.settings.DEFAULT_TEMPLATE
                if not content['title']:
                    content['title'] = ''
                content['content_title'] = content['content_title'] or ''
            if not content['content_body']:
                content['content_body'] = ''