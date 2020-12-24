# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/turtleart/scripts/qturtle.py
# Compiled at: 2017-02-06 01:13:11
import logging, turtle, turtleart.draw, IPython

def main():
    logging.basicConfig(level='DEBUG')
    log = logging.getLogger()
    turtle_name = raw_input("What is the turtle's name?> ")
    log.debug('Creating turtle named: %s' % turtle_name)
    myturtle = globals()[turtle_name] = turtle.Turtle()
    log.debug('Making a screen')
    screen = turtle.Screen()
    log.debug("Setting %s's speed to 10 to go FAST." % turtle_name)
    myturtle.speed(10)
    log.debug('Making a graph to give some orientation.')
    turtleart.draw.makegraph(myturtle)
    myturtle.goto(0, 0)
    IPython.start_ipython(user_ns={turtle_name: myturtle, 'screen': screen})