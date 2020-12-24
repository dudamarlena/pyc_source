# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Anaconda3\Lib\site-packages\pytesser3\__init__.py
# Compiled at: 2016-09-22 23:32:18
# Size of source mod 2**32: 2683 bytes
"""OCR in Python using the Tesseract engine from Google
http://code.google.com/p/pytesser/
by Michael J.T. O'Kelly
V 0.0.1, 3/10/07"""
from PIL import Image
import subprocess
from pytesser3 import util
from pytesser3 import errors
tesseract_exe_name = 'c:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
scratch_image_name = 'temp.bmp'
scratch_text_name_root = 'temp'
cleanup_scratch_flag = True

def call_tesseract(input_filename, output_filename):
    """Calls external tesseract.exe on input file (restrictions on types),
        outputting output_filename+'txt'"""
    args = [
     tesseract_exe_name, input_filename, output_filename]
    proc = subprocess.Popen(args)
    retcode = proc.wait()
    if retcode != 0:
        errors.check_for_errors()


def image_to_string(im, cleanup=cleanup_scratch_flag):
    """Converts im to file, applies tesseract, and fetches resulting text.
        If cleanup=True, delete scratch files after operation."""
    try:
        util.image_to_scratch(im, scratch_image_name)
        call_tesseract(scratch_image_name, scratch_text_name_root)
        text = util.retrieve_text(scratch_text_name_root)
    finally:
        if cleanup:
            util.perform_cleanup(scratch_image_name, scratch_text_name_root)

    return text


def image_file_to_string(filename, cleanup=cleanup_scratch_flag, graceful_errors=True):
    """Applies tesseract to filename; or, if image is incompatible and graceful_errors=True,
        converts to compatible format and then applies tesseract.  Fetches resulting text.
        If cleanup=True, delete scratch files after operation."""
    try:
        try:
            call_tesseract(filename, scratch_text_name_root)
            text = util.retrieve_text(scratch_text_name_root)
        except errors.Tesser_General_Exception:
            if graceful_errors:
                im = Image.open(filename)
                text = image_to_string(im, cleanup)
            else:
                raise

    finally:
        if cleanup:
            util.perform_cleanup(scratch_image_name, scratch_text_name_root)

    return text


if __name__ == '__main__':
    im = Image.open('phototest.tif')
    text = image_to_string(im)
    print(text)
    try:
        text = image_file_to_string('fnord.tif', graceful_errors=False)
    except Exception as e:
        print('fnord.tif is incompatible filetype.  Try graceful_errors=True')

    text = image_file_to_string('fnord.tif', graceful_errors=True)
    print('fnord.tif contents:', text)
    text = image_file_to_string('fonts_test.png', graceful_errors=True)
    print(text)