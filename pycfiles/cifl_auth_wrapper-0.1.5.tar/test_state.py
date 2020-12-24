# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cifitlib/test_state.py
# Compiled at: 2011-01-27 14:39:21
__doc__ = '\ntest_procs.py\n\nCreated by Craig Sawyer on 2010-01-14.\nCopyright (c) 2009, 2010 Craig Sawyer (csawyer@yumaed.org). All rights reserved. see LICENSE.\n'
import os, nose, state

def test_counts():
    if os.path.exists('test.pickle'):
        os.unlink('test.pickle')
    s = state.State('test', {'count': 2})
    s.add(1)
    print 'added 1:', s.get()
    assert s.get('first')[1] == 1
    assert s.get('last')[1] == 1
    assert s.get(2) == (None, None)
    assert len(s.get()) == 1
    s.add(2)
    print 'added 2:', s.get()
    assert s.get('first')[1] == 1
    assert s.get('last')[1] == 2
    assert s.get('2') == (None, None)
    assert len(s.get()) == 2
    s.add(3)
    print 'added 3:', s.get()
    assert s.get('first')[1] == 1
    assert s.get('last')[1] == 3
    print s.get(2)
    assert s.get(2)[1] == 3
    assert len(s.get()) == 3
    s.add(4)
    print 'added 4:', s.get()
    assert s.get('first')[1] == 2
    assert s.get('last')[1] == 4
    assert s.get(2)[1] == 4
    assert len(s.get()) == 3
    s.save()
    del s
    s = state.State('test')
    assert s.opts['count'] == 2
    s.add(5)
    assert s.get('first')[1] == 3
    assert s.get('last')[1] == 5
    assert s.get(1)[1] == 4
    assert len(s.get()) == 3
    return


if __name__ == '__main__':
    nose.run()