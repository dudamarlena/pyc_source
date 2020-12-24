# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: <demo_faktury-0.0.4>\tesseract.py
# Compiled at: 2020-03-26 17:02:32
# Size of source mod 2**32: 1184 bytes


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
     'convert',
     '-density',
     '350',
     path,
     '-depth',
     '8',
     '-alpha',
     'off',
     'png:-']
    p1 = subprocess.Popen(convert, stdout=(subprocess.PIPE))
    tess = [
     'tesseract', 'stdin', 'stdout']
    p2 = subprocess.Popen(tess, stdin=(p1.stdout), stdout=(subprocess.PIPE))
    out, err = p2.communicate()
    extracted_str = out
    return extracted_str