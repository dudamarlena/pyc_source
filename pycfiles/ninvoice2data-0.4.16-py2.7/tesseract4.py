# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ninvoice2data/input/tesseract4.py
# Compiled at: 2019-02-01 05:18:39


def to_text(path, language='fra'):
    """Wraps Tesseract 4 OCR with custom language model.

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
    import tempfile, time
    if not spawn.find_executable('tesseract'):
        raise EnvironmentError('tesseract not installed.')
    if not spawn.find_executable('convert'):
        raise EnvironmentError('imagemagick not installed.')
    if not spawn.find_executable('gs'):
        raise EnvironmentError('ghostscript not installed.')
    with tempfile.NamedTemporaryFile(suffix='.tiff') as (tf):
        gs_cmd = [
         'gs',
         '-q',
         '-dNOPAUSE',
         '-r600x600',
         '-sDEVICE=tiff24nc',
         '-sOutputFile=' + tf.name,
         path,
         '-c',
         'quit']
        subprocess.Popen(gs_cmd)
        time.sleep(3)
        magick_cmd = [
         'convert',
         tf.name,
         '-colorspace',
         'gray',
         '-type',
         'grayscale',
         '-contrast-stretch',
         '0',
         '-sharpen',
         '0x1',
         'tiff:-']
        p1 = subprocess.Popen(magick_cmd, stdout=subprocess.PIPE, shell=True)
        tess_cmd = [
         'tesseract', '-l', language, '--oem', '1', '--psm', '3', 'stdin', 'stdout']
        p2 = subprocess.Popen(tess_cmd, stdin=p1.stdout, stdout=subprocess.PIPE)
        out, err = p2.communicate()
        extracted_str = out
        return extracted_str