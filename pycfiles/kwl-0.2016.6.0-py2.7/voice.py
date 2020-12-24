# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/voice.py
# Compiled at: 2016-03-16 19:51:06
"""Allow customization of standard output into idiosyncratic forms."""
import data, pronounce as p

def get_voices(language):
    """Print out list of available voices in this language."""
    pass


def apply_voice(language, voice, surface):
    """Apply the substitutions of this particular voice."""
    subs = data.get_voice_substitutions(language, voice)
    return p.find_and_replace(surface, subs)