# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\repos\testlibs\np_rw_buffer\np_rw_buffer\buffer.py
# Compiled at: 2020-02-17 15:52:57
# Size of source mod 2**32: 19894 bytes
"""
    np_rw_buffer.buffer
    SeaLandAire Technologies
    @author: jengel

Numpy circular buffer to help store audio data.

"""
import numpy as np, threading
from .utils import make_thread_safe
from .circular_indexes import get_indexes
__all__ = [
 'UnderflowError', 'get_shape_columns', 'get_shape', 'reshape', 'RingBuffer', 'RingBufferThreadSafe']
UnderflowError = ValueError

def get_shape(shape):
    """Return rows, columns for the shape."""
    try:
        return (
         shape[0], shape[1]) + shape[2:]
    except IndexError:
        return (
         shape[0], 0) + shape[2:]
    except TypeError:
        return (
         int(shape), 0)


def get_shape_columns(shape):
    """Return the number of columns for the shape."""
    try:
        return shape[1]
    except (IndexError, TypeError):
        return 0


def reshape(ring_buffer, shape):
    """Safely reshape the data.

    Args:
        ring_buffer (RingBuffer/np.ndarray/np.array): Array to reshape
        shape (tuple): New shape
    """
    try:
        buffer = ring_buffer._data
    except AttributeError:
        buffer = ring_buffer

    new_shape = get_shape(shape)
    myshape = get_shape(buffer.shape)
    if new_shape[1] == 0:
        new_shape = (
         new_shape[0], 1) + new_shape[2:]
    if new_shape[0] == -1:
        try:
            buffer.shape = new_shape
        except ValueError:
            rows = int(np.ceil(myshape[0] / new_shape[1]))
            new_shape = (rows,) + new_shape[1:]
            buffer.resize(new_shape, refcheck=False)

    else:
        buffer.resize(new_shape, refcheck=False)
    try:
        ring_buffer.clear()
    except AttributeError:
        pass


def format_write_data(data, mydtype):
    """Format the given data to the proper shape that can be written into this buffer."""
    try:
        len(data)
        dshape = data.shape
    except TypeError:
        data = np.asarray(data, dtype=mydtype)
        dshape = data.shape
    except AttributeError:
        data = np.asarray(data, dtype=mydtype)
        dshape = data.shape

    if get_shape_columns(dshape) == 0:
        data = np.reshape(data, (-1, 1))
    dshape = data.shape
    return (
     data, dshape)


class RingBuffer(object):
    __doc__ = 'Numpy circular buffer to help store audio data.\n\n    Args:\n        shape (tuple/int): Length of the buffer.\n        columns (int)[1]: Columns for the buffer.\n        dtype (numpy.dtype)[numpy.float32]: Numpy data type for the buffer.\n    '

    def __init__(self, shape, columns=None, dtype=np.float32):
        self._start = 0
        self._end = 0
        self._length = 0
        self.lock = threading.RLock()
        if isinstance(shape, (tuple, list)):
            shape = shape
            if columns is not None:
                if columns > 0:
                    shape = (
                     shape[0], columns) + shape[2:]
        else:
            if columns is None:
                columns = 1
            shape = (
             shape, columns)
        if get_shape_columns(shape) == 0:
            shape = (
             shape[0], 1) + shape[2:]
        shape = tuple(int(np.ceil(i)) for i in shape)
        self._data = np.zeros(shape=shape, dtype=dtype)

    def clear(self):
        """Clear the data."""
        self._start = 0
        self._end = 0
        self._length = 0

    def get_data(self):
        """Return the data in the buffer without moving the start pointer."""
        idxs = self.get_indexes(self._start, self._length, self.maxsize)
        return self._data[idxs].copy()

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
        self._data[idxs] = data

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
        data, shape = format_write_data(data, self.dtype)
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
        data, shape = format_write_data(data, self.dtype)
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
        data, shape = format_write_data(data, self.dtype)
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
            return self._data[0:0].copy()
        else:
            idxs = self.get_indexes(self._start, amount, self.maxsize)
            self.move_start(amount)
            return self._data[idxs].copy()

    def read_remaining(self, amount=None):
        """Read the data and move the start/read pointer, so that the data is not read again.

        This method reads the remaining data if the amount specified is greater than the amount in the buffer.

        Args:
            amount (int)[None]: Amount of data to read
        """
        if amount is None or amount > self._length:
            amount = self._length
        if amount == 0:
            return self._data[0:0].copy()
        else:
            idxs = self.get_indexes(self._start, amount, self.maxsize)
            self.move_start(amount)
            return self._data[idxs].copy()

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
            return self._data[0:0].copy()
        else:
            idxs = self.get_indexes(self._start, amount, self.maxsize)
            self.move_start(increment)
            return self._data[idxs].copy()

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
            return (self._data[idxs].copy(), skips + 1)

    def __len__(self):
        """Return the current size of the buffer."""
        return self._length

    def __str__(self):
        return self.get_data().__str__()

    get_indexes = staticmethod(get_indexes)

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
        """Return the maximum buffer size."""
        return len(self._data)

    @maxsize.setter
    def maxsize(self, maxsize):
        """Set the maximum size."""
        self.shape = (
         int(maxsize),) + self.shape[1:]
        self.clear()

    def get_available_space(self):
        """Return the available space."""
        return self.maxsize - len(self)

    @property
    def columns(self):
        """Return the number of columns/columns."""
        try:
            return self._data.shape[1] or 1
        except (AttributeError, IndexError):
            return 1

    @columns.setter
    def columns(self, columns):
        """Set the columns."""
        self.shape = (
         self.maxsize, columns) + self.shape[2:]
        self.clear()

    @property
    def shape(self):
        """Return the shape of the data."""
        return self._data.shape

    @shape.setter
    def shape(self, new_shape):
        """Set the shape."""
        reshape(self, new_shape)

    @property
    def dtype(self):
        """Return the dtype of the data."""
        return self._data.dtype

    @dtype.setter
    def dtype(self, dtype):
        try:
            self._data = self._data.astype(dtype)
        except (AttributeError, ValueError, TypeError, Exception):
            self._data = np.zeros(shape=(self.shape), dtype=dtype)
            self.clear()


class RingBufferThreadSafe(RingBuffer):
    __doc__ = 'Standard numpy circular buffer.\n\n    Args:\n        length (tuple/int): Length of the buffer.\n        columns (int)[1]: Columns for the buffer.\n        dtype (numpy.dtype)[numpy.float32]: Numpy data type for the buffer.\n    '

    def __init__(self, shape, columns=None, dtype=np.float32):
        self.lock = threading.RLock()
        super().__init__(shape=shape, columns=columns, dtype=dtype)

    clear = make_thread_safe(RingBuffer.clear)
    get_data = make_thread_safe(RingBuffer.get_data)
    set_data = make_thread_safe(RingBuffer.set_data)
    expanding_write = make_thread_safe(RingBuffer.expanding_write)
    growing_write = make_thread_safe(RingBuffer.growing_write)
    write = make_thread_safe(RingBuffer.write)
    read = make_thread_safe(RingBuffer.read)
    read_remaining = make_thread_safe(RingBuffer.read_remaining)
    read_overlap = make_thread_safe(RingBuffer.read_overlap)
    read_last = make_thread_safe(RingBuffer.read_last)
    __len__ = make_thread_safe(RingBuffer.__len__)
    __str__ = make_thread_safe(RingBuffer.__str__)
    move_start = make_thread_safe(RingBuffer.move_start)
    move_end = make_thread_safe(RingBuffer.move_end)
    sync_length = make_thread_safe(RingBuffer.sync_length)
    get_available_space = make_thread_safe(RingBuffer.get_available_space)
    maxsize = make_thread_safe(RingBuffer.maxsize)
    columns = make_thread_safe(RingBuffer.columns)
    shape = make_thread_safe(RingBuffer.shape)
    dtype = make_thread_safe(RingBuffer.dtype)