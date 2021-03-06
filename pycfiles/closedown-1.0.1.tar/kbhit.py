# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/okay/tonka/src/livetitles/src/kbhit.py
# Compiled at: 2018-01-03 11:34:41
__doc__ = "\nA Python class implementing KBHIT, the standard keyboard-interrupt poller.\nWorks transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work\nwith IDLE.\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU Lesser General Public License as \npublished by the Free Software Foundation, either version 3 of the \nLicense, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\n"
import os
if os.name == 'nt':
    import msvcrt
else:
    import sys, termios, atexit
    from select import select

class KBHit:

    def __init__(self):
        """Creates a KBHit object that you can call to do various keyboard things.
        """
        if os.name == 'nt':
            pass
        else:
            self.fd = sys.stdin.fileno()
            self.new_term = termios.tcgetattr(self.fd)
            self.old_term = termios.tcgetattr(self.fd)
            self.new_term[3] = self.new_term[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)
            atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """ Resets to normal terminal.  On Windows this is a no-op.
        """
        if os.name == 'nt':
            pass
        else:
            termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def getch(self):
        """ Returns a keyboard character after kbhit() has been called.
            Should not be called in the same program as getarrow().
        """
        s = ''
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        else:
            return sys.stdin.read(1)

    def getarrow(self):
        """ Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        """
        if os.name == 'nt':
            msvcrt.getch()
            c = msvcrt.getch()
            vals = [72, 77, 80, 75]
        else:
            c = sys.stdin.read(3)[2]
            vals = [65, 67, 66, 68]
        return vals.index(ord(c.decode('utf-8')))

    def kbhit(self):
        """ Returns True if keyboard character was hit, False otherwise.
        """
        if os.name == 'nt':
            return msvcrt.kbhit()
        else:
            dr, dw, de = select([sys.stdin], [], [], 0)
            return dr != []


if __name__ == '__main__':
    kb = KBHit()
    print 'Hit any key, or ESC to exit'
    while True:
        if kb.kbhit():
            c = kb.getch()
            if ord(c) == 27:
                break
            print c

    kb.set_normal_term()