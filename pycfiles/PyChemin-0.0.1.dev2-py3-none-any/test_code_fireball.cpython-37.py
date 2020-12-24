# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gufranco/Documents/PyChemia/tests/test_code_fireball.py
# Compiled at: 2020-01-17 14:30:16
# Size of source mod 2**32: 750 bytes
import pychemia, tempfile, zipfile, os

def test_fireball():
    """
    Test (pychemia.code.fireball) [Reading fireball output]     :
    """
    tmpdir = tempfile.mkdtemp()
    path = os.path.abspath('tests/data/1280.zip')
    zf = zipfile.ZipFile(path)
    oldpwd = os.getcwd()
    os.chdir(tmpdir)
    zf.extract('1280/output.log')
    fo = zf.extract('1280/output.log')
    output = pychemia.code.fireball.read_fireball_stdout(fo)
    assert output['grand_total'][(-1)] == -31202.46383232
    assert len(output['grand_total']) == 313
    os.remove(fo)
    os.rmdir(tmpdir + os.sep + '1280')
    os.rmdir(tmpdir)
    os.chdir(oldpwd)