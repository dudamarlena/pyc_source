# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\conne\Desktop\Flock_SSG-master\Flock\src\themeSelector.py
# Compiled at: 2018-12-04 23:20:59
# Size of source mod 2**32: 3279 bytes
from . import settings
import shutil
FLOCK_ICON_PATH = settings.THEMES_FOLDER + 'flock_icon.png'
THEME_FOLDER = settings.THEMES_FOLDER
THEME_NAMES = '\n 1. Light theme\n 2. Dark theme\n 3. Fun theme\n 4. Blue Accent\n 5. Firebrick Accent\n 6. Green Accent\n 7. Orange Accent\n 8. Purple Accent\n 9. Select your own\n'

def selectTheme(destinationFolder):
    THEME_VALID = False
    while not THEME_VALID:
        print('Available themes' + THEME_NAMES)
        themeOption = input('Choose a theme: ')
        if themeOption == '1':
            settings.LOG('Light theme choosen')
            theme = 'light_theme'
            themePath = THEME_FOLDER + theme + '.css'
            THEME_VALID = True
        elif themeOption == '2':
            settings.LOG('Dark theme choosen')
            theme = 'dark_theme'
            themePath = THEME_FOLDER + theme + '.css'
            THEME_VALID = True
        elif themeOption == '3':
            settings.LOG('Fun theme choosen')
            theme = 'fun_theme'
            themePath = THEME_FOLDER + theme + '.css'
            THEME_VALID = True
        elif themeOption == '4':
            settings.LOG('Blue Accent theme selected')
            theme = 'std_blue'
            themePath = THEME_FOLDER + theme + '.css'
            THEME_VALID = True
        elif themeOption == '5':
            settings.LOG('Firebrick Accent theme selected')
            theme = 'std_firebrick'
            themePath = THEME_FOLDER + theme + '.css'
            THEME_VALID = True
        elif themeOption == '6':
            settings.LOG('Green Accent theme selected')
            theme = 'std_green'
            themePath = THEME_FOLDER + theme + '.css'
            THEME_VALID = True
        elif themeOption == '7':
            settings.LOG('Orange Accent theme selected')
            theme = 'std_orange'
            themePath = THEME_FOLDER + theme + '.css'
            THEME_VALID = True
        elif themeOption == '8':
            settings.LOG('Purple Accent theme selected')
            theme = 'std_purple'
            themePath = THEME_FOLDER + theme + '.css'
            THEME_VALID = True
        elif themeOption == '9':
            settings.LOG('Custom user theme selected')
            themePath = input('Insert the path and name to your custom theme: ')
            THEME_VALID = True
        else:
            settings.LOG('The selected theme does not exist')
            print('\nPlease choose a valid theme')

    shutil.copy2(themePath, destinationFolder + '/styles.css')
    shutil.copy2(FLOCK_ICON_PATH, destinationFolder + '/flock_icon.png')