# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bdx/.virtualenvs/pypoker/lib/python2.7/site-packages/evaluator/evaluator.py
# Compiled at: 2014-10-07 14:28:10
import logging, sys, os
from distutils.dir_util import mkpath
from cliff.command import Command
from hand import Hand

class Evaluate(Command):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Evaluate, self).get_parser(prog_name)
        parser.add_argument('-e', '--eval', metavar='eval', help='evaluate hand', nargs='+')
        return parser

    def take_action(self, parsed_args):
        """Override take_action to create and write to files"""
        a = []
        for i in parsed_args.eval:
            a.append(i)

        h = Hand(a)
        for i in h.cards:
            print i

        print h.get_rank()