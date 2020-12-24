# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_db_queue.py
# Compiled at: 2020-01-17 14:32:58
# Size of source mod 2**32: 1506 bytes
import os, pychemia, tempfile, shutil
from pychemia.utils.computing import hashfile
from pychemia.db import has_connection

def test_queue():
    """
    Test (pychemia.db.PyChemiaQueue)                            :
    """
    if not has_connection():
        return
    print('Testing PyChemiaQueue')
    source = 'tests/data/vasp_01'
    destination = tempfile.mkdtemp()
    print('Destination: %s' % destination)
    st = pychemia.code.vasp.read_poscar(source + os.sep + 'POSCAR')
    print('Structure: \n%s' % st)
    vi = pychemia.code.vasp.read_incar(source + os.sep + 'INCAR')
    print('VASP Input: \n%s' % vi)
    pq = pychemia.db.PyChemiaQueue()
    files = [
     source + os.sep + 'KPOINTS']
    entry_id = pq.new_entry(structure=st, variables=vi, code='vasp', files=files)
    nfiles = pq.db.fs.files.count()
    print('Number of files: ', nfiles)
    pychemia.code.vasp.write_from_queue(pq, entry_id, destination)
    for i in os.listdir(source):
        assert hashfile(source + os.sep + i) == hashfile(destination + os.sep + i)

    print('Files in source and destination are identical')
    print('Adding the same entry again and testing that the number of files is unchanged')
    entry_id = pq.new_entry(structure=st, variables=vi, code='vasp', files=files)
    assert nfiles == pq.db.fs.files.count()
    print('The number of files remains the same ', nfiles)
    shutil.rmtree(destination)


if __name__ == '__main__':
    test_queue()