# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/addcourse/main.py
# Compiled at: 2015-05-23 12:38:54
"""The main method for this package."""
import argparse, getpass
try:
    import readline
except ImportError:
    pass

from .course_adder import addcourse
from . import __version__

def main():
    """Main function."""
    descr = 'Repeatedly ask QUEST to add you into a particular course.'
    epi = 'Report Bugs to the bug list on our github page at:\n    <https://github.com/kcolford/uwaterloo-addcourse/issues>'
    parser = argparse.ArgumentParser(prog='addcourse', description=descr, epilog=epi, fromfile_prefix_chars='@')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-c', '--course', action='store', help='the course to try getting in to')
    parser.add_argument('-u', '--userid', action='store', help='the userid to login as')
    args = parser.parse_args()
    course = args.course
    if not course:
        course = raw_input('Desired Course: ')
    user = args.userid
    if not user:
        user = raw_input('QUEST ID: ')
    password = getpass.getpass('Password: ')
    addcourse(user, password, course)