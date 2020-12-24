# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/chippy/mmlparser.py
# Compiled at: 2016-08-22 08:57:16
# Size of source mod 2**32: 3226 bytes


class MMLParser(object):

    def __init__(self, tempo=120, octave=4, length=4, volume=10):
        self.tempo = tempo
        self.octave = octave
        self.reverse_octave = False
        self.length = length
        self.volume = volume
        self.raw_mml_data = []
        self.mml_title = None
        self.mml_composer = None
        self.mml_programmer = None
        self.notes = {'C': 261.63, 'C#': 277.183, 
         'D': 293.66, 'D#': 311.127, 
         'E': 329.63, 
         'F': 349.23, 'F#': 369.994, 
         'G': 392.0, 'G#': 415.305, 
         'A': 440.0, 'A#': 466.164, 
         'B': 493.88, 'R': 0.1}
        self.current_channel = None
        self.channel_a_queue = []
        self.channel_b_queue = []
        self.channel_c_queue = []
        self.channel_d_queue = []
        self.channel_e_queue = []

    def _parse_header(self):
        for line in self.raw_mml_data:
            if line.startswith('#INCLUDE'):
                continue
            if line.startswith('#TITLE'):
                self.mml_title = line[7:]
            elif line.startswith('#COMPOSER'):
                self.mml_composer = line[10:]
            else:
                if line.startswith('#PROGRAMER'):
                    self.mml_programmer = line[11:]
                else:
                    if line.startswith('#PROGRAMMER'):
                        self.mml_programmer = line[11:]
                    elif line.startswith('#OCTAVE-REV'):
                        self.reverse_octave = True

    def _set_channel(self, line):
        if line.startswith('#'):
            return
        if line.startswith('A '):
            self.current_channel = self.channel_a_queue
        else:
            if line.startswith('B '):
                self.current_channel = self.channel_b_queue
            else:
                if line.startswith('C '):
                    self.current_channel = self.channel_c_queue
                else:
                    if line.startswith('D '):
                        self.current_channel = self.channel_d_queue
                    else:
                        if line.startswith('E '):
                            self.current_channel = self.channel_e_queue
                        else:
                            self.current_channel = self.channel_a_queue

    def load_file(self, file_name):
        with open(file_name) as (f):
            for line in f.readlines():
                self.raw_mml_data.append(line.strip())

        self._parse_header()

    def parse_line(self, line):
        self._set_channel(line)
        for character in line:
            if character.upper() in self.notes.keys():
                freq = self.notes[character.upper()]
                leng = 60 / self.tempo
                self.current_channel.append((leng, freq))