# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pifi/PiFiRemote.py
# Compiled at: 2014-12-14 14:58:45
import os, signal, sys, logging
from time import sleep
from evdev import InputDevice, categorize, ecodes
import mpd
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s', filename='/var/log/pifi-remote.log', filemode='w')

def exitHandler(signal, frame):
    logging.info('Signaling internal jobs to stop...')
    try:
        os.system('mpc stop')
        stopExternalStreaming()
    except:
        logging.error('Unexpected error: %s', sys.exc_info()[0])


def stopExternalStreaming():
    os.system('killall -SIGUSR2 shairport')


def createMPDClient():
    mpc = mpd.MPDClient()
    mpc.timeout = None
    mpc.idletimeout = None
    mpc.connect('localhost', 6600)
    mpc.random(0)
    mpc.consume(0)
    mpc.single(0)
    mpc.repeat(1)
    mpc.crossfade(1)
    return mpc


def monitorRemote():
    dev = InputDevice('/dev/input/event0')
    logging.info('Job monitorRemote started')
    for event in dev.read_loop():
        if event.type != ecodes.EV_KEY or event.value != 1:
            sleep(0.05)
            continue
        try:
            mpc = createMPDClient()
            status = mpc.status()
            logging.debug(('Status: {}').format(status))
            logging.debug(('KeyCode: {}').format(event.code))
            if event.code == ecodes.KEY_LEFT:
                mpc.previous()
            elif event.code == ecodes.KEY_RIGHT:
                mpc.next()
            elif event.code == ecodes.KEY_UP:
                mpc.setvol(int(status['volume']) + 1)
            elif event.code == ecodes.KEY_DOWN:
                mpc.setvol(int(status['volume']) - 1)
            elif event.code == ecodes.KEY_ENTER:
                if status['state'] == 'play':
                    mpc.pause()
                else:
                    stopExternalStreaming()
                    mpc.play()
            elif event.code == ecodes.KEY_ESC:
                stopExternalStreaming()
                mpc.stop()
                os.system('mpc volume -1')
                os.system('mpc volume +1')
            elif event.code == ecodes.KEY_A:
                break
            mpc.close()
            mpc.disconnect()
        except Exception as e:
            logging.error('Caught exception: %s (%s)', e, type(e))

    logging.info('Job monitorRemote stopped')


def main():
    logging.info('starting %s', __file__)
    signal.signal(signal.SIGINT, exitHandler)
    signal.signal(signal.SIGTERM, exitHandler)
    mpc = createMPDClient()
    logging.info('mpd version: ' + mpc.mpd_version)
    logging.info('mpd outputs: ' + str(mpc.outputs()))
    logging.info('mpd stats: ' + str(mpc.stats()))
    mpc.close()
    mpc.disconnect()
    mpc = None
    try:
        monitorRemote()
    except Exception as e:
        logging.error('Critical exception: %s', e)

    logging.info('terminated')
    exit(0)
    return


if __name__ == '__main__':
    main()