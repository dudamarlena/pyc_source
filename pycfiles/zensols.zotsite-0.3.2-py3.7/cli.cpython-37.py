# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/zotsite/cli.py
# Compiled at: 2020-01-03 18:29:22
# Size of source mod 2**32: 1952 bytes
from zensols.actioncli import OneConfPerActionOptionsCliEnv
from zensols.zotsite import SiteCreator, AppConfig

class SiteCli(object):

    def __init__(self, *args, **kwargs):
        config = (AppConfig.from_args)(*args, **kwargs)
        self.site = SiteCreator(config)

    def print_structure(self):
        self.site.print_structure()

    def export(self):
        self.site.export()


class ConfAppCommandLine(OneConfPerActionOptionsCliEnv):

    def __init__(self):
        coll_op = [
         None, '--collection', False,
         {'dest':'name_pat', 
          'metavar':'DB PATTERN', 
          'help':'regular expression pattern to match collections'}]
        outdir_op = ['-o', '--outputdir', True,
         {'dest':'out_dir', 
          'default':'./zotsite', 
          'metavar':'DIRECTORY', 
          'help':'the directory to output the website'}]
        cnf = {'executors':[
          {'name':'exporter', 
           'executor':lambda params: SiteCli(**params), 
           'actions':[
            {'name':'print', 
             'meth':'print_structure', 
             'opts':[
              coll_op]},
            {'name':'export', 
             'opts':[
              outdir_op, coll_op]}]}], 
         'config_option':{'name':'config', 
          'expect':False, 
          'opt':[
           '-c', '--config', False,
           {'dest':'config', 
            'metavar':'FILE', 
            'help':'configuration file'}]}, 
         'whine':1}
        super(ConfAppCommandLine, self).__init__(cnf,
          config_env_name='zotsiterc', pkg_dist='zensols.zotsite', config_type=AppConfig)


def main():
    cl = ConfAppCommandLine()
    cl.invoke()