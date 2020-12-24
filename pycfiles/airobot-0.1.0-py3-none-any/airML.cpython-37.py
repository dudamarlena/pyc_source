# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/oshara/GSoC/DBPedia/airML/src/airML.py
# Compiled at: 2020-05-08 12:36:03
# Size of source mod 2**32: 373 bytes
import sys, os

def kbox_execute():
    JAR_EXECUTE = 'java -jar kbox.jar'
    if len(sys.argv) == 1:
        returned_output = os.system(JAR_EXECUTE)
    else:
        arg = ' '.join(sys.argv[1:])
        execute = JAR_EXECUTE + ' ' + arg
        returned_output = os.system(execute)


if __name__ == '__main__':
    kbox_execute()