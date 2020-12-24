# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/core/result.py
# Compiled at: 2018-09-17 04:16:15
# Size of source mod 2**32: 6413 bytes
import json, six
from .constant import COLOURS, ERROR, FAILED, OUTPUT_CHARS, PASSED
from ..utils.caching_iterable import CachingIterable

class CheckResult(object):

    def __init__(self, ok, description, message, reference_url, check_name, logs):
        self.ok = ok
        self.description = description
        self.message = message
        self.reference_url = reference_url
        self.check_name = check_name
        self.logs = logs

    @property
    def status(self):
        if self.ok:
            return PASSED
        else:
            return FAILED

    def __str__(self):
        return '{}:{}'.format(self.status, self.message)


class DockerfileCheckResult(CheckResult):

    def __init__(self, ok, description, message, reference_url, check_name, lines=None, correction_diff=None):
        super(DockerfileCheckResult, self).__init__(ok, description, message, reference_url, check_name)
        self.lines = lines
        self.correction_diff = correction_diff


class CheckResults(object):

    def __init__(self, results):
        self.results = CachingIterable(results)

    @property
    def results_per_check(self):
        return {r.check_name:r for r in self.results}

    @property
    def _dict_of_results(self):
        """
        Get the dictionary representation of results

        :return: dict (str -> dict (str -> str))
        """
        result_json = {}
        result_list = []
        for r in self.results:
            result_list.append({'name':r.check_name, 
             'ok':r.ok, 
             'status':r.status, 
             'description':r.description, 
             'message':r.message, 
             'reference_url':r.reference_url, 
             'logs':r.logs})

        result_json['checks'] = result_list
        return result_json

    @property
    def json(self):
        """
        Get the json representation of results

        :return: str
        """
        return json.dumps((self._dict_of_results), indent=4)

    def save_json_to_file(self, file):
        json.dump(obj=(self._dict_of_results), fp=file,
          indent=4)

    @property
    def statistics(self):
        """
        Get the dictionary with the count of the check-statuses

        :return: dict(str -> int)
        """
        result = {}
        for r in self.results:
            result.setdefault(r.status, 0)
            result[r.status] += 1

        return result

    @property
    def ok(self):
        """
        If the results ended without any error

        :return: True, if there is no check which ends with error status
        """
        return ERROR not in self.statistics

    @property
    def fail(self):
        """
        If the results ended without any fail

        :return: True, if there is no check which ends with fail status
        """
        return FAILED in self.statistics

    def generate_pretty_output(self, stat, verbose, output_function, logs=True):
        """
        Send the formated to the provided function

        :param stat: if True print stat instead of full output
        :param verbose: bool
        :param output_function: function to send output to
        """
        has_check = False
        for r in self.results:
            has_check = True
            if stat:
                output_function((OUTPUT_CHARS[r.status]), fg=(COLOURS[r.status]),
                  nl=False)
            else:
                output_function((str(r)), fg=(COLOURS[r.status]))
                if verbose:
                    output_function(('  -> {}\n  -> {}'.format(r.description, r.reference_url)),
                      fg=(COLOURS[r.status]))
                    if logs and r.logs:
                        output_function('  -> logs:', fg=(COLOURS[r.status]))
                        for l in r.logs:
                            output_function(('    -> {}'.format(l)), fg=(COLOURS[r.status]))

        if not has_check:
            output_function('No check found.')
        elif stat:
            if not verbose:
                output_function('')
        else:
            output_function('')
            for status, count in six.iteritems(self.statistics):
                output_function(('{}:{} '.format(status, count)), nl=False)

            output_function('')

    def get_pretty_string(self, stat, verbose):
        """
        Pretty string representation of the results

        :param stat: bool
        :param verbose: bool
        :return: str
        """
        pretty_output = _PrettyOutputToStr()
        self.generate_pretty_output(stat=stat, verbose=verbose,
          output_function=(pretty_output.save_output))
        return pretty_output.result


class FailedCheckResult(CheckResult):

    def __init__(self, check, logs=None):
        super(FailedCheckResult, self).__init__(ok=False,
          message=(check.message),
          description=(check.description),
          reference_url=(check.reference_url),
          check_name=(check.name),
          logs=(logs or []))

    @property
    def status(self):
        return ERROR


class _PrettyOutputToStr(object):

    def __init__(self):
        self.result = ''

    def save_output(self, text=None, fg=None, nl=True):
        text = text or ''
        self.result += text
        if nl:
            self.result += '\n'