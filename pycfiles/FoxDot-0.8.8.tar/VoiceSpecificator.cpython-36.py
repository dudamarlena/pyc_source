# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Ryan\Documents\GitHub\FoxDot\FoxDot\lib\Extensions\VRender\VoiceSpecificator.py
# Compiled at: 2018-08-29 05:13:03
# Size of source mod 2**32: 920 bytes
import math, sys

def generateVoiceSpecification(lyrics, tempo, inputMusicXMLPath, outputMusicXMLPath):
    with open(inputMusicXMLPath, 'r') as (c):
        content = [x.strip() for x in c.readlines()]
        with open(outputMusicXMLPath, 'w') as (f):
            f.write(addVoiceTags(tempo, lyrics, content))


def addVoiceTags(tempo, text, content):
    print('Text:\n' + str(text))
    output = ''
    tempo_xml = '<direction>\n<sound tempo="{}"/>\n</direction>'.format(tempo)
    lyrics_xml = '<voice>1</voice>\n<lyric>\n<text>{}</text>\n</lyric>'
    i = 0
    ignoreThisNote = False
    for line in content:
        if '<rest/>' in line:
            ignoreThisNote = True
        if '</note' in line:
            if not ignoreThisNote:
                output += lyrics_xml.format(text[(i % len(text))])
                i += 1
            else:
                ignoreThisNote = False
            output += line
            if tempo != -1 and '<measure' in line:
                output += tempo_xml

    return output