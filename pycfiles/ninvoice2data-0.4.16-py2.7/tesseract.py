# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ninvoice2data/input/tesseract.py
# Compiled at: 2019-02-01 05:18:39


def to_text(path):
    """Wraps Tesseract OCR.

    Parameters
    ----------
    path : str
        path of electronic invoice in JPG or PNG format

    Returns
    -------
    extracted_str : str
        returns extracted text from image in JPG or PNG format

    """
    import subprocess
    from distutils import spawn
    if not spawn.find_executable('tesseract'):
        raise EnvironmentError('tesseract not installed.')
    if not spawn.find_executable('convert'):
        raise EnvironmentError('imagemagick not installed.')
    convert = [
     'convert', '-density', '350', path, '-depth', '8', 'png:-']
    p1 = subprocess.Popen(convert, stdout=subprocess.PIPE, shell=True)
    tess = [
     'tesseract', 'stdin', 'stdout']
    p2 = subprocess.Popen(tess, stdin=p1.stdout, stdout=subprocess.PIPE)
    out, err = p2.communicate()
    extracted_str = out
    return extracted_str