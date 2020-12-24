# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-fat/egg/nosetty/test/test_units.py
# Compiled at: 2007-05-24 09:55:41
import os, sys
from nose.tools import eq_, raises
from fixture import TempIO
from nosetty import reproduce_program, Session, NoseTTY, InteractiveError

def test_main_program_is_reproducable():
    eq_(reproduce_program(['nosetests', '-v']), ['nosetests', '-v'])
    nosepassthru = os.path.join(os.path.dirname(__file__), 'nosepassthru.py')
    p = reproduce_program([nosepassthru])
    eq_(p, [sys.executable, nosepassthru])
    assert p[0].lower().endswith('python'), 'unexpected args: %s' % p


def test_session_maintains_state():
    tmp = TempIO()
    data_file = tmp.join('.session')
    session = Session(data_file, 'foo')
    eq_(session.started_as_parent(), True)
    eq_(session.started_as_parent(), False)
    eq_(session.started_as_parent(), False)
    session2 = Session(data_file, 'foo2')
    eq_(session2.started_as_parent(), True)
    eq_(session2.started_as_parent(), False)
    session.unregister_parent()
    eq_(session.started_as_parent(), True)
    eq_(session2.started_as_parent(), False)
    session2.unregister_parent()
    eq_(session2.started_as_parent(), True)


def test_edit_command_is_customizable():
    p = NoseTTY()
    p.tty_editor = 'foober'
    p.tty_edit_cmd = '%(editor)s --foo-line %(lineno)s %(filename)s'
    eq_(p.compileEditCommand('foo_file.py', 1), 'foober --foo-line 1 foo_file.py')
    p.tty_editor = 'foober'
    p.tty_edit_cmd = '%(editor)s --foo-line %(lineindex)s %(filename)s'
    eq_(p.compileEditCommand('foo_file.py', 1), 'foober --foo-line 0 foo_file.py')
    p.tty_editor = 'foober'
    p.tty_edit_cmd = '%(editor)s --foo-line %(lineindex)s %(FARRBAR)s'
    raises(InteractiveError)(p.compileEditCommand)('filename.py', 1)