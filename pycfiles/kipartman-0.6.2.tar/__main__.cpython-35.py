# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seb/git/kipartman/kipartman/__main__.py
# Compiled at: 2017-12-13 06:03:37
# Size of source mod 2**32: 1684 bytes
import os
os.sys.path.append(os.path.dirname(os.path.abspath(__file__)))
if not os.path.exists('resources'):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
import wx
from frames.main_frame import MainFrame
import sys

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    print('Running kipartman')
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    from kicad.kicad_mod_file import KicadModFile
    f = KicadModFile()
    f.LoadFile('/home/seb/bike-alarm/bikealarm-hardware/library/Switch.pretty/SPST_B3U-1000P-B.kicad_mod')
    f.Render('/tmp/a.png')
    from kicad.kicad_lib_file import KicadLibFile
    f = KicadLibFile()
    app.MainLoop()


if __name__ == '__main__':
    main()