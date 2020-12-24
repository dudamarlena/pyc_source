# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.6/site-packages/ioflo/base/interfacing.py
# Compiled at: 2017-12-17 08:35:26
# Size of source mod 2**32: 4297 bytes
"""interfacing.py  remote host interfacing module

"""
import pickle, pdb, string, math, types, os, time, copy
from collections import deque
from ..aid.sixing import *
from ..aid.consoling import getConsole
console = getConsole()

class NMEAParser(object):
    __doc__ = 'NMEA Serial String Parser Object\n\n       NMEA-0183\n\n       Under the NMEA-0183 standard, all characters used are printable\n       ASCII text (plus carriage return and line feed).  NMEA-0183 data\n       is sent at 4800 baud.\n\n       The data is transmitted in the form of "sentences".  Each\n       sentence starts with a "$", a two letter "talker ID", a three\n       letter "sentence ID", followed by a number of data fields\n       separated by commas, and terminated by an optional checksum, and\n       a carriage return/line feed.  A sentence may contain up to 82\n       characters including the "$" and CR/LF.\n\n       If data for a field is not available, the field is simply\n       omitted, but the commas that would delimit it are still sent,\n       with no space between them.\n\n       Since some fields are variable width, or may be omitted as\n       above, the receiver should locate desired data fields by\n       counting commas, rather than by character position within the\n       sentence.\n\n       The optional checksum field consists of a "*" and two hex digits\n       representing the exclusive OR of all characters between, but not\n       including, the "$" and "*".  A checksum is required on some\n       sentences.\n\n       The standard allows individual manufacturers to define\n       proprietary sentence formats.  These sentences start with "$P",\n       then a 3 letter manufacturer ID, followed by whatever data the\n       manufacturer wishes, following the general format of the\n       standard sentences.\n\n       Some common talker IDs are:\n              GP      Global Positioning System receiver\n              LC      Loran-C receiver\n              OM      Omega Navigation receiver\n              II      Integrated Instrumentation\n                              (eg. AutoHelm Seatalk system)\n\n    '

    def __init__(self):
        """Initialize instance   """
        pass

    def validate(self, sentence):
        """   Validates NMEA string and strips off leading $ and trailing optional
              checksum and linefeed if any

              If fails any test returns "" empty string
              Otherwise returns stripped string

              Tests:
                 length of string <= 82
                 first char is $
                 no more than one checksum indicator * exists
                 if checksum indicator
                    it is in correct position and valid

        """
        if len(sentence) > 82:
            return ''
        else:
            if sentence[0] != '$':
                return ''
            else:
                sentence = sentence.rstrip()
                sentence = sentence[1:]
                spot = sentence.rfind('*')
                lspot = sentence.find('*')
                if spot != lspot:
                    return ''
                if spot != -1:
                    if spot != len(sentence) - 3:
                        return ''
                    sentence, given = sentence.rsplit('*')
                    given = int(given, 16)
                    check = 0
                    for c in sentence:
                        check += ord(c)
                        check %= 256

                    if check != given:
                        return ''
            return sentence

    def parse(self, sentence):
        """parse nemea sentence """
        chunks = sentence.split(',')

    def validateFile(self, fname):
        fp = open(fname, 'r')
        valid = True
        fp.close()