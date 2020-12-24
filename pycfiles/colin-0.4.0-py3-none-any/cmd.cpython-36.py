# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/colin/core/checks/cmd.py
# Compiled at: 2018-06-08 08:01:48
# Size of source mod 2**32: 4131 bytes
import re
from conu import ConuException
from ..exceptions import ColinException
from ..result import CheckResult, FailedCheckResult
from .containers import ContainerAbstractCheck
from .images import ImageAbstractCheck

class CmdAbstractCheck(ContainerAbstractCheck, ImageAbstractCheck):

    def __init__(self, message, description, reference_url, tags, cmd, expected_output=None, expected_regex=None, substring=None):
        super(CmdAbstractCheck, self).__init__(message, description, reference_url, tags)
        self.cmd = cmd
        self.expected_output = expected_output
        self.expected_regex = expected_regex
        self.substring = substring

    def check(self, target):
        try:
            output = target.get_output(cmd=(self.cmd))
        except ConuException as ex:
            if str(ex).endswith('exit code 126') or str(ex).endswith('error: 127'):
                return CheckResult(ok=False, description=(self.description),
                  message=(self.message),
                  reference_url=(self.reference_url),
                  check_name=(self.name),
                  logs=[
                 "exec: '{}': executable file not found in $PATH".format(self.cmd)])
            else:
                return FailedCheckResult(check=self, logs=[
                 str(ex)])
        except ColinException as ex:
            return FailedCheckResult(check=self, logs=[
             str(ex)])

        passed = True
        logs = ['Output:\n{}'.format(output)]
        if self.substring is not None:
            substring_present = self.substring in output
            passed = passed and substring_present
            logs.append("{}: Substring '{}' is {}present in the output of the command '{}'.".format('ok' if substring_present else 'nok', self.substring, '' if substring_present else 'not ', self.cmd))
        if self.expected_output is not None:
            expected_output = self.expected_output == output
            if expected_output:
                logs.append("ok: Output of the command '{}' was as expected.".format(self.cmd))
            else:
                logs.append("nok: Output of the command '{}' does not match the expected one: '{}'.".format(self.cmd, self.expected_output))
                passed = False
        if self.expected_regex is not None:
            pattern = re.compile(self.expected_regex)
            if pattern.match(output):
                logs.append("ok: Output of the command '{}' match the regex '{}'.".format(self.cmd, self.expected_regex))
            else:
                logs.append("nok: Output of the command '{}' does not match the expected regex: '{}'.".format(self.cmd, self.expected_regex))
                passed = False
        return CheckResult(ok=passed, description=(self.description),
          message=(self.message),
          reference_url=(self.reference_url),
          check_name=(self.name),
          logs=logs)