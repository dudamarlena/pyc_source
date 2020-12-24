# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hvn/python2/lib/python2.7/site-packages/pho/cli.py
# Compiled at: 2015-04-04 05:41:54
import argparse, pho

def parse_args():
    parser = argparse.ArgumentParser(description=pho.__doc__)
    sparsers = parser.add_subparsers(dest='subparser_name')
    subcmds = ('create', 'delete', 'done', 'undone', 'edit', 'show', 'run', 'status')
    for subcmd in subcmds:
        sub_parser = sparsers.add_parser(subcmd, help=('{0} a task').format(subcmd))
        sub_parser.set_defaults(func=getattr(pho, subcmd))
        sub_parser.add_argument('taskname')

    sub_parser = sparsers.add_parser('list', help='list all tasks')
    sub_parser.add_argument('--all', help='also display done tasks', action='store_true', default=False)
    sub_parser.set_defaults(func=getattr(pho, 'list'))
    sub_parser = sparsers.add_parser('comment', help='add comment to a task')
    sub_parser.add_argument('taskname')
    sub_parser.add_argument('comment', help='comment to add')
    sub_parser.set_defaults(func=getattr(pho, 'comment'))
    args = parser.parse_args()
    if args.subparser_name in subcmds:
        args.func(args.taskname)
    elif args.subparser_name == 'comment':
        args.func(args.taskname, args.comment)
    else:
        args.func(args.all)


if __name__ == '__main__':
    parse_args()