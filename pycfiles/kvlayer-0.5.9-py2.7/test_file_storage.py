# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/tests/test_file_storage.py
# Compiled at: 2015-07-31 13:31:44
from __future__ import absolute_import
import uuid
from kvlayer._file_storage import FileStorage

def test_persistence(tmpdir, namespace_string):
    filename = str(tmpdir.join('original'))
    storage = FileStorage(config={'filename': filename}, app_name='kvlayer', namespace=namespace_string)
    storage.setup_namespace({'table1': 4, 'table2': 1})
    storage.put('table1', *[
     (
      (uuid.uuid4(), uuid.uuid4(),
       uuid.uuid4(), uuid.uuid4()), 'test_data')])
    results = list(storage.scan('table1'))
    assert len(results) == 1
    assert results[0][1] == 'test_data'
    storage = FileStorage(config={'filename': filename}, app_name='kvlayer', namespace=namespace_string)
    storage.setup_namespace({'table1': 4, 'table2': 1})
    results2 = list(storage.scan('table1'))
    assert len(results2) == 1
    assert results2[0][1] == 'test_data'
    copy_filename = str(tmpdir.join('new'))
    storage = FileStorage(config={'filename': filename, 'copy_to_filename': copy_filename}, app_name='kvlayer', namespace=namespace_string)
    storage.setup_namespace({'table1': 4, 'table2': 1})
    results3 = list(storage.scan('table1'))
    assert len(results3) == 1
    assert results3[0][1] == 'test_data'
    assert results == results2 == results3