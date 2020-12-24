# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/springboard/springboard/tools/commands/bootstrap.py
# Compiled at: 2015-11-17 11:55:31
from elasticgit.utils import load_class
from springboard.tools.commands.clone import CloneRepoTool
from springboard.tools.commands.index import CreateIndexTool
from springboard.tools.commands.mapping import CreateMappingTool
from springboard.tools.commands.sync import SyncDataTool
from springboard.tools.commands.base import SpringboardToolCommand

class BootstrapTool(CloneRepoTool, CreateIndexTool, CreateMappingTool, SyncDataTool):
    command_name = 'bootstrap'
    command_help_text = 'Tools for bootstrapping new content repositories locally.'
    command_arguments = SpringboardToolCommand.command_arguments

    def run(self, config, verbose, clobber, repo_dir):
        config_file, config_data = config
        repos = [ self.clone_repo(repo_name=repo_name, repo_url=repo_url, repo_dir=repo_dir, clobber=clobber, verbose=verbose) for repo_name, repo_url in config_data['repositories'].items()
                ]
        for workdir, _ in repos:
            self.bootstrap(workdir, models=config_data.get('models', {}).items(), clobber=clobber, verbose=verbose)

    def bootstrap(self, workdir, models=(), clobber=False, verbose=False):
        index_created = self.create_index(workdir, clobber=clobber, verbose=verbose)
        for model_name, mapping in models:
            model_class = load_class(model_name)
            if index_created:
                self.create_mapping(workdir, model_class, mapping, verbose=verbose)
            self.sync_data(workdir, model_class, verbose=verbose, clobber=clobber)