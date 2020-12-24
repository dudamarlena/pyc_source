# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\serial_tool\serial.py
# Compiled at: 2020-04-01 08:10:36
# Size of source mod 2**32: 960 bytes
import serial, datetime, argparse
file = 'serial.log'

def open_serial(port, bps, is_log=False):
    s = serial.Serial(port, bps)
    while s.is_open:
        line = s.readline().decode()
        t = datetime.datetime.now().ctime()
        line = f"{t} : {line}"
        print(line)
        if is_log:
            with open(file, 'a') as (f):
                f.writelines(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', help='serial port. like COM1 or /dev/serial ')
    parser.add_argument('-b', dest='bps', type=int, default=9600,
      help='serial boundrates')
    parser.add_argument('-l', dest='log', action='store_true', help='is logging')
    args = parser.parse_args()
    open_serial(args.port, args.bps, args.log)


if __name__ == '__main__':
    main()