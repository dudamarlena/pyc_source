# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/av_streamer/test.py
# Compiled at: 2018-04-07 03:14:34
from threading import Thread
from time import sleep
from av_streamer import start_stream

def frame(image):
    print len(image)


def connect_camera():
    start_stream('rtsp://192.168.10.210/Streaming/Channels/1', '/home/smartup/z_test_ffmpeg/test.mp4', frame)
    print 'reconnect at 5 second'
    sleep(5)
    print 'reconnect'
    Thread(target=connect_camera).start()


Thread(target=connect_camera).start()