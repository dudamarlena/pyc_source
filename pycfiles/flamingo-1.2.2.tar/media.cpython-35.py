# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/plugins/media.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 1891 bytes
import logging, os
from flamingo.core.data_model import ContentSet, Content
logger = logging.getLogger('flamingo.core.media')

def add_media(context, content, name, **extra_meta_data):
    if name.startswith('/'):
        path = name[1:]
    else:
        path = os.path.join(os.path.dirname(content['path']), name)
    path = os.path.normpath(path)
    if name.startswith('/'):
        output = os.path.join(context.settings.MEDIA_ROOT, name[1:])
    else:
        output = os.path.join(context.settings.MEDIA_ROOT, os.path.dirname(content['path']), os.path.basename(name))
    url = '/' + output
    if not content['media']:
        content['media'] = ContentSet()
    media_content = Content(path=path, output=output, url=url, content=content, **extra_meta_data)
    content['media'].add(media_content)
    context.plugins.run_plugin_hook('media_added', content, media_content)
    logger.debug('%s added to %s', media_content['path'] or media_content, content['path'] or content)
    return media_content


class Media:

    def post_build(self, context):
        if context.settings.SKIP_FILE_OPERATIONS:
            return
        for content in context.contents:
            if not content['media']:
                pass
            else:
                for media in content['media']:
                    context.cp(source=os.path.join(context.settings.CONTENT_ROOT, media['path']), destination=os.path.join(context.settings.OUTPUT_ROOT, media['output']))