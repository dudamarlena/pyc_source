# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/trader/workspace/learn/leboard/tests/leboard/test_leboard.py
# Compiled at: 2018-04-12 13:08:22
# Size of source mod 2**32: 1073 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, leboard, numpy as np

def test_leboard():
    letask = leboard.TaskBoard('__TEST_LEBOARD_TASK')
    letask.delete()
    entries = {}
    for layer in range(1, 6):
        board_entry = letask.Entry()
        board_entry.set('accuracy', np.random.random())
        board_entry.set('loss', np.random.random() * 100)
        board_entry.set('layers', layer)
        board_entry.commit()
        entries[board_entry.document.id] = board_entry.data.to_dict()

    for snapshot in letask.collection.get():
        print(snapshot.to_dict())
        @py_assert0 = entries[snapshot.id]
        @py_assert4 = snapshot.to_dict
        @py_assert6 = @py_assert4()
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.to_dict\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(snapshot) if 'snapshot' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(snapshot) else 'snapshot',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None

    for snap in letask.leaderboard('accuracy'):
        print(dict(id=snap.id, **snap.to_dict()))

    letask.delete()