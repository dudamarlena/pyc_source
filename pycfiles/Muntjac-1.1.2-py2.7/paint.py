# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/addon/invient/paint.py
# Compiled at: 2013-04-04 15:36:37


class IPaint(object):
    """This Paint interface defines how color patterns can be generated
    when drawing the InvientCharts.

    @author: Invient
    @author: Richard Lincoln
    """

    def getString(self):
        """Returns string representation of an object of type Paint.

        @return: Returns string representation of an object of type Paint.
        """
        raise NotImplementedError