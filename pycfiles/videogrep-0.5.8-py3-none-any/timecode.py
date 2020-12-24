# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sam/Dropbox/Projects/videogrep/build/lib/videogrep/timecode.py
# Compiled at: 2016-09-30 17:48:34
__version__ = '0.3.1'

class Timecode(object):

    def __init__(self, framerate, start_timecode=None, start_seconds=None, frames=None):
        """The main timecode class.

        Does all the calculation over frames, so the main data it holds is
        frames, then when required it converts the frames to a timecode by
        using the frame rate setting.

        :param str framerate: The frame rate of the Timecode instance. It
          should be one of ['23.98', '24', '25', '29.97', '30', '50', '59.94',
          '60', 'ms'] where "ms" equals to 1000 fps. Can not be skipped.
          Setting the framerate will automatically set the :attr:`.drop_frame`
          attribute to correct value.
        :param start_timecode: The start timecode. Use this to be able to
          set the timecode of this Timecode instance. It can be skipped and
          then the frames attribute will define the timecode, and if it is also
          skipped then the start_second attribute will define the start
          timecode, and if start_seconds is also skipped then the default value
          of '00:00:00:00' will be used.
        :type start_timecode: str or None
        :param start_seconds: A float or integer value showing the seconds.
        :param int frames: Timecode objects can be initialized with an
          integer number showing the total frames.
        """
        self.drop_frame = False
        self._int_framerate = None
        self._framerate = None
        self.framerate = framerate
        self.frames = None
        if start_timecode:
            self.frames = self.tc_to_frames(start_timecode)
        elif frames is not None:
            self.frames = frames
        elif start_seconds is not None:
            self.frames = self.float_to_tc(start_seconds)
        else:
            self.frames = self.tc_to_frames('00:00:00:00')
        return

    @property
    def framerate(self):
        """getter for _framerate attribute
        """
        return self._framerate

    @framerate.setter
    def framerate(self, framerate):
        """setter for the framerate attribute
        :param framerate:
        :return:
        """
        if framerate == '29.97':
            self._int_framerate = 30
            self.drop_frame = True
        elif framerate == '59.94':
            self._int_framerate = 60
            self.drop_frame = True
        elif framerate == '23.98':
            self._int_framerate = 24
        elif framerate == 'ms':
            self._int_framerate = 1000
            framerate = 1000
        elif framerate == 'frames':
            self._int_framerate = 1
        else:
            self._int_framerate = int(framerate)
        self._framerate = framerate

    def set_timecode(self, timecode):
        """Sets the frames by using the given timecode
        """
        self.frames = self.tc_to_frames(timecode)

    def float_to_tc(self, seconds):
        """set the frames by using the given seconds
        """
        return int(seconds * self._int_framerate)

    def tc_to_frames(self, timecode):
        """Converts the given timecode to frames
        """
        hours, minutes, seconds, frames = map(int, timecode.split(':'))
        ffps = float(self._framerate)
        if self.drop_frame:
            drop_frames = int(round(ffps * 0.066666))
        else:
            drop_frames = 0
        ifps = self._int_framerate
        hour_frames = ifps * 60 * 60
        minute_frames = ifps * 60
        total_minutes = 60 * hours + minutes
        frame_number = hour_frames * hours + minute_frames * minutes + ifps * seconds + frames - drop_frames * (total_minutes - total_minutes // 10)
        frames = frame_number + 1
        return frames

    def frames_to_tc(self, frames):
        """Converts frames back to timecode

        :returns str: the string representation of the current time code
        """
        if frames == 0:
            return (0, 0, 0, 0)
        ffps = float(self._framerate)
        if self.drop_frame:
            drop_frames = int(round(ffps * 0.066666))
        else:
            drop_frames = 0
        frames_per_hour = int(round(ffps * 60 * 60))
        frames_per_24_hours = frames_per_hour * 24
        frames_per_10_minutes = int(round(ffps * 60 * 10))
        frames_per_minute = int(round(ffps) * 60) - drop_frames
        frame_number = frames - 1
        if frame_number < 0:
            frame_number += frames_per_24_hours
        frame_number %= frames_per_24_hours
        if self.drop_frame:
            d = frame_number // frames_per_10_minutes
            m = frame_number % frames_per_10_minutes
            if m > drop_frames:
                frame_number += drop_frames * 9 * d + drop_frames * ((m - drop_frames) // frames_per_minute)
            else:
                frame_number += drop_frames * 9 * d
        ifps = self._int_framerate
        frs = frame_number % ifps
        secs = frame_number // ifps % 60
        mins = frame_number // ifps // 60 % 60
        hrs = frame_number // ifps // 60 // 60
        return (
         hrs, mins, secs, frs)

    @classmethod
    def parse_timecode(cls, timecode):
        """parses timecode string frames '00:00:00:00' or '00:00:00;00' or
        milliseconds '00:00:00:000'
        """
        bfr = timecode.replace(';', ':').replace('.', ':').split(':')
        hrs = int(bfr[0])
        mins = int(bfr[1])
        secs = int(bfr[2])
        frs = int(bfr[3])
        return (hrs, mins, secs, frs)

    def __iter__(self):
        return self

    def next(self):
        self.add_frames(1)
        return self

    def back(self):
        self.sub_frames(1)
        return self

    def add_frames(self, frames):
        """adds or subtracts frames number of frames
        """
        self.frames += frames

    def sub_frames(self, frames):
        """adds or subtracts frames number of frames
        """
        self.add_frames(-frames)

    def mult_frames(self, frames):
        """multiply frames
        """
        self.frames *= frames

    def div_frames(self, frames):
        """adds or subtracts frames number of frames"""
        self.frames = self.frames / frames

    def __eq__(self, other):
        """the overridden equality operator
        """
        if isinstance(other, Timecode):
            return self._framerate == other._framerate and self.frames == other.frames
        if isinstance(other, str):
            new_tc = Timecode(self._framerate, other)
            return self.__eq__(new_tc)
        if isinstance(other, int):
            return self.frames == other

    def __add__(self, other):
        """returns new Timecode instance with the given timecode or frames
        added to this one
        """
        tc = Timecode(self._framerate, frames=self.frames)
        if isinstance(other, Timecode):
            tc.add_frames(other.frames)
        elif isinstance(other, int):
            tc.add_frames(other)
        else:
            raise TimecodeError('Type %s not supported for arithmetic.' % other.__class__.__name__)
        return tc

    def __sub__(self, other):
        """returns new Timecode object with added timecodes"""
        if isinstance(other, Timecode):
            subtracted_frames = self.frames - other.frames
        elif isinstance(other, int):
            subtracted_frames = self.frames - other
        else:
            raise TimecodeError('Type %s not supported for arithmetic.' % other.__class__.__name__)
        return Timecode(self._framerate, start_timecode=None, frames=subtracted_frames)

    def __mul__(self, other):
        """returns new Timecode object with added timecodes"""
        if isinstance(other, Timecode):
            multiplied_frames = self.frames * other.frames
        elif isinstance(other, int):
            multiplied_frames = self.frames * other
        else:
            raise TimecodeError('Type %s not supported for arithmetic.' % other.__class__.__name__)
        return Timecode(self._framerate, start_timecode=None, frames=multiplied_frames)

    def __div__(self, other):
        """returns new Timecode object with added timecodes"""
        if isinstance(other, Timecode):
            div_frames = self.frames / other.frames
        elif isinstance(other, int):
            div_frames = self.frames / other
        else:
            raise TimecodeError('Type %s not supported for arithmetic.' % other.__class__.__name__)
        return Timecode(self._framerate, start_timecode=None, frames=div_frames)

    def __repr__(self):
        return '%02d:%02d:%02d:%02d' % self.frames_to_tc(self.frames)

    @property
    def hrs(self):
        hrs, mins, secs, frs = self.frames_to_tc(self.frames)
        return hrs

    @property
    def mins(self):
        hrs, mins, secs, frs = self.frames_to_tc(self.frames)
        return mins

    @property
    def secs(self):
        hrs, mins, secs, frs = self.frames_to_tc(self.frames)
        return secs

    @property
    def frs(self):
        hrs, mins, secs, frs = self.frames_to_tc(self.frames)
        return frs

    @property
    def frame_number(self):
        """returns the 0 based frame number of the current timecode instance
        """
        return self.frames - 1


class TimecodeError(Exception):
    """Raised when an error occurred in timecode calculation
    """
    pass