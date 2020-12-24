# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\spammer.py
# Compiled at: 2019-08-22 15:07:50
# Size of source mod 2**32: 1426 bytes
import pyautogui, time, random, threading
print('module lancer')

def aide(nothing):
    print('for minecraft spamming write this for exemple : minecraft(3,"mineraft spammings"",10,0.5)')


def spam(text, number, delay):
    time.sleep(5)

    def start():
        for x in range(0, number):
            r = str(random.randint(10, 99999999999999999999999999999999999999999999999999999))
            pyautogui.typewrite(r)
            pyautogui.typewrite(['enter'])
            time.sleep(temp)


def minecraft(text, number, temp):
    time.sleep(5)
    if text == random:
        for x in range(0, number):
            r = str(random.randint(10, 99999999999999999999999999999999999999999999999999999))
            pyautogui.typewrite('t')
            pyautogui.typewrite(r)
            pyautogui.typewrite(['enter'])
            time.sleep(temp)

    else:
        for x in range(number):
            r = str(random.randint(1, 9))
            pyautogui.typewrite('t')
            pyautogui.typewrite(text + r)
            time.sleep(temp)
            pyautogui.typewrite(['enter'])