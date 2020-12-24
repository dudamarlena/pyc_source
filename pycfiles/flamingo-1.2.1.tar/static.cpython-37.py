# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/plugins/static.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 620 bytes
import os

class Static:

    def post_build(self, context):
        if context.settings.CONTENT_PATHS:
            return
        for static_dir in context.templating_engine.find_static_dirs():
            for root, dirs, files in os.walk(static_dir):
                for f in files:
                    source = os.path.join(root, f)
                    destination = os.path.join(context.settings.STATIC_ROOT, os.path.relpath(root, static_dir), f)
                    context.cp(source=source, destination=destination)