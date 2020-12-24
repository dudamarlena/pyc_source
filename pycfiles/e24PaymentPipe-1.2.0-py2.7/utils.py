# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/e24PaymentPipe/utils.py
# Compiled at: 2015-12-29 16:11:31
import itertools
FILTER_CHARS = [
 '~', '`', '!', '#', '$', '%', '^', '|', '\\', ':', "'", '"', '/']

def xor(cryptext=None):
    """
    :param cryptext: The crypted text to decipher
    :return: the plain text
    """
    key = 'Those who profess to favour freedom and yet depreciate agitation are men who want rain without thunder '
    key += 'and lightning'
    key = itertools.cycle(bytearray(key, 'utf-8'))
    return bytearray([ a ^ b for a, b in zip(cryptext, key) ])


def sanitize(s):
    """
    Filter out characters not allowed in the tracking id or the UDF values
    """
    return s.translate(None, ('').join(FILTER_CHARS))