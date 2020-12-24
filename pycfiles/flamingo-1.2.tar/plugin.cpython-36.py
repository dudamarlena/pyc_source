# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/rtd/plugin.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 404 bytes
import json, os

class ReadTheDocs:
    THEME_PATHS = [
     os.path.join(os.path.dirname(__file__), 'theme')]

    def templating_engine_setup(self, context, templating_engine):
        context.settings.EXTRA_CONTEXT['json'] = json

    def contents_parsed(self, context):
        context.contents.add(template='rtd/search.html',
          output='search.html')