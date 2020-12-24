# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pfigue/Workspace/hex2words/venv-3.4-setup/lib/python3.4/site-packages/hex2words/input.py
# Compiled at: 2015-08-17 03:57:22
# Size of source mod 2**32: 3169 bytes
from __future__ import absolute_import
from __future__ import print_function
import re, logging
logger = logging.getLogger(__name__)
from .hex2words import hex2words
re_blanks_pattern = re.compile('[\\ \\t\\n]')
re_symbols_pattern = re.compile('[:\\ -]')
re_GPG_line_pattern = re.compile('^\\s+Key fingerprint = ([a-zA-Z0-9\\s]+)$')
re_XXXsum_line_pattern = re.compile('^([a-zA-Z0-9]+)\\s+(\\S+)$')
re_hexasWithSymbols_line_pattern = re.compile('^([a-zA-Z0-9]+)$')

def process_GPG_output_line(line):
    """Parses the line as it is from `GPG --list-keys` command
If the format doesn't fit, returns None.
If it does fit, returns the hex hash of the key
"""
    result = re_GPG_line_pattern.match(line)
    if result is None:
        return
    fp_str = result.group(1)
    fp_str = re_blanks_pattern.sub('', fp_str)
    return fp_str


def process_XXXsum_output_line(line):
    """Parses the line as it is from `sha256sum` or similar command.
If the format doesn't fit, returns None.
If it does fit, returns a duple: the hex hash and the filename
"""
    result = re_XXXsum_line_pattern.match(line)
    if result is None:
        return
    fp_str = result.group(1)
    filename = result.group(2)
    return (fp_str, filename)


def process_hexasWithSymbols_output_line(line):
    line = line.strip()
    clean_line = re_symbols_pattern.sub('', line)
    result = re_hexasWithSymbols_line_pattern.match(clean_line)
    if result is None:
        return
    fp_str = result.group(1)
    return (line, fp_str)


def process_input(lines):
    TYPE_UNDEFINED, TYPE_XXXsum, TYPE_GPG, TYPE_hexasWithSymbols = range(4)
    output = ''
    output_type = TYPE_UNDEFINED
    for line in lines:
        if not line:
            continue
        if output_type in (TYPE_UNDEFINED, TYPE_XXXsum):
            result = process_XXXsum_output_line(line)
            if result is not None:
                output_type = TYPE_XXXsum
                fp_str, filename = result
                msg = '{0}:\n\t{1}\n\t{2}\n\n'
                msg = msg.format(filename, fp_str, word_it(fp_str))
                output += msg
        if output_type in (TYPE_UNDEFINED, TYPE_GPG):
            result = process_GPG_output_line(line)
            if result is not None:
                output_type = TYPE_GPG
                fp_str = result
                msg = '{0}: {1}\n\n'.format(fp_str, word_it(fp_str))
                output += msg
            if output_type in (TYPE_UNDEFINED, TYPE_hexasWithSymbols):
                result = process_hexasWithSymbols_output_line(line)
                if result is not None:
                    output_type = TYPE_hexasWithSymbols
                    line_wospaces, fp_str = result
                    msg = '{0}\n\t{1}\n\n'.format(line_wospaces, word_it(fp_str))
                    output += msg
                else:
                    continue

    if output_type == TYPE_UNDEFINED:
        logger.error('Sorry, I can not identify the format of the input.')
        return
    return output


def word_it(fp_str):
    words = hex2words(fp_str)
    words = words.lower()
    return words