# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/satoshi/dev/karakuri/env/lib/python2.7/site-packages/karakuri/run.py
# Compiled at: 2014-08-05 02:43:12
from __future__ import print_function
import sys, argparse
from .project import Project

def main():
    parser = argparse.ArgumentParser(description='Exec project defined given image')
    parser.add_argument('image_name', metavar='image', type=str, help='a name of image')
    sub_parsers = parser.add_subparsers(title='command', metavar='command')
    do_parser = sub_parsers.add_parser('do', help='exec task')
    do_parser.add_argument('task', metavar='task', type=str, nargs='?', default='', help='a task to exec')
    do_parser.add_argument('args', metavar='args', type=str, nargs='*', default='', help='args will be passed to task command')
    do_parser.set_defaults(func=do)
    do_parser = sub_parsers.add_parser('rm', help='remove stopped containers')
    do_parser.set_defaults(func=rm)
    tasks_parser = sub_parsers.add_parser('tasks', help='show tasks')
    tasks_parser.set_defaults(func=tasks)
    args = parser.parse_args()
    args.func(args)


def do(args):
    code = Project(args.image_name).do(args.task, args.args)
    sys.exit(code)


def rm(args):
    Project(args.image_name).rm()


def tasks(args):
    tasks = Project(args.image_name).tasks()
    print(('[task]').ljust(32), '[command]')
    for task, cmd in tasks.items():
        print(task.ljust(32), cmd)