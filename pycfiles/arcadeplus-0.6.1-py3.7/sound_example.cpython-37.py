# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sound_example.py
# Compiled at: 2020-03-29 18:08:49
# Size of source mod 2**32: 693 bytes
"""
Sound Demo

If Python and arcadeplus are installed, this example can be run from the command line with:
python -m arcadeplus.examples.sound
"""
import arcadeplus, os
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
arcadeplus.open_window(300, 300, 'Sound Demo')
laser_sound = arcadeplus.load_sound(':resources:sounds/laser1.wav')
arcadeplus.play_sound(laser_sound)
arcadeplus.run()