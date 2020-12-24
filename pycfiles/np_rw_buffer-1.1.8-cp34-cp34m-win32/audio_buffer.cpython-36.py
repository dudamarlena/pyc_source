# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\repos\testlibs\np_rw_buffer\np_rw_buffer\audio_buffer.py
# Compiled at: 2020-02-17 15:26:19
# Size of source mod 2**32: 11093 bytes
import numpy as np
from .utils import make_thread_safe
from .buffer import RingBuffer, RingBufferThreadSafe, UnderflowError
__all__ = [
 'UnderflowError', 'AudioFramingBuffer']

class AudioFramingBuffer(RingBufferThreadSafe):
    __doc__ = "The Audio Framing Buffer differs from the RingBuffer by the read and write methods.\n\n    You can have a negative length and the write will always write in the correct\n    position (where it was left off). This helps keep read at the proper position. The\n    read pointer always moves with the read data. It doesn't care how much data is in the buffer.\n    After it reads it back-fills zeros, so if it wraps around in the reading it will read those\n    zeros again. This completely decouples the read from the write unless the read wraps around a\n    second time. Then the write might not be caught up and issues may arise. We are not worried\n    about that yet.\n\n    Users should not have to set the shape or the maxsize values. Users should only set the sample\n    rate, seconds, and buffer delay.\n\n    Example:\n\n        ..code-block :: python\n\n            >>> buffer = AudioFramingBuffer(2000, 1)\n            >>> buffer.write(np.array([(i,) for i in range(10)]))\n            >>> # Buffer: [(read ptr)0, 1, 2, 3, 4, 5, 6, 7, 8, 9, (write ptr) 0, 0, 0, 0, 0]\n            >>> buffer.read(15)\n            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, (write ptr) 0, 0, 0, 0, 0] (read ptr at end)\n            >>> buffer.write(np.array([(i,) for i in range(10)])) # This will write in the position after 19\n            >>> # Buffer: [0, 0, 0, 0, 0, 0, 0, 0, 0, (was 9) 0, 0, 1, 2, 3, 4, (read ptr) 5, 6, 7, 8, 9] (write ptr at end)\n            >>> buffer.read(10)\n            [5, 6, 7, 8, 9, (write ptr) 0, 0, 0, 0, 0] (read ptr at end)\n    "

    def __init__(self, sample_rate=22050.0, channels=1, seconds=2, buffer_delay=0, dtype=np.float32):
        if isinstance(sample_rate, (tuple, list)):
            channels = sample_rate[1]
            length = sample_rate[0]
            sample_rate = length / seconds
        self._sample_rate = sample_rate
        self._buffer_delay = buffer_delay
        self._seconds = seconds
        self.read_frame = 0
        self.write_frame = 0
        self.can_read = not self._buffer_delay > 0
        self._sample_counter = 0
        length = np.ceil(self._sample_rate * self._seconds)
        super().__init__(shape=(length, channels), dtype=dtype)

    channels = RingBufferThreadSafe.columns

    @make_thread_safe
    def get_sample_rate(self):
        """Return the rate of the data in Hz."""
        return self._sample_rate

    @make_thread_safe
    def set_sample_rate(self, rate):
        """Set the buffer's sample rate. This helps synchronize the buffer size with the total
        seconds.

        Note:
            This method will try to reset the buffer size from set_data.
        """
        self._sample_rate = rate
        self.maxsize = np.ceil(self._sample_rate * self._seconds)

    sample_rate = property(get_sample_rate, set_sample_rate)

    @property
    @make_thread_safe
    def seconds(self):
        """Return the total number of seconds that the buffer can hold."""
        return self._seconds

    @seconds.setter
    @make_thread_safe
    def seconds(self, seconds):
        """Set the total number of seconds that the buffer can hold."""
        self._seconds = seconds
        self.maxsize = np.ceil(self.get_sample_rate() * self._seconds)
        if self.seconds < self.buffer_delay:
            self.buffer_delay = self.seconds

    @property
    @make_thread_safe
    def buffer_delay(self):
        """Return the number of seconds (of data in the buffer) before you can read data from the buffer."""
        return self._buffer_delay

    @buffer_delay.setter
    @make_thread_safe
    def buffer_delay(self, seconds):
        """Set the number of seconds (of data in the buffer) before you can read data from the buffer."""
        if self._buffer_delay > self.seconds:
            raise ValueError('The buffer delay cannot be greater than the total number of seconds the buffer can hold!')
        self._buffer_delay = seconds

    @make_thread_safe
    def clear(self):
        super().clear()
        self._data[:] = 0
        self.can_read = False

    def _write(self, data, length, error, move_start=False):
        """Actually write the data to the numpy array.

        # Note:
        #     Writing in this buffer does not move the start like the RingBuffer. The write pointer can overrun the
        #     read pointer.

        Args:
            data (np.array/np.ndarray): Numpy array of data to write. This should already be in the correct format.
            length (int): Length of data to write. (This argument needs to be here for error purposes).
            error (bool): Error on overflow else overrun the start pointer or move the start pointer to prevent
                overflow (Makes it circular).
            move_start (bool)[True]: If error is false should overrun occur or should the start pointer move.

        Raises:
            OverflowError: If error is True and more data is being written then there is space available.
        """
        super()._write(data, length, error, move_start)
        if self._length >= self.get_sample_rate() * self.buffer_delay:
            self.can_read = True

    @make_thread_safe
    def read(self, amount=None, error=False):
        """Read the data and move the start/read pointer, so that data is not read again.

        This method reads empty if the amount specified is greater than the amount in the buffer.

        Args:
            amount (int)[None]: Amount of data to read
            error (bool)[False]: Raise an error if there is not enough data.

        Raises:
            UnderflowError: If error was given as True and the amount is > the length.

        Returns:
            data (np.array/np.ndarray): Array of data that is the length amount filled with zeros if needed.
        """
        if amount is None:
            amount = self._length
        if not self.can_read:
            return np.zeros(shape=(amount, self.channels), dtype=(self.dtype))
        else:
            idxs = self.get_indexes(self._start, amount, self.maxsize)
            self.move_start(amount, error, limit_amount=False)
            data = self._data[idxs].copy()
            self._data[idxs] = 0
            return data

    def move_start(self, amount, error=True, limit_amount=True):
        """This is an internal method and should not need to be called by the user.

        Move the start pointer the given amount (+/-).

        Raises:
            UnderflowError: If the amount is > the length.

        Args:
            amount (int): Amount to move the start pointer by.
            error (bool)[True]: Raise a ValueError else sync the end pointer and length.
            limit_amount (bool)[True]: If True force the amount to be less than or equal to the amount in the buffer.
        """
        if amount > self._length:
            if error:
                raise UnderflowError('Not enough data in the buffer ' + repr(self))
            if limit_amount:
                amount = self._length
        stop = self._start + amount
        try:
            self._start = stop % self.maxsize
        except ZeroDivisionError:
            self._start = stop

        self._length -= amount
        if self._length <= -(self.maxsize * 2):
            if self.maxsize > 0:
                self._length = (self._end - self._start) % self.maxsize - self.maxsize

    def move_end(self, amount, error=True, move_start=True):
        """This is an internal method and should not need to be called by the user.

        Move the end pointer the given amount (+/-).

        Raises:
            OverflowError: If the amount is > the available buffer space.

        Args:
            amount (int): Amount to move the end pointer by.
            error (bool)[True]: Raise an OverflowError else sync the start pointer and length.
            move_start (bool)[True]: If True and amount > available move the start pointer with the end pointer.
        """
        avaliable = self.maxsize - self._length
        if amount > 0:
            if amount > avaliable:
                if error:
                    raise OverflowError('Not enough space in the buffer ' + repr(self) + ' ' + repr(len(self)) + ' < ' + repr(amount))
                if move_start:
                    make_available = amount - avaliable
                    self.move_start(make_available, False)
                    if amount > self.maxsize:
                        self.move_start(-(amount - self.maxsize) - 1, False)
        stop = self._end + amount
        try:
            self._end = stop % self.maxsize
        except ZeroDivisionError:
            self._end = stop

        self._length += amount
        if self._length >= self.maxsize * 2:
            if self.maxsize > 0:
                self._length = self._length % self.maxsize

    @property
    def shape(self):
        """Return the shape of the data."""
        return self._data.shape

    @shape.setter
    @make_thread_safe
    def shape(self, new_shape):
        """Set the shape."""
        RingBufferThreadSafe.shape.fset(self, new_shape)
        self._seconds = self.maxsize / self.get_sample_rate()
        if self._seconds < self.buffer_delay:
            self.buffer_delay = self._seconds

    def __len__(self):
        """Return the current size of the buffer."""
        if self._length < 0:
            return 0
        else:
            if self._length > self.maxsize:
                return self.maxsize
            return self._length