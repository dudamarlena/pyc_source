# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sy85\binreader.py
# Compiled at: 2010-04-10 11:44:49
"""Generic functions for reading/writing binary data with arbitrary
fixed-field-length formats.
"""
import converters, logging
from data import voice
SOX = b'\xf0'
MANUFACTURER_ID = 'C'

class NullHandler(logging.Handler):

    def emit(self, record):
        pass


log = logging.getLogger(__name__)
log.addHandler(NullHandler())

def is_yamaha_sysex(data):
    """Return True if given data looks like a Yamaha sysex bulk dump."""
    return len(data) >= 8 and data.startswith(SOX + MANUFACTURER_ID)


def read_patch(data, format):
    """Parse given binary data according to format specified in format.

    Returns a dictionary with data field number as key and an 2-item tuple
    with the data field name and the converted data field value as the value.

    """

    def add_value(patch, param_no, name, value):
        if isinstance(value, tuple):
            value = (
             name,) + value
        else:
            value = (
             name, value)
        if param_no in patch:
            if not isinstance(patch[param_no], list):
                patch[param_no] = [
                 patch[param_no]]
            patch[param_no].append(value)
        else:
            patch[param_no] = value

    patch = dict()
    for line in format:
        (offset, length, param_no, name, cv_func_name) = line[:5]
        if param_no is None:
            continue
        cv_func_args = line[5:]
        cv_func = getattr(converters, cv_func_name)
        value = data[line[0]:line[0] + line[1]]
        try:
            value = cv_func(value, *cv_func_args)
            add_value(patch, param_no, name, value)
        except Exception, exc:
            log.error("Exception while calling converter function '%s' for param #%i (offset %i). Saving raw binary value.\nError: %s", cv_func_name, param_no, offset, exc)
            log.debug('Raw value: %r', value)
            add_value(patch, param_no, name, value)
            raise

    return patch


def make_logger():
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger(__name__).addHandler(console)
    return console


if __name__ == '__main__':
    import sys, pprint
    make_logger()
    syx = open(sys.argv[1], 'rb').read()
    if is_yamaha_sysex(syx):
        try:
            vc = read_patch(syx[32:-2], voice.VOICE_SYSEX_FORMAT)
            pprint.pprint(vc)
        except Exception, exc:
            print 'Voice parsing failed: %s' % exc
            raise

    else:
        print 'Sysex format not recognized.'
        sys.exit(2)