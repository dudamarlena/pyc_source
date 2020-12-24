# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/mm_unit/__init__.py
# Compiled at: 2009-02-18 00:27:36
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from minimock import Printer
import doctest
__all__ = [
 'TraceTracker', 'assert_same_trace']

class TraceTracker(Printer):
    """
    Keeps track of the usage of a MiniMock-ed object, and allows for that usage
    to be analysed after the fact.
    """

    def __init__(self, *args, **kw):
        self.out = StringIO()
        super(TraceTracker, self).__init__(self.out, *args, **kw)
        self.checker = doctest.OutputChecker()
        self.options = doctest.ELLIPSIS
        self.options |= doctest.NORMALIZE_WHITESPACE
        self.options |= doctest.REPORT_UDIFF

    def check(self, want):
        """
        Compare expected MiniMock usage with that which we expected.
        
        :param want: the MiniMock output that results from expected usage of
            mocked objects
        :type want: string
        :rtype: a ``True`` value if the check passed, ``False`` otherwise
        
        Example::
        
            >>> from minimock import Mock
            >>> tt = TraceTracker()
            >>> m = Mock('mock_obj', tracker=tt)
            >>> m.some_meth('dummy argument')
            >>> tt.check("Called mock_obj.some_meth('dummy argument')")
            True
            >>> tt.check("Failing expected trace")
            False
        """
        return self.checker.check_output(want, self.dump(), optionflags=self.options)

    def diff(self, want):
        r"""
        Compare expected MiniMock usage with that which we expected.
        
        :param want: the MiniMock output that results from expected usage of
            mocked objects
        :type want: string
        :rtype: a ``True`` value if the check passed, ``False`` otherwise
        
        Example::
        
            >>> from minimock import Mock
            >>> tt = TraceTracker()
            >>> m = Mock('mock_obj', tracker=tt)
            >>> m.some_meth('dummy argument')
            >>> tt.diff("Dummy string")
            "Expected:\n    Dummy string\nGot:\n    Called mock_obj.some_meth('dummy argument')\n"
        """
        return self.checker.output_difference(doctest.Example('', want), self.dump(), optionflags=self.options)

    def dump(self):
        r"""
        Return the MiniMock usage so far.
        
        Example::
        
            >>> from minimock import Mock
            >>> tt = TraceTracker()
            >>> m = Mock('mock_obj', tracker=tt)
            >>> m.some_meth('dummy argument')
            >>> tt.dump()
            "Called mock_obj.some_meth('dummy argument')\n"
        """
        return self.out.getvalue()


def assert_same_trace(tracker, want):
    r"""
    Check the usage of a :class:`mm_unit.TraceTracker` is as expected.
    
    :param tracker: a :class:`mm_unit.TraceTracker` instance
    :param want: the expected MiniMock output
    :type want: string
    :raises: :exc:`AssertionError` if the expected and observed outputs don't
        match
    
    Example::
    
            >>> from minimock import Mock
            >>> tt = TraceTracker()
            >>> m = Mock('mock_obj', tracker=tt)
            >>> m.some_meth('dummy argument')
            >>> assert_same_trace(tt,
            ...     "Called mock_obj.some_meth('dummy argument')\n")
    """
    assert tracker.check(want), tracker.diff(want)


if __name__ == '__main__':
    import doctest
    doctest.testmod()