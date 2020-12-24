# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\conne\Desktop\Flock_SSG-master\Flock\src\settings.py
# Compiled at: 2018-12-05 21:30:13
# Size of source mod 2**32: 1118 bytes
import os, re
DEBUG = False
PREFS_FOLDER = os.path.expanduser('~\\.flock_preferences')
LOG_FILE = PREFS_FOLDER + '\\log\\'
FIRST_USE_FILE = PREFS_FOLDER + 'firstUse'
DICTIONARY_FILE = PREFS_FOLDER + 'flock_dictionary.txt'
THEMES_FOLDER = PREFS_FOLDER + '\\Themes'

def LOG(string):
    global DEBUG
    LOG_FILE_FIXED = re.sub(':', '-', LOG_FILE)
    LOG_FILE_FIXED = list(LOG_FILE_FIXED)
    LOG_FILE_FIXED[1] = ':'
    LOG_FILE_FIXED = ''.join(LOG_FILE_FIXED)
    f = open(LOG_FILE_FIXED, 'a+')
    f.write('\n' + string)
    f.close()
    if DEBUG:
        print(string)


def createPreferencesFolder():
    global PREFS_FOLDER
    if not os.path.isdir(PREFS_FOLDER):
        os.mkdir(PREFS_FOLDER)
        os.mkdir(PREFS_FOLDER + '\\log')