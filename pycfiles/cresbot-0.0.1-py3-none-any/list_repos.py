# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bdx/.virtualenvs/mkdirstest/lib/python2.7/site-packages/crepopy/list_repos.py
# Compiled at: 2014-10-29 21:15:26
import logging, sys, os
from distutils.dir_util import mkpath
from cliff.command import Command
from github3 import login

class ListRepos(Command):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ListRepos, self).get_parser(prog_name)
        parser.add_argument('username', metavar='username', help='username', type=str)
        parser.add_argument('password', metavar='password', help='password', type=str)
        return parser

    def take_action(self, parsed_args):
        """Override take_action to create and write to files"""
        l = login(parsed_args.username, parsed_args.password)
        for repo in l.iter_repos():
            print repo