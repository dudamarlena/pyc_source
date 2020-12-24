# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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