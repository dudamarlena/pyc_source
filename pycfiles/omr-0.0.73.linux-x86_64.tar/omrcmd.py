# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/omr/omrcmd.py
# Compiled at: 2014-05-04 13:52:16
"""
Run app with command line arguments.
Run GUI if no arguments are provided.
"""
import argparse, multiprocessing, sys, Tkinter, omr

def parse_args():
    """parse command line arguments."""
    parser = argparse.ArgumentParser(description='Extract answer choices from scanned jpg bubble forms.')
    parser.add_argument('frontdir', help='Image directory.')
    parser.add_argument('-b', '--backdir', default=None, help='Optional back side image directory')
    parser.add_argument('-f', '--form', default='882E', choices=omr.FORMS.keys(), help='Form string')
    return parser.parse_args()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        multiprocessing.log_to_stderr()
        args = parse_args()
        args.pool = multiprocessing.Pool()
        omr.main(**vars(args))
        args.pool.close()
        args.pool.join()
        print 'completed'
    else:
        root = Tkinter.Tk()
        app = omr.Gui(root)
        root.update_idletasks()
        root.mainloop()