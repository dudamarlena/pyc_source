# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/quiik/core.py
# Compiled at: 2019-09-08 01:26:44
# Size of source mod 2**32: 5161 bytes
from fabulous import text
import random, termios, fcntl, sys, os
from time import time, sleep

def wait_key():
    """ Wait for a key press on the console and return it. """
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        try:
            try:
                result = sys.stdin.read(1)
            except IOError:
                pass

        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result


def clear_scr():
    if 'win32' in sys.platform or 'win64' in sys.platform:
        os.system('cls')
    else:
        os.system('clear')


wasd_keys = {'up':'w', 
 'down':'s', 
 'left':'a', 
 'right':'d'}
ijkl_keys = {'up':'i', 
 'down':'k', 
 'left':'j', 
 'right':'l'}

class Game:

    def __init__(self, key_choice):
        self.score = 0
        self.keys = []
        if key_choice:
            for k, v in ijkl_keys.items():
                self.keys.append(v)

        else:
            for k, v in wasd_keys.items():
                self.keys.append(v)

    def random_key(self):
        count = random.randint(0, 3)
        return self.keys[count]

    def display_menu(self):
        try:
            if 'win32' in sys.platform or 'win64' in sys.platform:
                os.system('cls')
            else:
                os.system('clear')
            r = lambda : random.randint(0, 255)
            hex = '#%02X%02X%02X' % (r(), r(), r())
            print(text.Text('Quiik!', color=hex, shadow=True, skew=5))
            sleep(3)
            if 'win32' in sys.platform or 'win64' in sys.platform:
                os.system('cls')
            else:
                os.system('clear')
            print(text.Text('Created by', color=hex, shadow=True, skew=5))
            print(text.Text('Max Bridgland', color=hex, shadow=True, skew=5))
            sleep(3)
            if 'win32' in sys.platform or 'win64' in sys.platform:
                os.system('cls')
            else:
                os.system('clear')
            print(text.Text('Answer In', color=hex, shadow=True, skew=5))
            print(text.Text('1 Second', color=hex, shadow=True, skew=5))
            sleep(3)
            if 'win32' in sys.platform or 'win64' in sys.platform:
                os.system('cls')
            else:
                os.system('clear')
            print(text.Text('Times Up?', color=hex, shadow=True, skew=5))
            print(text.Text("You're Out!", color=hex, shadow=True, skew=5))
            sleep(3)
        except KeyboardInterrupt:
            clear_scr()
            print(text.Text('Goodbye!', color=('#%02X%02X%02X' % (255, 50, 50)), shadow=True))
            exit()

    def display_random_key(self, key):
        try:
            if 'win32' in sys.platform or 'win64' in sys.platform:
                os.system('cls')
            else:
                os.system('clear')
            r = lambda : random.randint(0, 255)
            hex = '#%02X%02X%02X' % (r(), r(), r())
            print(text.Text(('Press: ' + key), color=hex, shadow=True, skew=5))
        except KeyboardInterrupt:
            clear_scr()
            print(text.Text('Goodbye!', color=('#%02X%02X%02X' % (255, 50, 50)), shadow=True))
            exit()

    def start_screen(self):
        clear_scr()
        r = lambda : random.randint(0, 255)
        hex = '#%02X%02X%02X' % (r(), r(), r())
        print(text.Text('Press S to Start', color=hex, shadow=True, skew=5))
        while wait_key() == 's':
            break

    def end_screen(self):
        try:
            print(text.Text('Game Over', color=('#%02X%02X%02X' % (255, 50, 50)), shadow=True))
            print(text.Text(('Points: ' + str(self.score)), color=('#%02X%02X%02X' % (255,
                                                                                      50,
                                                                                      50)), shadow=True))
            sleep(3)
            clear_scr()
            print(text.Text('Play Again? Y/N', color=('#%02X%02X%02X' % (255, 50, 50)), shadow=True))
            while 1:
                key = wait_key()
                if key.lower() == 'y':
                    return True
                if key.lower() == 'n':
                    return False

        except KeyboardInterrupt:
            clear_scr()
            print(text.Text('Goodbye!', color=('#%02X%02X%02X' % (255, 50, 50)), shadow=True))
            exit()