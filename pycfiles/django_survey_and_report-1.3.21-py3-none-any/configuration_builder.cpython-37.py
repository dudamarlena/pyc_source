# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/exporter/tex/configuration_builder.py
# Compiled at: 2019-03-02 04:44:34
# Size of source mod 2**32: 1787 bytes
from survey.models import Survey
from .configuration import Configuration

class ConfigurationBuilder(Configuration):
    __doc__ = '\n        Permit to create serializable uninitialized configuration easily.\n        We just use the default dict for a Builder, the user will be able to\n        modify value from the default.\n\n        We delete unwanted survey in self._conf in order to print\n        only what the user want.\n    '

    def __init__(self, survey=None):
        """ Initialize a configuration file.

        :param Survey survey: If survey is defined we generate configuration
        only for this survey."""
        super(ConfigurationBuilder, self).__init__(self.DEFAULT_PATH)
        self._init_default()
        if survey:
            for other_survey in Survey.objects.all():
                unwanted_survey = survey.name != other_survey.name
                if unwanted_survey:
                    del self._conf[other_survey.name]

    def _init_default(self):
        """ Return the default configuration. """
        default_value_generic = self._conf['generic']
        default_value_chart = self._conf['generic']['chart']
        default_values = {'chart': default_value_chart}
        for survey in Survey.objects.all():
            if self._conf.get(survey.name) is None:
                self._conf[survey.name] = default_value_generic
            categories = {}
            for category in survey.categories.all():
                categories[category.name] = default_values

            self._conf[survey.name]['categories'] = categories
            questions = {}
            for question in survey.questions.all():
                questions[question.text] = default_values

            self._conf[survey.name]['questions'] = questions