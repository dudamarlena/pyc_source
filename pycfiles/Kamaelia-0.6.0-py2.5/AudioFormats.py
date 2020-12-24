# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/PyMedia/AudioFormats.py
# Compiled at: 2008-10-19 12:19:52
import pymedia.audio.sound as sound
format2PyMediaFormat = {'AC3': sound.AFMT_AC3, 
   'A_LAW': sound.AFMT_A_LAW, 
   'IMA_ADPCM': sound.AFMT_IMA_ADPCM, 
   'MPEG': sound.AFMT_MPEG, 
   'MU_LAW': sound.AFMT_MU_LAW, 
   'S16_BE': sound.AFMT_S16_BE, 
   'S16_LE': sound.AFMT_S16_LE, 
   'S16_NE': sound.AFMT_S16_NE, 
   'S8': sound.AFMT_S8, 
   'U16_BE': sound.AFMT_U16_BE, 
   'U16_LE': sound.AFMT_U16_LE, 
   'U8': sound.AFMT_U8}
pyMediaFormat2format = dict([ (v, k) for (k, v) in format2PyMediaFormat.items() ])
format2BytesPerSample = {'AC3': None, 
   'A_LAW': 1, 
   'IMA_ADPCM': 0.5, 
   'MPEG': None, 
   'MU_LAW': 1, 
   'S16_BE': 2, 
   'S16_LE': 2, 
   'S16_NE': 2, 
   'S8': 1, 
   'U16_BE': 2, 
   'U16_LE': 2, 
   'U8': 1}
codec2fileExt = {'MP3': 'mp3', 
   'mp3': 'mp3', 
   'Mp3': 'mp3'}
codec2PyMediaCodec = {'MP3': 'mp3', 
   'mp3': 'mp3', 
   'Mp3': 'mp3'}