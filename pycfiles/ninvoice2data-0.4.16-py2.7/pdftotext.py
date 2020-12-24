# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ninvoice2data/input/pdftotext.py
# Compiled at: 2019-02-01 05:18:39


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
    if spawn.find_executable('pdftotext'):
        out, err = subprocess.Popen([
         'pdftotext', '-layout', '-enc', 'UTF-8', path, '-'], stdout=subprocess.PIPE).communicate()
        return out
    raise EnvironmentError('pdftotext not installed. Can be downloaded from https://poppler.freedesktop.org/')