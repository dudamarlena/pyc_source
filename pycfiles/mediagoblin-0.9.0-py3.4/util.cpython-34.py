# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/media_types/video/util.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 2797 bytes
import logging
from mediagoblin import mg_globals as mgg
_log = logging.getLogger(__name__)

def skip_transcode(metadata, size):
    """
    Checks video metadata against configuration values for skip_transcode.

    Returns True if the video matches the requirements in the configuration.
    """
    config = mgg.global_config['plugins']['mediagoblin.media_types.video']['skip_transcode']
    medium_config = mgg.global_config['media:medium']
    _log.debug('skip_transcode config: {0}'.format(config))
    metadata_tags = metadata.get_tags()
    if not metadata_tags:
        return False
    if config['mime_types']:
        if metadata_tags.get_string('mimetype')[0] and metadata_tags.get_string('mimetype')[1] not in config['mime_types']:
            return False
    if config['container_formats']:
        if metadata_tags.get_string('container-format')[0] and metadata_tags.get_string('container-format')[1] not in config['container_formats']:
            return False
    if config['video_codecs']:
        for video_info in metadata.get_video_streams():
            video_tags = video_info.get_tags()
            if not video_tags:
                return False
            if video_tags.get_string('video-codec')[1] not in config['video_codecs']:
                return False

    if config['audio_codecs']:
        for audio_info in metadata.get_audio_streams():
            audio_tags = audio_info.get_tags()
            if not audio_tags:
                return False
            if audio_tags.get_string('audio-codec')[1] not in config['audio_codecs']:
                return False

    if config['dimensions_match']:
        for video_info in metadata.get_video_streams():
            if not video_info.get_height() <= size[1]:
                return False
            if not video_info.get_width() <= size[0]:
                return False

    return True