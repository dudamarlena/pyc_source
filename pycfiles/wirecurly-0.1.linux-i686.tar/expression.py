# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/wirecurly/dialplan/expression.py
# Compiled at: 2014-01-08 15:34:56
import logging
log = logging.getLogger(__name__)
__all__ = [
 'ExpressionBase', 'ExpressionAbs', 'ExpressionTime', 'ExpressionField']

class ExpressionBase(object):
    """
                Base Class for expressions
        """

    def __init__(self):
        super(ExpressionBase, self).__init__()

    def todict(self):
        """
                        to_dict must return a dict with all attributes
                """
        raise NotImplementedError


class ExpressionAbs(ExpressionBase):
    """
                Class for absolute expression
        """

    def __init__(self):
        super(ExpressionAbs, self).__init__()

    def todict(self):
        """
                        Absolute expressions have no attributes
                """
        return {}


class ExpressionTime(ExpressionBase):
    """
                Class for Time expressions
        """

    def __init__(self, wday, hour):
        super(ExpressionTime, self).__init__()
        self.wday = wday
        self.hour = hour

    def todict(self):
        """
                        Return a dict with wday and hour
                """
        return {'wday': self.wday, 'hour': self.hour}


class ExpressionField(ExpressionBase):
    """
                Field expressions Class
        """

    def __init__(self, field, exp):
        super(ExpressionField, self).__init__()
        self.field = field
        self.exp = exp

    def todict(self):
        """
                        Return a dict with field and expression
                """
        return {'field': self.field, 'expression': self.exp}