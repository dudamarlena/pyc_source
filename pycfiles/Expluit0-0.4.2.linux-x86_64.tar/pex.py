# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/expluit0/encoder/pex.py
# Compiled at: 2012-07-10 13:42:43
import random
NOPS = [
 [
  b'\x90', ['nop']],
 [
  b'\x97', ['eax', 'edi']],
 [
  b'\x96', ['eax', 'esi']],
 [
  b'\x95', ['eax', 'ebp']],
 [
  b'\x93', ['eax', 'ebx']],
 [
  b'\x92', ['eax', 'edx']],
 [
  b'\x91', ['eax', 'ecx']],
 [
  b'\x99', ['edx']],
 [
  'M', ['ebp']],
 [
  'H', ['eax']],
 [
  'G', ['edi']],
 [
  'O', ['edi']],
 [
  '@', ['eax']],
 [
  'A', ['ecx']],
 [
  '7', ['eax']],
 [
  '?', ['eax']],
 [
  "'", ['eax']],
 [
  '/', ['eax']],
 [
  'F', ['esi']],
 [
  'N', ['esi']],
 [
  b'\xfc', []],
 [
  b'\xfd', []],
 [
  b'\xf8', []],
 [
  b'\xf9', []],
 [
  b'\xf5', []],
 [
  b'\x98', ['eax']],
 [
  b'\x9f', ['eax']],
 [
  'J', ['edx']],
 [
  'D', ['esp']],
 [
  'B', ['edx']],
 [
  'C', ['ebx']],
 [
  'I', ['ecx']],
 [
  'K', ['ebx']],
 [
  'E', ['ebp']],
 [
  'L', ['esp']],
 [
  b'\x9b', []],
 [
  '`', ['esp']],
 [
  '\x0e', ['esp']],
 [
  '\x1e', ['esp']],
 [
  'P', ['esp']],
 [
  'U', ['esp']],
 [
  'S', ['esp']],
 [
  'Q', ['esp']],
 [
  'W', ['esp']],
 [
  'R', ['esp']],
 [
  '\x06', ['esp']],
 [
  'V', ['esp']],
 [
  'T', ['esp']],
 [
  '\x16', ['esp']],
 [
  'X', ['esp', 'eax']],
 [
  ']', ['esp', 'ebp']],
 [
  '[', ['esp', 'ebx']],
 [
  'Y', ['esp', 'ecx']],
 [
  '_', ['esp', 'edi']],
 [
  'Z', ['esp', 'edx']],
 [
  '^', ['esp', 'esi']],
 [
  b'\xd6', ['eax']]]

def NopGenerator(length):
    nops = [ x[0] for x in NOPS ]
    nopsled = ''
    for i in range(length):
        nopsled += random.choice(nops)

    return nopsled


def nopInPython(nopsled):
    pass


def nopInC(nopsled):
    nopCodes = '// total %d (0x%x) bytes\n' % (len(nopsled), len(nopsled))
    nopCodes += 'unsigned char NOP[] = \n'
    for i in range(0, len(nopsled), 8):
        nopCodes += '"'
        nopCodes += '\\x' + ('\\x').join([ '%02x' % ord(x) for x in nopsled[i:i + 8] ])
        nopCodes += '"\n'

    nopCodes = nopCodes[:-1] + ';\n'
    return nopCodes


if __name__ == '__main__':
    nopsled = NopGenerator(128)
    print nopInC(nopsled)