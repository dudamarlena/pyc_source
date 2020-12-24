# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/disko/.virtualenvs/ffl_website/src/kotti_video/kotti_video/__init__.py
# Compiled at: 2012-05-09 04:47:10
import logging
log = logging.getLogger(__name__)

def kotti_configure(settings):
    settings['kotti.includes'] += ' kotti_video.views'
    settings['kotti.available_types'] += ' kotti_video.resources.Video'
    settings['kotti.available_types'] += ' kotti_video.resources.Mp4File'
    settings['kotti.available_types'] += ' kotti_video.resources.WebmFile'
    settings['kotti.available_types'] += ' kotti_video.resources.OggFile'
    settings['kotti.available_types'] += ' kotti_video.resources.SubtitlesFile'
    settings['kotti.available_types'] += ' kotti_video.resources.ChaptersFile'