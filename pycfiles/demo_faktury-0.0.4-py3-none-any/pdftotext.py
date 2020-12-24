# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <demo_faktury-0.0.4>\pdftotext.py
# Compiled at: 2020-03-26 17:02:32
# Size of source mod 2**32: 784 bytes
from os.path import dirname, join
_PATH = join(dirname(dirname(__file__)), 'poppler')

def to_text(path):
    """Wrapper around Poppler pdftotext.

    Parameters
    ----------
    path : str
        path of electronic invoice in PDF

    Returns
    -------
    out : str
        returns extracted text from pdf

    Raises
    ------
    EnvironmentError:
        If pdftotext library is not found
    """
    import subprocess
    from distutils import spawn
    pdftotext = spawn.find_executable('pdftotext', path=_PATH)
    out, err = subprocess.Popen([
     pdftotext, '-layout', '-enc', 'UTF-8', path, '-'],
      stdout=(subprocess.PIPE)).communicate()
    return out