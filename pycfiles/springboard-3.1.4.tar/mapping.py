# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/springboard/springboard/tools/commands/mapping.py
# Compiled at: 2015-11-17 11:55:31
import os
from elasticgit import EG
from elasticgit.utils import load_class, fqcn
from springboard.tools.commands.base import SpringboardToolCommand, CommandArgument

class CreateMappingTool(SpringboardToolCommand):
    command_name = 'create-mapping'
    command_help_text = 'Upload a mapping for models stored in elastic-git'
    command_arguments = SpringboardToolCommand.command_arguments + (
     CommandArgument('repo_name', metavar='repo_name', help='The repository name'),)

    def run(self, config, verbose, clobber, repo_dir, repo_name):
        config_file, config_data = config
        for model_name, mapping in config_data.get('models', {}).items():
            model_class = load_class(model_name)
            self.create_mapping(os.path.join(repo_dir, repo_name), model_class, mapping, verbose=verbose)

    def create_mapping(self, workdir, model_class, mapping, verbose=False):
        self.verbose = verbose
        workspace = EG.workspace(workdir, index_prefix=os.path.basename(workdir))
        self.emit('Creating mapping for %s.' % (fqcn(model_class),))
        workspace.setup_custom_mapping(model_class, mapping)
        self.emit('Mapping created.')