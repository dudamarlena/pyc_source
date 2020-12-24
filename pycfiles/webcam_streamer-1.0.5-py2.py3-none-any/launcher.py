# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/theo/Documents/Projects/webcam-streamer/webcamstreamer/launcher.py
# Compiled at: 2015-02-20 12:01:37
from __future__ import print_function
import os, subprocess
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

COMMAND = 'cd {directory} && gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker -b {host}:{port} streamer:app'

def main():
    print('-----------------------------------------------\n--------------- webcam-streamer ---------------\n-----------------------------------------------')
    print('webcam-streamer: Checking requirements...')
    try:
        import PIL
    except:
        print('webcam-streamer: PIL must be installed.')
        return False

    try:
        import cv2
    except:
        print('webcam-streamer: OpenCV and its Python bindings must be installed.')
        return False

    print('webcam-streamer: Reading config...')
    config = configparser.ConfigParser()
    defaults_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'streamer/defaults.cfg'))
    try:
        config.read_file(defaults_file)
    except AttributeError:
        config.readfp(defaults_file)

    config.read(os.path.expanduser('~/.webcam-streamer.cfg'))
    print('webcam-streamer: Launching webserver...')
    subprocess.call(COMMAND.format(host=config.get('server', 'host'), port=config.get('server', 'port'), directory=os.path.dirname(os.path.realpath(__file__))), shell=True)
    print('webcam-streamer: Dying... :(')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('webcam-streamer: Killing thyself...')