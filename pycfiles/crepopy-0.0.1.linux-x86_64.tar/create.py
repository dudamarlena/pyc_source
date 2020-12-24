# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bdx/.virtualenvs/mkdirstest/lib/python2.7/site-packages/crepopy/create.py
# Compiled at: 2014-10-29 21:15:26
import logging, sys, os
from distutils.dir_util import mkpath
from cliff.command import Command
from github3 import login

class Create(Command):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Create, self).get_parser(prog_name)
        parser.add_argument('username', metavar='username', help='username', type=str)
        parser.add_argument('password', metavar='password', help='password', type=str)
        parser.add_argument('reponame', metavar='reponame', help='reponame', type=str)
        parser.add_argument('discription', metavar='discription', help='discription', type=str)
        return parser

    def take_action(self, parsed_args):
        """Override take_action to create and write to files"""
        l = login(parsed_args.username, parsed_args.password)
        l.create_repo(name=parsed_args.reponame, description=parsed_args.discription, homepage=False, has_issues=False, has_wiki=False, has_downloads=False)