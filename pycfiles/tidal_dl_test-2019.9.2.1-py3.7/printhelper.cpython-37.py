# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tidal_dl\printhelper.py
# Compiled at: 2019-09-04 12:41:15
# Size of source mod 2**32: 2874 bytes
from aigpy import cmdHelper
from aigpy import systemHelper

def printErr(length, elsestr):
    cmdHelper.myprint('[ERR]'.ljust(length), cmdHelper.TextColor.Red, None)
    print(elsestr)


def printWarring(length, elsestr):
    cmdHelper.myprint('[WARRING]'.ljust(length), cmdHelper.TextColor.Red, None)
    print(elsestr)


def printSUCCESS(length, elsestr):
    cmdHelper.myprint('[SUCCESS]'.ljust(length), cmdHelper.TextColor.Green, None)
    print(elsestr)


def printChoice(string, isInt=False, default=None):
    tmpstr = ''
    cmdHelper.myprint(string, cmdHelper.TextColor.Yellow, None)
    if not isInt:
        return cmdHelper.myinput(tmpstr)
    return cmdHelper.myinputInt(tmpstr, default)


def printChoice2(string, default=None):
    ret = printChoice(string, False, default)
    try:
        iret = int(ret)
        return (ret, iret)
    except:
        return (
         ret, default)


def printMenu():
    print('=====================Choice=========================')
    cmdHelper.myprint(" Enter '0': ", cmdHelper.TextColor.Green, None)
    print('Exit.')
    cmdHelper.myprint(" Enter '1': ", cmdHelper.TextColor.Green, None)
    print('LogIn And Get SessionID.')
    cmdHelper.myprint(" Enter '2': ", cmdHelper.TextColor.Green, None)
    print('Setting(OutputDir/Quality/ThreadNum).')
    cmdHelper.myprint(" Enter '3': ", cmdHelper.TextColor.Green, None)
    print('Download Album.')
    cmdHelper.myprint(" Enter '4': ", cmdHelper.TextColor.Green, None)
    print('Download Track.')
    cmdHelper.myprint(" Enter '5': ", cmdHelper.TextColor.Green, None)
    print('Download PlayList.')
    cmdHelper.myprint(" Enter '6': ", cmdHelper.TextColor.Green, None)
    print('Download Video.')
    cmdHelper.myprint(" Enter '7': ", cmdHelper.TextColor.Green, None)
    print('Download Favorite.')
    cmdHelper.myprint(" Enter '8': ", cmdHelper.TextColor.Green, None)
    print('Download ArtistAlbum.')
    cmdHelper.myprint(" Enter '9': ", cmdHelper.TextColor.Green, None)
    print('Show Config.')
    cmdHelper.myprint(' Enter URL: ', cmdHelper.TextColor.Green, None)
    print('Download By Url.')
    cmdHelper.myprint(' Enter Path: ', cmdHelper.TextColor.Green, None)
    print('Download By File.')
    print('====================================================')


LOG = '\n /$$$$$$$$ /$$       /$$           /$$               /$$ /$$\n|__  $$__/|__/      | $$          | $$              | $$| $$\n   | $$    /$$  /$$$$$$$  /$$$$$$ | $$          /$$$$$$$| $$\n   | $$   | $$ /$$__  $$ |____  $$| $$ /$$$$$$ /$$__  $$| $$\n   | $$   | $$| $$  | $$  /$$$$$$$| $$|______/| $$  | $$| $$\n   | $$   | $$| $$  | $$ /$$__  $$| $$        | $$  | $$| $$\n   | $$   | $$|  $$$$$$$|  $$$$$$$| $$        |  $$$$$$$| $$\n   |__/   |__/ \\_______/ \\_______/|__/         \\_______/|__/\n   \n       https://github.com/yaronzz/Tidal-Media-Downloader \n'