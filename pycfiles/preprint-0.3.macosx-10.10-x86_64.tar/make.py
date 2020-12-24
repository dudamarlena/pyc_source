# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jsick/.virtualenvs/paperweight/lib/python2.7/site-packages/preprint/make.py
# Compiled at: 2014-12-02 19:28:35
import logging, subprocess
from cliff.command import Command
from .vc import run_vc

class Make(Command):
    """Do a one-off compilation of the paper"""
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Make, self).get_parser(prog_name)
        parser.add_argument('--cmd', default=self.app.confs.config('cmd'), help='Command to run for compilation')
        return parser

    def take_action(self, parsed_args):
        run_vc()
        cmd = parsed_args.cmd.format(master=self.app.options.master)
        self.log.debug(('Compiling with {0}').format(cmd))
        subprocess.call(cmd, shell=True)