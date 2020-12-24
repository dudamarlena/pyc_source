# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\clock.py
# Compiled at: 2020-04-30 10:09:23
# Size of source mod 2**32: 3321 bytes
"""       turtle-example-suite:

             tdemo_clock.py

Enhanced clock-program, showing date
and time
  ------------------------------------
   Press STOP to exit the program!
  ------------------------------------
"""
from turtle import *
from datetime import datetime

def jump(distanz, winkel=0):
    penup()
    right(winkel)
    forward(distanz)
    left(winkel)
    pendown()


def hand(laenge, spitze):
    fd(laenge * 1.15)
    rt(90)
    fd(spitze / 2.0)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze / 2.0)


def make_hand_shape(name, laenge, spitze):
    reset()
    jump(-laenge * 0.15)
    begin_poly()
    hand(laenge, spitze)
    end_poly()
    hand_form = get_poly()
    register_shape(name, hand_form)


def clockface(radius):
    reset()
    pensize(7)
    for i in range(60):
        jump(radius)
        if i % 5 == 0:
            fd(25)
            jump(-radius - 25)
        else:
            dot(3)
            jump(-radius)
        rt(6)


def setup():
    global hour_hand
    global minute_hand
    global second_hand
    global writer
    mode('logo')
    make_hand_shape('second_hand', 125, 25)
    make_hand_shape('minute_hand', 130, 25)
    make_hand_shape('hour_hand', 90, 25)
    clockface(160)
    second_hand = Turtle()
    second_hand.shape('second_hand')
    second_hand.color('gray20', 'gray80')
    minute_hand = Turtle()
    minute_hand.shape('minute_hand')
    minute_hand.color('blue1', 'red1')
    hour_hand = Turtle()
    hour_hand.shape('hour_hand')
    hour_hand.color('blue3', 'red3')
    for hand in (second_hand, minute_hand, hour_hand):
        hand.resizemode('user')
        hand.shapesize(1, 1, 3)
        hand.speed(0)

    ht()
    writer = Turtle()
    writer.ht()
    writer.pu()
    writer.bk(85)


def wochentag(t):
    wochentag = [
     'Monday', 'Tuesday', 'Wednesday',
     'Thursday', 'Friday', 'Saturday', 'Sunday']
    return wochentag[t.weekday()]


def datum(z):
    monat = [
     'Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June',
     'July', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']
    j = z.year
    m = monat[(z.month - 1)]
    t = z.day
    return '%s %d %d' % (m, t, j)


def tick():
    t = datetime.today()
    sekunde = t.second + t.microsecond * 1e-06
    minute = t.minute + sekunde / 60.0
    stunde = t.hour + minute / 60.0
    try:
        tracer(False)
        writer.clear()
        writer.home()
        writer.forward(65)
        writer.write((wochentag(t)), align='center',
          font=('Courier', 14, 'bold'))
        writer.back(150)
        writer.write((datum(t)), align='center',
          font=('Courier', 14, 'bold'))
        writer.forward(85)
        tracer(True)
        second_hand.setheading(6 * sekunde)
        minute_hand.setheading(6 * minute)
        hour_hand.setheading(30 * stunde)
        tracer(True)
        ontimer(tick, 100)
    except Terminator:
        pass


def main():
    tracer(False)
    setup()
    tracer(True)
    tick()
    return 'EVENTLOOP'


def clock():
    mode('logo')
    msg = main()
    print(msg)
    mainloop()