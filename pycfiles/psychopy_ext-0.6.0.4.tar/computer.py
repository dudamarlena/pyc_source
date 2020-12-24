# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qbilius/Dropbox (MIT)/psychopy_ext/psychopy_ext/demos/scripts/computer.py
# Compiled at: 2015-12-11 19:53:07
"""
Computer configuration file
===========================

Specify default settings for all computers where you run your experiment such
as a monitor size or root path to storing data. This is intended as a more
portable and extended version of PsychoPy's MonitorCenter.

A computer is recognized by its mac address which is dependent on its
hardware and by its name. In the future versions of psychopy_ext,
if anything in the hardware changes, you'll see a warning.

# TODO: split computer configuration and defaults possibly by moving to a
config file

"""
import uuid, platform
recognized = True
root = '.'
stereo = False
default_keys = {'exit': ('lshift', 'escape'), 'trigger': 'space'}
valid_responses = {'f': 0, 'j': 1}
distance = 80
width = 37.5
screen = 0
view_scale = (1, 1)
mac = uuid.getnode()
system = platform.uname()[0]
name = platform.uname()[1]
if mac == 153254424819 and system == 'Linux':
    distance = 80
    width = 37.5
    root = '/media/qbilius/Data/data/'
elif mac == 153254424819 and system == 'Windows':
    root = 'D:/data/'
elif mac == 145320949993177:
    distance = 127
    width = 60
    view_scale = [1, -1]
    default_keys['trigger'] = 5
    valid_responses = {'9': 0, '8': 1, '7': 2, '6': 3}
else:
    recognized = False