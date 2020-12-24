# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/widget/stock/guiprogressbar.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 6562 bytes
"""
General-purpose :mod:`QProgressBar` subclasses.
"""
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QProgressBar
from betsee.util.widget.mixin.guiwdgmixin import QBetseeObjectMixin

class QBetseeProgressBar(QBetseeObjectMixin, QProgressBar):
    __doc__ = '\n    :mod:`QProgressBar`-based widget exposing additional caller-friendly slots.\n\n    This widget augments the stock :class:`QProgressBar` class with high-level\n    properties simplifying usage *and* high-level slots combining the utility\n    of various lower-level slots (e.g., :meth:`set_range_and_value_minimum`).\n    '

    @property
    def is_done(self) -> bool:
        """
        ``True`` only if this progress bar is currently in the **finished
        state** (i.e., if the current value of this progress bar is equal to
        the maximum value previously passed to the :meth:`setRange` method).
        """
        return self.value() == self.maximum()

    @property
    def is_reset(self) -> bool:
        """
        ``True`` only if this progress bar is currently in the **reset state**
        (i.e., if either the :meth:`setValue` method has yet to be called *or*
        the :meth:`reset` method has been called more recently than the
        :meth:`setValue` method).

        Equivalently, this property returns ``True`` only if this progress bar
        has no current progress value. Note that:

        * All progress bars are initially reset by default.
        * The **undetermined state** (i.e., when the range of this progress
          bar is ``[0, 0]``) takes precedence over this reset state. A progress
          bar that is currently undetermined is *not* reset.
        """
        return self.value() == self.minimum() - 1

    @property
    def is_undetermined(self) -> bool:
        """
        ``True`` only if this progress bar is currently in the **undetermined
        state** (i.e., if the :meth:`set_range_undetermined` method has been
        called more recently than any other range-setting method).

        Equivalently, this property returns ``True`` only if this progress bar
        allows exactly one possible progress value (i.e., 0), which Qt
        typically portrays as a busy indicator.
        """
        return self.maximum() == 0 and self.minimum() == 0

    @Slot(int, int)
    def set_range_and_value_minimum(self, minimum: int, maximum: int) -> None:
        """
        Sets the range of this progress bar to the passed range *and* sets the
        value of this progress bar to the minimum value of this range.

        This high-level slot is intended to serve as a drop-in replacement for
        the lower-level :meth:`setRange`. The latter only sets the range of
        this progress bar to the passed range, requiring callers to explicitly
        call the stock :meth:`setValue` slot with the minimum value of this
        range to perform the equivalent of this slot. Since callers typically
        perform both on setting the range, this slot conjoins these two slots
        into one slot for caller convenience.

        Caveats
        ----------
        Note that, if:

        * The passed minimum and maximum are both 0, this progress bar is set
          to an undetermined state.
        * The passed maximum is less than the passed minimum, only the passed
          minimum is set; the passed maximum is ignored.
        * The current value of this progress bar resides outside this range,
          this progress bar is implicitly reset by internally calling the
          :meth:`reset` method.

        Parameters
        ----------
        minimum : int
            Minimum value to constrain the values of this progress bar to.
        maximum : int
            Maximum value to constrain the values of this progress bar to.
        """
        self.setRange(minimum, maximum)
        self.setValue(minimum)

    def set_range_undetermined(self) -> None:
        """
        Change this progress bar to the **undetermined state** (i.e., the state
        such that this progress bar allows exactly one possible progress value
        of 0 rather than a range of such values).

        Qt typically portrays this state as a busy indicator.
        """
        self.setRange(0, 0)