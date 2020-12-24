# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Repos\TestLibs\np_rw_buffer\np_rw_buffer\new_buffer.py
# Compiled at: 2019-08-16 13:50:31
# Size of source mod 2**32: 16939 bytes
import numpy as np
from . import get_indexes
UnderflowError = ValueError

def format_write_data(data, mydtype, myshape):
    """Format the given data to the proper shape that can be written into this buffer."""
    try:
        len(data)
        dshape = data.shape
    except (TypeError, AttributeError):
        data = np.asarray(data, dtype=mydtype)
        dshape = data.shape

    if len(myshape) != len(dshape):
        data = np.reshape(data, (-1, ) + myshape[1:])
        dshape = data.shape
    return (data, dshape)


class RingBuffer(np.ndarray):
    __doc__ = 'Numpy circular buffer to help store audio data.\n\n    Example:\n\n        .. code-block:: python\n\n            buf = RingBuffer(10)\n            buf = RingBuffer(10, 2)\n            buf = RingBuffer((10, 2))\n\n    Args:\n        *shape (tuple/int): Length of the buffer.\n        dtype (numpy.dtype)[numpy.float32]: Numpy data type for the buffer.\n        fill_zeros (bool)[False]: Fill with zeros.\n        fill_ones (bool)[False]: Fill with ones.\n    '

    def __new__(cls, *args, shape=None, dtype=np.float32, fill_zeros=False, fill_ones=False, **kwargs):
        """Numpy circular buffer to help store audio data.

        Args:
            *args (tuple/int): Shape of the buffer.
            shape (tuple)[None]: Keyword argument for the shape of the buffer.
            dtype (numpy.dtype)[numpy.float32]: Numpy data type for the buffer.
            fill_zeros (bool)[False]: Fill with zeros.
            fill_ones (bool)[False]: Fill with ones.
        """
        if shape is None:
            shape = args
            if len(args) == 0:
                shape = 0
            elif len(args) == 1:
                if isinstance(args[0], (list, tuple)):
                    shape = args[0]
        obj = super(RingBuffer, cls).__new__(cls, shape=shape, dtype=dtype)
        obj._start = 0
        obj._end = 0
        obj._length = 0
        if fill_ones:
            obj[:] = 1
            obj._length = obj.shape[0]
            obj._end = obj._length
        else:
            if fill_zeros:
                obj[:] = 0
                obj._length = obj.shape[0]
                obj._end = obj._length
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._start = getattr(obj, '_start', 0)
        self._end = getattr(obj, '_end', 0)
        self._length = getattr(obj, '_length', 0)

    get_indexes = staticmethod(get_indexes)

    def clear(self):
        """Clear the data."""
        self._start = 0
        self._end = 0
        self._length = 0

    def get_data(self):
        """Return the data in the buffer without moving the start pointer."""
        idxs = self.get_indexes(self._start, self._length, self.maxsize)
        return self[idxs].view(np.ndarray)

    def set_data(self, data):
        """Set the data."""
        self.dtype = data.dtype
        self.shape = data.shape
        self.clear()
        self.expanding_write(data)

    def _write(self, data, length, error, move_start=True):
        """Actually write the data to the numpy array.

        Args:
            data (np.array/np.ndarray): Numpy array of data to write. This should already be in the correct format.
            length (int): Length of data to write. (This argument needs to be here for error purposes).
            error (bool): Error on overflow else overrun the start pointer or move the start pointer to prevent
                overflow (Makes it circular).
            move_start (bool)[True]: If error is false should overrun occur or should the start pointer move.

        Raises:
            OverflowError: If error is True and more data is being written then there is space available.
        """
        idxs = self.get_indexes(self._end, length, self.maxsize)
        self.move_end(length, error, move_start)
        self[idxs] = data

    def expanding_write(self, data, error=True):
        """Write data into the buffer. If the data is larger than the buffer expand the buffer.

        Args:
            data (numpy.array): Data to write into the buffer.
            error (bool)[True]: Error on overflow else overrun the start pointer or move the start pointer to prevent
                overflow (Makes it circular).

        Raises:
            ValueError: If data shape does not match this shape. Arrays without a column will be convert to 1 column
                Example: (5,) will become (5, 1) and will not error if there is 1 column
            OverflowError: If the written data will overflow the buffer.
        """
        data, shape = format_write_data(data, self.dtype, self.shape)
        length = shape[0]
        if shape[1:] != self.shape[1:]:
            msg = 'could not broadcast input array from shape {:s} into shape {:s}'.format(str(shape), str(self.shape))
            raise ValueError(msg)
        else:
            if length > self.maxsize:
                self.shape = (
                 length,) + self.shape[1:]
        self._write(data, length, error)

    def growing_write(self, data):
        """Write data into the buffer. If there is not enough available space then grow the buffer.

        Args:
            data (numpy.array): Data to write into the buffer.

        Raises:
            ValueError: If data shape does not match this shape. Arrays without a column will be convert to 1 column
                Example: (5,) will become (5, 1) and will not error if there is 1 column
            OverflowError: If the written data will overflow the buffer.
        """
        data, shape = format_write_data(data, self.dtype, self.shape)
        length = shape[0]
        available = self.get_available_space()
        if shape[1:] != self.shape[1:]:
            msg = 'could not broadcast input array from shape {:s} into shape {:s}'.format(str(shape), str(self.shape))
            raise ValueError(msg)
        else:
            if length > available:
                old_data = self.get_data()
                self.shape = (self.maxsize + (length - available),) + self.shape[1:]
                if len(old_data) > 0:
                    self._write(old_data, len(old_data), False)
        self._write(data, length, error=True)

    def write(self, data, error=True):
        """Write data into the buffer.

        Args:
            data (numpy.array): Data to write into the buffer.
            error (bool)[True]: Error on overflow else overrun the start pointer or move the start pointer to prevent
                overflow (Makes it circular).

        Raises:
            ValueError: If data shape does not match this shape. Arrays without a column will be convert to 1 column
                Example: (5,) will become (5, 1) and will not error if there is 1 column
            OverflowError: If the written data will overflow the buffer.
        """
        data, shape = format_write_data(data, self.dtype, self.shape)
        length = shape[0]
        if shape[1:] != self.shape[1:]:
            msg = 'could not broadcast input array from shape {:s} into shape {:s}'.format(str(shape), str(self.shape))
            raise ValueError(msg)
        else:
            if not error:
                if length > self.maxsize:
                    data = data[-self.maxsize:]
                    length = self.maxsize
        self._write(data, length, error)

    def read(self, amount=None):
        """Read the data and move the start/read pointer, so that data is not read again.

        This method reads empty if the amount specified is greater than the amount in the buffer.

        Args:
            amount (int)[None]: Amount of data to read
        """
        if amount is None:
            amount = self._length
        if amount == 0 or amount > self._length:
            return self[0:0].view(np.ndarray)
        else:
            idxs = self.get_indexes(self._start, amount, self.maxsize)
            self.move_start(amount)
            return self[idxs].view(np.ndarray)

    def read_remaining(self, amount=None):
        """Read the data and move the start/read pointer, so that the data is not read again.

        This method reads the remaining data if the amount specified is greater than the amount in the buffer.

        Args:
            amount (int)[None]: Amount of data to read
        """
        if amount is None or amount > self._length:
            amount = self._length
        if amount == 0:
            return self[0:0].view(np.ndarray)
        else:
            idxs = self.get_indexes(self._start, amount, self.maxsize)
            self.move_start(amount)
            return self[idxs].view(np.ndarray)

    def read_overlap(self, amount=None, increment=None):
        """Read the data and move the start/read pointer.

        This method only increments the start/read pointer the given increment amount. This way the same data can be
        read multiple times.

        This method reads empty if the amount specified is greater than the amount in the buffer.

        Args:
            amount (int)[None]: Amount of data to read
            increment (int)[None]: Amount to move the start/read pointer allowing overlap if increment is less than the
                given amount.
        """
        if amount is None:
            amount = self._length
        if increment is None:
            increment = amount
        if amount == 0 or amount > self._length:
            return self[0:0].view(np.ndarray)
        else:
            idxs = self.get_indexes(self._start, amount, self.maxsize)
            self.move_start(increment)
            return self[idxs].view(np.ndarray)

    def read_last(self, amount=None, update_rate=None):
        """Read the last amount of data and move the start/read pointer.

        This is an odd method for FFT calculations. It reads the newest data moving the start pointer by the
        update_rate amount that it was given. The returned skips number is the number of update_rate values.

        Example:

            .. code-block :: python

                >>> buffer = RingBuffer(11, 1)
                >>> buffer.write([0, 1, 2, 3, 4, 5, 6, 7 ,8, 9, 10])
                >>> buffer.read_last(6, 2))
                (array([[4.],
                        [5.],
                        [6.],
                        [7.],
                        [8.],
                        [9.]], dtype=float32), 3)
                >>> # Note must read in a multiple of the amount and moves by a multiple of the update rate.

        Args:
            amount (int)[None]: Amount of data to read. NFFT value.
            update_rate (int)[None]: The fft update rate value. How many samples to move the pointer by
                to cause overlap.

        Returns:
            data (np.array/np.ndarray) [None]: Data that is of length amount.
            updates (int) [0]: Number of updates (Total number of update rates until the end of the data was
                found including the data that was returned).
        """
        if amount is None:
            amount = self._length
        if update_rate is None:
            update_rate = amount
        if amount == 0 or amount > self._length:
            return (None, 0)
        else:
            skips = (self._length - amount) // update_rate
            if skips > 0:
                self.move_start(update_rate * skips)
            idxs = self.get_indexes(self._start, amount, self.maxsize)
            self.move_start(update_rate)
            return (self[idxs].view(np.ndarray), skips + 1)

    def __len__(self):
        """Return the current size of the buffer."""
        return self._length

    def __str__(self):
        d = self.get_data()
        return np.ndarray.__str__(d)

    def __bytes__(self):
        d = self.get_data()
        return np.ndarray.tobytes(d)

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
        if amount == 0:
            return
        else:
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

        self.sync_length(False or amount < 0)

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
        if amount == 0:
            return
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

        self.sync_length(True and amount >= 0)

    def sync_length(self, should_grow=True):
        """Sync the length with the start and end pointers.

        Args:
            should_grow (int): Determines if start and end equal means full or empty.
                Writing can make full, reading empty.
        """
        try:
            self._length = (self._end - self._start) % self.maxsize
        except ZeroDivisionError:
            self._length = 0

        if self._length == 0:
            if should_grow:
                self._length = self.maxsize

    @property
    def maxsize(self):
        try:
            return super().__len__()
        except:
            return 0

    @maxsize.setter
    def maxsize(self, maxsize):
        """Set the maximum size."""
        self.shape = (
         int(maxsize),) + self.shape[1:]

    def get_available_space(self):
        """Return the available space."""
        return self.maxsize - len(self)

    @property
    def shape(self):
        return super(RingBuffer, self).shape

    @shape.setter
    def shape(self, new_shape):
        try:
            super(RingBuffer, type(self)).shape.__set__(self, new_shape)
            self.clear()
            return
        except ValueError:
            pass

        if new_shape[0] == -1:
            rows = int(np.ceil(self.shape[0] / new_shape[1]))
            new_shape = (rows,) + new_shape[1:]
        self.resize(new_shape, refcheck=False)
        self.clear()

    @property
    def columns(self):
        try:
            return self.shape[1]
        except (IndexError, AttributeError):
            return 0

    @columns.setter
    def columns(self, value):
        myshape = self.shape
        self.shape = myshape[0:1] + (value,) + myshape[2:]