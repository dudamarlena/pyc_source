# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/head_controller/Features.py
# Compiled at: 2019-10-27 02:12:25
# Size of source mod 2**32: 3171 bytes
import sys, os, curses, cv2, time, pandas as pd
import head_controller.db as db
import json
RESIZE_FACTOR = 0.02
TRAIN_TIME = 30

def get_input(stdscr):
    k = 0
    d = ''
    while k != ord('q'):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        if k == curses.KEY_DOWN:
            d = 'DOWN'
        else:
            if k == curses.KEY_UP:
                d = 'UP'
            else:
                if k == curses.KEY_RIGHT:
                    d = 'RIGHT'
                else:
                    if k == curses.KEY_LEFT:
                        d = 'LEFT'
        stdscr.addstr(0, 0, 'Collecting Features. Press q to quit')
        stdscr.addstr(1, 0, 'LAST KEY: ' + d)
        stdscr.refresh()
        k = stdscr.getch()


def get_feature_loop_from_video(stdscr):
    video = cv2.VideoCapture(0)
    df = pd.DataFrame()
    df['img_gray'] = []
    df['time'] = []
    df['shape'] = []
    df['label'] = []
    t1 = time.time()
    a = 0
    k = 0
    d = ''
    while time.time() - t1 < TRAIN_TIME:
        stdscr.clear()
        if k == curses.KEY_DOWN:
            d = 'DOWN'
        else:
            if k == curses.KEY_UP:
                d = 'UP'
            else:
                if k == curses.KEY_RIGHT:
                    d = 'RIGHT'
                else:
                    if k == curses.KEY_LEFT:
                        d = 'LEFT'
                    else:
                        d = 'NONE'
        stdscr.addstr(0, 0, 'Collecting Features. Press q to quit')
        stdscr.addstr(1, 0, 'LAST KEY: ' + d)
        stdscr.refresh()
        k = stdscr.getch()
        a += 1
        check, frame = video.read()
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            try:
                print('Error. Stopping early. {}'.format(e))
                break
            finally:
                e = None
                del e

        gray = cv2.resize(gray, (0, 0), fx=RESIZE_FACTOR, fy=RESIZE_FACTOR)
        cv2.imshow('Capturing', gray)
        time_ = time.time() * 1000.0
        df = df.append({'img_gray':json.dumps([int(x) for x in gray.ravel()]),  'label':str(d), 
         'time':time_, 
         'shape':json.dumps(gray.shape)},
          ignore_index=True)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows
    return df


def get_single_input(stdscr):
    k = stdscr.getch()
    d = ''
    stdscr.clear()
    if k == curses.KEY_DOWN:
        d = 'DOWN'
    else:
        if k == curses.KEY_UP:
            d = 'UP'
        else:
            if k == curses.KEY_RIGHT:
                d = 'RIGHT'
            else:
                if k == curses.KEY_LEFT:
                    d = 'LEFT'
                else:
                    d = 'NONE'
    stdscr.refresh()
    return d


class Collector:

    def gather(self):
        curses.wrapper(get_input)

    def get_key(self):
        df = curses.wrapper(get_feature_loop_from_video)
        return df