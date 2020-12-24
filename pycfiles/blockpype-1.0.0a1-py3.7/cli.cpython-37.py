# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blockpype/cli.py
# Compiled at: 2019-07-01 10:56:21
# Size of source mod 2**32: 3513 bytes
import argparse, select, subprocess, sys

def setup_args():
    """Sets up command line parameters
    """
    parser = argparse.ArgumentParser(description='Breaks apart input stream into blocks and pipes each block into newly spawned processes.')
    command_group = parser.add_mutually_exclusive_group(required=True)
    command_group.add_argument('-l',
      '--lines',
      help='Break apart after each LINES',
      type=int,
      default=None)
    command_group.add_argument('-b',
      '--bytes',
      help='Break apart after each BYTES',
      type=int,
      default=None)
    command_group.add_argument('-c',
      '--chars',
      help='Break apart after each CHARS',
      type=int,
      default=None)
    parser.add_argument('pipe_args', type=str, nargs='+', help='Process to start and pipe to')
    return parser.parse_args()


def endproc(proc: subprocess.Popen):
    """Properly ends a process and handles any errors
    """
    proc.communicate()
    code = proc.poll()
    if code is None:
        code = proc.wait()
    if code != 0:
        exit(code)


def main():
    """Entry point for CLI
    """
    args = setup_args()
    encoding = sys.stdin.encoding
    stream = None
    if args.chars:
        stream = sys.stdin
    else:
        stream = sys.stdin.buffer
    if select.select([sys.stdin], [], [], 0.0)[0]:
        proc = None
        if args.lines:
            lines = 0
            for line in stream:
                if lines == 0:
                    proc = subprocess.Popen((args.pipe_args), stdin=(subprocess.PIPE))
                proc.stdin.write(line)
                lines += 1
                if lines == args.lines:
                    lines = 0
                    if proc:
                        endproc(proc)
                        proc = None

            if proc:
                endproc(proc)
        elif not args.chars:
            if args.bytes:
                block_size = args.chars or args.bytes
                have_read = 0
                buff_size = 10000
                while True:
                    if have_read == 0:
                        proc = subprocess.Popen((args.pipe_args), stdin=(subprocess.PIPE))
                    else:
                        if select.select([sys.stdin], [], [], 0.0)[0]:
                            buff = stream.read(min([buff_size, block_size - have_read]))
                        else:
                            buff = ''
                        len_buff = len(buff)
                        if len_buff == 0:
                            break
                        if args.chars:
                            proc.stdin.write(buff.encode(encoding))
                        else:
                            proc.stdin.write(buff)
                    have_read += len_buff
                    if block_size == have_read:
                        have_read = 0
                        if proc:
                            endproc(proc)
                            proc = None


if __name__ == '__main__':
    main()