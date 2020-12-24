# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winontop\winontop.py
# Compiled at: 2016-08-14 13:34:42
import sys, win32gui

def enumHandler(hwnd, lParam):
    """The windows on top functionality is taken here
    Source: http://stackoverflow.com/questions/1482565/how-to-make-python-window-run-as-always-on-top"""
    if win32gui.IsWindowVisible(hwnd):
        if sys.argv[1].lower() in win32gui.GetWindowText(hwnd).lower():
            win32gui.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 1)
            return True


def showDoc():
    print 'Help Documentation\nHey folks this is an easy to use tool to keep windows on top of others.\nYou have to specify only a part of the name in windows name. No need to install any third party software.\nIf you want a chrome tab to be on top just mention any word in the title.\n\nFor eg. if you want youtube video "Game of Thrones Season 6: Episode #9 Preview (HBO)" on top\n>>> winontop thrones\nor\n>>> winontop games\n\nFor help doc\n>>> winontop -h\n\nTested on Windows 10/Python2\nFeel free to contribute or report any issues at https://github.com/jithurjacob/winontop'


def main():
    """
    Argument Parsing and help documentation
    """
    if len(sys.argv) != 2:
        print 'Incorrect number of arguments. Use -h for help'
    elif sys.argv[1] in ('-h', '--h', '-help'):
        showDoc()
    else:
        win32gui.EnumWindows(enumHandler, None)
    return


if __name__ == '__main__':
    main()