# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/management/commands/generatetexconf.py
# Compiled at: 2020-01-26 10:29:21
# Size of source mod 2**32: 1147 bytes
import sys
from survey.exporter.tex import ConfigurationBuilder
from survey.management.survey_command import SurveyCommand

class Command(SurveyCommand):
    __doc__ = '\n        See the "help" var.\n    '
    help = 'This command permit to generate the latex configuration in order\n    to manage the survey report generation. '

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('output', nargs='+', type=str, help='Output prefix.')

    def write_conf(self, name, conf):
        file_ = open(name, 'w', encoding='UTF-8')
        file_.write(str(conf))
        file_.close()

    def handle(self, *args, **options):
        (super(Command, self).handle)(*args, **options)
        output = options['output']
        if len(output) != len(self.surveys):
            exit_msg = 'You want to generate {} surveys but you only gave {} output names.'
            sys.exit(exit_msg.format(len(self.surveys), len(output)))
        for i, survey in enumerate(self.surveys):
            conf = ConfigurationBuilder(survey)
            self.write_conf(output[i], conf)