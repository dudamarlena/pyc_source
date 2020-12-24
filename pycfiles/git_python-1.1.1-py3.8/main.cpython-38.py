# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-aarch64/egg/main.py
# Compiled at: 2020-01-03 23:06:28
# Size of source mod 2**32: 2627 bytes
import os
from sys import exit
import json, argparse
from git import Repo
try:
    repo = Repo('.')
except InvalidGitRepositoryError:
    print('Invalid or Not a Git Repo')
    exit()
else:
    git = repo.git
    cdir = os.path.dirname(__file__)

    class GPushC:

        def __init__(self):
            with open(cdir + '/config.json', 'r') as (f):
                content = json.load(f)
            self.c = content

        def update_json(self, data):
            with open(cdir + '/config.json', 'w') as (f):
                json.dump(data, f)

        def add_tag(self, tag):
            self.c[tag] = {}
            self.update_json(self.c)

        def add_tag_remote(self, tag, name, remote):
            if tag not in self.c:
                print('Tag Not Added!')
                return None
            self.c[tag][name] = remote
            self.update_json(self.c)

        def push_tag(self, tag):
            for tag in self.c[tag].values():
                git.push(tag)


    gpushc = GPushC()

    def gaddc(message):
        git.add('.')
        git.commit('-m', message)


    def parser_gp():
        parser = argparse.ArgumentParser(description='combination and simplification of some useful git commands')
        subparser = parser.add_subparsers(help='main commands')
        pushc = subparser.add_parser('pushc', help='push as tags')
        pushc_sub = pushc.add_subparsers(help='pushc', dest='pushc')
        pushc_addt = pushc_sub.add_parser('addt', help='add tag of remote repos')
        pushc_addt.add_argument('-t', '--tag', help='tag name', required=True)
        pushc_addr = pushc_sub.add_parser('addr', help='add remote git repo to tag')
        pushc_addr.add_argument('-t', '--tag', help='where the remote to be added', required=True)
        pushc_addr.add_argument('-n', '--name', help='the name for the remote', required=True)
        pushc_addr.add_argument('-r', '--remote', help='the git repo url', required=True)
        pushc_pusht = pushc_sub.add_parser('pusht', help='push the change to each of tag')
        pushc_pusht.add_argument('-t', '--tag', help='push as a tag')
        addc = subparser.add_parser('addc', help='add and commit')
        addc.add_argument('-m', '--message', help='commit message', required=True)
        args = parser.parse_args()
        if 'message' in args:
            gaddc(args.message)
        elif 'pushc' in args:
            if args.pushc == 'addt':
                gpushc.add_tag(args.tag)
            else:
                if args.pushc == 'addr':
                    gpushc.add_tag_remote(args.tag, args.name, args.remote)
                else:
                    if args.pushc == 'pusht':
                        gpushc.push_tag(args.tag)


    if __name__ == '__main__':
        parser_gp()