# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mop/utils.py
# Compiled at: 2020-03-30 00:35:10
# Size of source mod 2**32: 1682 bytes
import logging, eyed3
from pathlib import Path
from typing import Optional
from eyed3.id3 import ID3_V1
from eyed3.core import AudioFile
log = logging.getLogger(__name__)

def eyed3_load(path) -> Optional[AudioFile]:
    """Wrapper for eyed3.load.
    Adds the following members to AudioFile:
    - is_dirty
    - second_v1_tag
    - selected_tag
    """
    audio_file = eyed3.load(path)
    if audio_file:
        if audio_file.info:
            log.debug(f"Handle audio file: {audio_file}")
            audio_file.second_v1_tag = None
            audio_file.selected_tag = None
            if audio_file.tag is None:
                audio_file.initTag()
            else:
                if audio_file.tag.isV2():
                    v1_audio_file = eyed3.load(path, tag_version=ID3_V1)
                    if v1_audio_file.tag:
                        log.debug('Found extra v1 tag')
                        audio_file.second_v1_tag = v1_audio_file.tag
                        audio_file.second_v1_tag.is_dirty = False
            audio_file.tag.is_dirty = False
            return audio_file
    log.debug(f"Handle file: {path}")
    return None


def eyed3_load_dir(audio_dir) -> list:

    class FileHandler(eyed3.utils.FileHandler):

        def __init__(self):
            self.audio_files = []

        def handleDirectory(self, d, files):
            for f in files:
                if (audio_file := eyed3_load(Path(d) / f)):
                    self.audio_files.append(audio_file)

    if audio_dir is not None:
        handler = FileHandler()
        eyed3.utils.walk(handler, audio_dir, recursive=True)
        return handler.audio_files