# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\arcadeplus\examples\sound_example.py
# Compiled at: 2020-03-29 18:08:49
# Size of source mod 2**32: 693 bytes
__doc__ = '\nSound Demo\n\nIf Python and arcadeplus are installed, this example can be run from the command line with:\npython -m arcadeplus.examples.sound\n'
import arcadeplus, os
file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)
arcadeplus.open_window(300, 300, 'Sound Demo')
laser_sound = arcadeplus.load_sound(':resources:sounds/laser1.wav')
arcadeplus.play_sound(laser_sound)
arcadeplus.run()