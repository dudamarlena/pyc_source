# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Git\assembly-code\JARV1S-Ghidra\pywrap\ghidrapy\__main__.py
# Compiled at: 2019-12-01 11:34:53
# Size of source mod 2**32: 353 bytes
import sys, logging
logging.basicConfig(level=(logging.INFO),
  format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s',
  handlers=[
 logging.StreamHandler()])
if __name__ == '__main__':
    from ghidrapy.decompiler import process, cleanup
    process(sys.argv[1])
    cleanup(sys.argv[1])