# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cube\cube.py
# Compiled at: 2007-04-06 01:02:27
from OpenGL import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys, os, traceback, pygame
from pygame.locals import *
import pygame.mouse, pcapy, socket, struct, string
from optparse import OptionParser
import re
from Tkinter import *
from config import TkinterConfigParser
import network, display

def main(argv=None):
    from controllers import ConfigurationController, NetworkController, DisplayController, GraphicsController, PygameEventsController, SchedulingController, QuitEvent
    configcon = ConfigurationController(argv=argv)
    networkcon = NetworkController(config=configcon.parser)
    displaycon = DisplayController(config=configcon.parser)
    graphicscon = GraphicsController(config=configcon.parser)
    networkcon.grapher = graphicscon.grapher
    eventcon = PygameEventsController(config=configcon.parser)
    schedcon = SchedulingController(config=configcon.parser, perfevery=0)
    schedcon.add_target('network', networkcon.run, mindelay=100)
    schedcon.add_target('display', displaycon.run, mindelay=100)
    schedcon.add_target('graphics', graphicscon.run, mindelay=100)
    schedcon.add_target('events', eventcon.run, mindelay=100)

    def update_fps(s=None, o=None, v=None):
        v = configcon.parser.getfloat('display', 'fps')
        if v > 0:
            schedcon.targets['graphics'].mindelay = int(1000.0 / configcon.parser.getfloat('display', 'fps'))
        else:
            schedcon.targets['graphics'].mindelay = 0

    configcon.parser.trace('display', 'fps', update_fps)
    update_fps()
    if argv is None:
        argv = sys.argv

    def updatefilter(s, o, v):
        try:
            networkcon.reader.reader.setfilter(v)
        except pcapy.PcapError, e:
            print 'Invalid filter: %s' % v

    configcon.parser.trace('capture', 'filter', updatefilter)
    while 1:
        try:
            schedcon.run()
        except QuitEvent:
            break

    configcon.stop()
    return


if __name__ == '__main__':
    import time
    delay = 5
    run_times = 1
    while delay > 0 or run_times > 0:
        if run_times > 0:
            run_times -= 1
        try:
            sys.exit(main())
        except SystemExit:
            break
        except KeyboardInterrupt:
            break
        except Exception, e:
            print 'Exception: %s' % e
            traceback.print_exc(file=sys.stdout)
            print 'Sleeping %s seconds before restart...' % delay
            time.sleep(delay)
            continue