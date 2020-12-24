# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_parser/common/tracker.py
# Compiled at: 2009-09-07 17:44:28
"""
Shared code for tracker parser.
"""
NOTE_NAME = {}
NOTES = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'G#', 'A', 'A#', 'B')
for octave in xrange(10):
    for (index, note) in enumerate(NOTES):
        NOTE_NAME[octave * 12 + index] = '%s (octave %s)' % (note, octave)