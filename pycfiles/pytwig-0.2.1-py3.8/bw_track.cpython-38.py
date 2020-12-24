# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytwig/bw_track.py
# Compiled at: 2020-02-17 04:05:21
# Size of source mod 2**32: 1845 bytes
from pytwig import bw_object

class Track(bw_object.BW_Object):

    def __init__(self):
        super().__init__(classnum=144)

    def add_device_to_chain(self, device_preset, pos=-1):
        if pos < -1:
            pos = -1
        else:
            if self.get(356) == None:
                self.set(356, bw_object.BW_Object(138))
            if pos == -1:
                self.get(356).get(324).append(bw_object.BW_Object(163))
            else:
                if pos >= 0:
                    maxpos = len(self.get(356).get(324))
                    if pos > maxpos:
                        pos = maxpos
                    self.get(356).get(324).insert(pos, bw_object.BW_Object(163))
        self.get(356).get(324)[pos].set(407, device_preset)

    def set_main_clip(self, clip):
        self.get(350).get(561)[0].set(576, clip)
        return self

    def add_matrix_clip(self, clip, pos=-1):
        if self.get(350).get(561)[0].get(576) == None:
            self.get(350).get(561)[0].set(576, clip)
            return self
        else:
            if pos < -1:
                pos = -1
            if pos == -1:
                self.get(350).get(561).append(bw_object.BW_Object(227))
            else:
                if pos >= 0:
                    maxpos = len(self.get(1246))
                    if pos > maxpos:
                        pos = maxpos
                    self.get(350).get(561).insert(pos, bw_object.BW_Object(227))
        self.get(350).get(561)[pos].set(576, clip)
        return self


class Group_Track(bw_object.BW_Object):

    def __init__(self):
        super().__init__(classnum=477)

    def add_device_to_chain(self, device_preset, pos=-1):
        if self.get(1248) == None:
            self.set(1248, Track())
        self.get(1248).add_device_to_chain(device_preset, pos=pos)
        return self

    def set_main_clip(self, clip):
        raise SyntaxError('Cannot set main clip of a group track. I think.')
        return self

    def add_subtrack(self, track, pos=-1):
        if pos < -1:
            pos = -1
        elif pos == -1:
            self.get(1246).append(track)
        else:
            if pos >= 0:
                maxpos = len(self.get(1246))
                if pos > maxpos:
                    pos = maxpos
                self.get(1246).insert(pos, track)