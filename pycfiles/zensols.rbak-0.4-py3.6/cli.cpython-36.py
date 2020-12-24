# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/zensols/rbak/cli.py
# Compiled at: 2018-07-22 01:39:48
# Size of source mod 2**32: 2196 bytes
import logging, os
from zensols.actioncli import OneConfPerActionOptionsCli
from zensols.actioncli import Config
from zensols.rbak import Backuper
logger = logging.getLogger('zensols.rbak.cli')
VERSION = '0.2'

class ConfAppCommandLine(OneConfPerActionOptionsCli):

    def __init__(self):
        dry_run_op = [
         '-d', '--dryrun', False,
         {'dest':'dry_run', 
          'action':'store_true', 
          'default':False,  'help':'dry run to not actually connect, but act like it'}]
        sources_op = ['-n', '--sources', False,
         {'dest':'source_names', 
          'help':'override the sources property in the config'}]
        cnf = {'executors':[
          {'name':'backup', 
           'executor':lambda params: Backuper(**params), 
           'actions':[
            {'name':'info', 
             'doc':'print backup configuration information'},
            {'name':'backup', 
             'meth':'sync', 
             'doc':'run the backup', 
             'opts':[
              dry_run_op, sources_op]},
            {'name':'mount', 
             'meth':'mount_all', 
             'doc':'mount all targets', 
             'opts':[
              dry_run_op]},
            {'name':'umount', 
             'meth':'umount_all', 
             'doc':'un-mount all targets', 
             'opts':[
              dry_run_op]}]}], 
         'config_option':{'name':'config', 
          'opt':[
           '-c', '--config', False,
           {'dest':'config', 
            'metavar':'FILE',  'default':'/etc/rbak.conf', 
            'help':'configuration file'}]}, 
         'whine':1}
        super(ConfAppCommandLine, self).__init__(cnf, version=VERSION)


def main():
    cl = ConfAppCommandLine()
    cl.invoke()