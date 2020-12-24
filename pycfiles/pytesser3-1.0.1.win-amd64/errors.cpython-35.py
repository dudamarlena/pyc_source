# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Anaconda3\Lib\site-packages\pytesser3\errors.py
# Compiled at: 2016-09-22 23:33:35
# Size of source mod 2**32: 418 bytes
"""Test for exceptions raised in the tesseract.exe logfile"""

class Tesser_General_Exception(Exception):
    pass


class Tesser_Invalid_Filetype(Tesser_General_Exception):
    pass


def check_for_errors(logfile='tesseract.log'):
    inf = open(logfile)
    text = inf.read()
    inf.close()
    if text.find('Error') != -1:
        raise Tesser_General_Exception