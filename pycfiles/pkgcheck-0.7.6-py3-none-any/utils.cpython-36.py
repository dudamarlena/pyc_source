# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/utils.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 4442 bytes
"""Various miscellaneous utility functions."""
_control_chars = b'\n\r\t\x0c\x08'
_printable_ascii = _control_chars + bytes(range(32, 127))
_printable_high_ascii = bytes(range(127, 256))

def is_binary(path, blocksize=1024):
    """Check if a given file is binary or not.

    Uses a simplified version of the Perl detection algorithm, based roughly on
    Eli Bendersky's translation to Python:
    http://eli.thegreenplace.net/2011/10/19/perls-guess-if-file-is-text-or-binary-implemented-in-python/

    This is biased slightly more in favour of deeming files as text files than
    the Perl algorithm, since all ASCII compatible character sets are accepted as
    text, not just utf-8.

    :param path: Path to a file to check.
    :param blocksize: Amount of bytes to read for determination.
    :returns: True if appears to be a binary, otherwise False.
    """
    try:
        with open(path, 'rb') as (f):
            byte_str = f.read(blocksize)
    except IOError:
        return False
    else:
        if not byte_str:
            return False
        else:
            low_chars = byte_str.translate(None, _printable_ascii)
            nontext_ratio1 = len(low_chars) / len(byte_str)
            high_chars = byte_str.translate(None, _printable_high_ascii)
            nontext_ratio2 = len(high_chars) / len(byte_str)
            is_likely_binary = nontext_ratio1 > 0.3 and nontext_ratio2 < 0.05 or nontext_ratio1 > 0.8 and nontext_ratio2 > 0.8
            decodable = False
            try:
                byte_str.decode()
                decodable = True
            except UnicodeDecodeError:
                import chardet
                detected_encoding = chardet.detect(byte_str)
                if detected_encoding['confidence'] > 0.8:
                    try:
                        byte_str.decode(encoding=(detected_encoding['encoding']))
                        decodable = True
                    except (UnicodeDecodeError, LookupError):
                        pass

            if decodable:
                return False
            if is_likely_binary or b'\x00' in byte_str:
                return True
            return False