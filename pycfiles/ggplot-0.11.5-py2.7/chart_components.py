# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/chart_components.py
# Compiled at: 2016-07-31 11:30:58
from __future__ import absolute_import, division, print_function, unicode_literals
from copy import deepcopy
from .ggplot import ggplot

class ggtitle(object):
    """
    Add a title to your plot

    Parameters
    ----------
    title:
        Your plot title

    Examples
    --------
    >>> ggplot(mpg, aes(x='hwy')) + geom_hisotgram() + ggtitle("MPG Plot")
    """

    def __init__(self, title):
        if title is None:
            raise Exception(b'No title specified!')
        self.title = title
        return

    def __radd__(self, gg):
        if isinstance(gg, ggplot):
            gg = deepcopy(gg)
            gg.title = self.title
            return gg
        else:
            return self


class xlim(object):
    """
    Set upper and lower limits for your x axis

    Parameters
    ----------
    lower_limit:
        lower limit for axis
    upper_limit:
        upper limit for axis

    Examples
    --------
    >>> ggplot(mpg, aes(x='hwy')) + geom_hisotgram() + xlim(0, 20)
    """

    def __init__(self, low=None, high=None):
        if low != None:
            try:
                _ = low - 0
            except TypeError:
                raise Exception(b"The 'low' argument to", self.__class__.__name__, b'must be of a numeric type or None')

        if high != None:
            try:
                _ = high - 0
            except TypeError:
                raise Exception(b"The 'high' argument to", self.__class__.__name__, b'must be of a numeric type or None')

        self.low, self.high = low, high
        return

    def __radd__(self, gg):
        gg = deepcopy(gg)
        gg.xlimits = [self.low, self.high]
        return gg


class ylim(object):
    """
    Set upper and lower limits for your y axis

    Parameters
    ----------
    lower_limit:
        lower limit for axis
    upper_limit:
        upper limit for axis

    Examples
    --------
    >>> ggplot(mpg, aes(x='hwy')) + geom_hisotgram() + ylim(0, 5)
    """

    def __init__(self, low=None, high=None):
        if low != None:
            try:
                _ = low - 0
            except TypeError:
                raise Exception(b"The 'low' argument to", self.__class__.__name__, b'must be of a numeric type or None')

        if high != None:
            try:
                _ = high - 0
            except TypeError:
                raise Exception(b"The 'high' argument to", self.__class__.__name__, b'must be of a numeric type or None')

        self.low, self.high = low, high
        return

    def __radd__(self, gg):
        gg = deepcopy(gg)
        gg.ylimits = [self.low, self.high]
        return gg


class xlab(object):
    """
    Set label for x axis

    Parameters
    ----------
    label:
        label for your axis

    Examples
    --------
    >>> ggplot(mpg, aes(x='hwy')) + geom_hisotgram() + xlab("Miles / gallon")
    """

    def __init__(self, xlab):
        if xlab is None:
            raise Exception(b'Arguments to', self.__class__.__name__, b'cannot be None')
        self.xlab = xlab
        return

    def __radd__(self, gg):
        gg = deepcopy(gg)
        gg.xlab = self.xlab
        return gg


class ylab(object):
    """
    Set label for y axis

    Parameters
    ----------
    label:
        label for your axis

    Examples
    --------
    >>> ggplot(mpg, aes(x='hwy')) + geom_hisotgram() + ylab("Count
(# of cars)")
    """

    def __init__(self, ylab):
        if ylab is None:
            raise Exception(b'Arguments to', self.__class__.__name__, b'cannot be None')
        self.ylab = ylab
        return

    def __radd__(self, gg):
        gg = deepcopy(gg)
        gg.ylab = self.ylab
        return gg


class labs(object):
    """
    Set labels plot

    Parameters
    ----------
    x:
        label for your x axis
    y:
        label for your y axis
    title:
        title for your plot

    Examples
    --------
    >>> ggplot(mpg, aes(x='hwy')) + geom_hisotgram() + labs("Miles / gallon", "Count
(# of cars)", "MPG Plot")
    """

    def __init__(self, x=None, y=None, title=None):
        self.x = x
        self.y = y
        self.title = title

    def __radd__(self, gg):
        gg = deepcopy(gg)
        if self.x:
            gg.xlab = self.x
        if self.y:
            gg.ylab = self.y
        if self.title:
            gg.title = self.title
        return gg


if __name__ == b'__main__':
    xlab(b'HI')
    ylab(b'hi')
    labs(x=b'hi', y=b'boo', title=b'foo')
    ggtitle(b'hi')