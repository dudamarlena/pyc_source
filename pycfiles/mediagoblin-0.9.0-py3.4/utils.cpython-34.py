# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/plugins/archivalook/utils.py
# Compiled at: 2014-09-16 18:42:02
# Size of source mod 2**32: 1172 bytes
from mediagoblin.tools.pluginapi import hook_handle

def feature_template(media, feature_type):
    """
    Get the feature template for this media
    """
    template_name = hook_handle((
     'feature_%s_template' % feature_type, media.media_type))
    if template_name is None:
        return '/archivalook/feature_displays/default_%s.html' % feature_type
    return template_name