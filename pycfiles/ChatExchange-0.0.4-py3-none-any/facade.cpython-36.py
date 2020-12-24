# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\facade.py
# Compiled at: 2019-03-27 03:03:24
# Size of source mod 2**32: 4514 bytes
__doc__ = '\nModule `chatette_qiu.facade`\nContains a facade to the system, allowing to run the parsing, generation and\nwriting of the output file(s).\n'
import os, shutil
from random import seed as random_seed
from chatette_qiu.utils import print_DBG
from chatette_qiu.parsing.parser import Parser
from chatette_qiu.generator import Generator
import chatette_qiu.adapters.factory as adapter_factory

class Facade(object):
    """Facade"""
    instance = None

    def __init__(self, master_file_path, output_dir_path, adapter_str='rasa', local=False, seed=None):
        if local:
            self.output_dir_path = os.path.dirname(master_file_path)
        else:
            self.output_dir_path = os.getcwd()
        if output_dir_path is None:
            self.output_dir_path = os.path.join(self.output_dir_path, 'output')
        else:
            self.output_dir_path = os.path.join(self.output_dir_path, output_dir_path)
        if seed is not None:
            random_seed(seed)
        self.adapter = adapter_factory.create_adapter(adapter_str)
        self.parser = Parser(master_file_path)
        self.generator = None

    @classmethod
    def from_args(cls, args):
        return cls(args.input, args.output, args.adapter, args.local, args.seed)

    @staticmethod
    def get_or_create(master_file_path, output_dir_path, adapter_str=None, local=False, seed=None):
        if Facade.instance is None:
            instance = Facade(master_file_path, output_dir_path, adapter_str, local, seed)
        return instance

    @staticmethod
    def get_or_create_from_args(args):
        if Facade.instance is None:
            instance = Facade.from_args(args)
        return instance

    def run(self):
        """
        Executes the parsing, generation and (if needed) writing of the output.
        """
        self.run_parsing()
        for file in self.parser.all_files[1:]:
            self.parse_file(file)

        self.run_generation()

    def run_parsing(self):
        """Executes the parsing alone."""
        self.parser.parse()

    def parse_file(self, filepath):
        """
        Parses the new template file at `filepath` with the current parser.
        """
        self.parser.open_new_master_file(filepath)
        self.parser.parse()

    def run_generation(self, adapter_str=None):
        """"
        Runs the generation of all intents and writes them out to the output
        file(s) using the adapter `adapter` if one is provided.
        @pre: the parsing has been done.
        """
        if adapter_str is None:
            adapter = self.adapter
        else:
            adapter = adapter_factory.create_adapter(adapter_str)
        self.generator = Generator(self.parser)
        synonyms = self.generator.get_entities_synonyms()
        if os.path.exists(self.output_dir_path):
            shutil.rmtree(self.output_dir_path)
        train_examples = list(self.generator.generate_train())
        if train_examples:
            adapter.write(os.path.join(self.output_dir_path, 'train'), train_examples, synonyms)
        test_examples = list(self.generator.generate_test(train_examples))
        if test_examples:
            adapter.write(os.path.join(self.output_dir_path, 'test'), test_examples, synonyms)
        print_DBG('Generation over')

    def get_stats_as_str(self):
        if self.parser is None:
            return '\tNo file parsed.'
        else:
            stats = self.parser.stats
            result = '\t' + str(stats['#files']) + ' files parsed\n' + '\t' + str(stats['#declarations']) + ' declarations: ' + str(stats['#intents']) + ' intents, ' + str(stats['#slots']) + ' slots and ' + str(stats['#aliases']) + ' aliases\n' + '\t' + str(stats['#rules']) + ' rules'
            return result