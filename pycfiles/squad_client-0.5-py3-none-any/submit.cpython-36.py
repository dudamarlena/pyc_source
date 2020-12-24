# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chaws/linaro/src/linaro/squad_client/squad_client/commands/submit.py
# Compiled at: 2020-04-16 07:50:41
# Size of source mod 2**32: 6075 bytes
import json, logging, os, yaml
from squad_client.shortcuts import submit_results
from squad_client.core.command import SquadClientCommand
logger = logging.getLogger()

class SubmitCommand(SquadClientCommand):
    command = 'submit'
    help_text = 'submit results to SQUAD'

    def register(self, subparser):
        parser = super(SubmitCommand, self).register(subparser)
        result_group = parser.add_mutually_exclusive_group()
        result_group.add_argument('--results',
          help='File with test results to submit. Max 5MB. JSON and YAML formats are supported')
        result_group.add_argument('--result-name', help='Single result name')
        parser.add_argument('--result-value',
          help='Single result output (pass/fail/skip)',
          choices=[
         'pass', 'fail', 'skip'])
        parser.add_argument('--metrics',
          help='File with metrics(benchmarsk) to submit. Max 5MB. JSON and YAML formats are supported')
        parser.add_argument('--metadata',
          help='File with metadata to submit. Max 5MB. JSON and YAML formats are supported')
        parser.add_argument('--attachments',
          nargs='+',
          help='Job attachments. Multiple files are allowed',
          default=[])
        parser.add_argument('--logs', help='Test log file path')
        parser.add_argument('--group',
          help='SQUAD group where results are stored', required=True)
        parser.add_argument('--project',
          help='SQUAD project where results are stored', required=True)
        parser.add_argument('--build',
          help='Build version where results are stored', required=True)
        parser.add_argument('--environment',
          help='Build environent where results are stored',
          required=True)

    def __check_file(self, file_path):
        if not os.path.exists(file_path):
            logger.error("Requested file %s doesn't exist" % file_path)
            return False
        else:
            if os.stat(file_path).st_size > 5242881:
                logger.error('%s - file too big' % file_path)
                return False
            return True

    def __read_input_file(self, file_path):
        if not self._SubmitCommand__check_file(file_path):
            return
        else:
            _, ext = os.path.splitext(file_path)
            if ext not in ('.json', '.yml', '.yaml'):
                logger.error('File "%s" is neither JSON nor YAML')
                return
            parser = json.load if ext == '.json' else yaml.safe_load
            parser_exception = json.JSONDecodeError if ext == '.json' else yaml.YAMLError
            output_dict = None
            with open(file_path, 'r') as (results_file):
                try:
                    output_dict = parser(results_file)
                except parser_exception as e:
                    logger.error('Failed parsing file "%s": %s' % (file_path, e))

            return output_dict

    def run(self, args):
        results_dict = {}
        metrics_dict = {}
        metadata_dict = None
        logs_file = None
        if args.result_name:
            if not args.result_value:
                logger.error('Test result value is required')
                return False
            results_dict = {args.result_name: args.result_value}
        if args.results:
            results_dict = self._SubmitCommand__read_input_file(args.results)
            if results_dict is None:
                return False
        if args.metrics:
            metrics_dict = self._SubmitCommand__read_input_file(args.metrics)
            if metrics_dict is None:
                return False
        if args.result_name is None and args.results is None and args.metrics is None:
            logger.error('At least one of --result-name, --results, --metrics is required')
            return False
        else:
            if args.metadata:
                metadata_dict = self._SubmitCommand__read_input_file(args.metadata)
                if metadata_dict is None:
                    return False
                if args.logs:
                    if not self._SubmitCommand__check_file(args.logs):
                        return False
                    with open(args.logs, 'r') as (logs_file_source):
                        logs_file = logs_file_source.read()
                for filename in args.attachments:
                    if not self._SubmitCommand__check_file(filename):
                        return False

                if results_dict:
                    for key, value in iter(results_dict.items()):
                        if type(key) is not str:
                            logger.error('Non-string key detected')
                            return False
                        if type(value) not in [str, dict]:
                            logger.error('Incompatible results detected')
                            return False

            else:
                if metrics_dict:
                    for key, value in iter(metrics_dict.items()):
                        if type(key) is not str:
                            logger.error('Non-string key detected')
                            return False
                        if type(value) not in [float, int, list]:
                            logger.error('Incompatible metrics detected')
                            return False

                if metadata_dict:
                    for key, value in iter(metadata_dict.items()):
                        if type(key) is not str:
                            logger.error('Non-string key detected')
                            return False
                        if type(value) not in [str, dict]:
                            logger.error('Incompatible results detected')
                            return False

            submit_results(group_project_slug=('%s/%s' % (args.group, args.project)),
              build_version=(args.build),
              env_slug=(args.environment),
              tests=results_dict,
              metrics=metrics_dict,
              log=logs_file,
              metadata=metadata_dict)
            return True