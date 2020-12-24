# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fabrom/workspace/jability-python-package/jabilitypyup/test_toolbox.py
# Compiled at: 2013-05-25 04:38:30
import toolbox
from toolbox import *

def test_ensure_listindex():
    l = ('a', 'b', 'c')
    assert ensure_listindex(l, '[0]') == 'a'
    assert ensure_listindex(l, '[0][0]') == 'a'
    l = (0, 1, 2)
    assert ensure_listindex(l, '[0][0]', 3) == 3
    assert ensure_listindex(l, '[5]', 4) == 4


def test_logger_force_rollover():
    assert logger_force_rollover(logging.getLogger()) >= 0
    try:
        logger_force_rollover(None)
        logger_force_rollover(list())
    except Exception:
        assert False
    else:
        assert True

    return


if __name__ == '__main__':
    import doctest
    doctest.testmod(toolbox)
    try:
        import nose
    except:
        pass
    else:
        nose.main()