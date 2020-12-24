# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ninvoice2data/input/textfile.py
# Compiled at: 2019-02-01 06:07:02


def to_text(path):
    """Read text from given file.

    Parameters
    ----------
    path : str
        path of electronic invoice in JPG or PNG format

    Returns
    -------
    extracted_str : str
        returns extracted text any out file

    """
    file = open(path, 'r')
    return file.read()