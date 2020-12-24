# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/cachet_url_monitor/expectation.py
# Compiled at: 2020-02-10 00:40:07
# Size of source mod 2**32: 4544 bytes
import abc, re
import cachet_url_monitor.status as st
from cachet_url_monitor.exceptions import ConfigurationValidationError
from cachet_url_monitor.status import ComponentStatus

class Expectation(object):
    __doc__ = 'Base class for URL result expectations. Any new expectation should extend\n    this class and the name added to create() method.\n    '

    @staticmethod
    def create(configuration):
        """Creates a list of expectations based on the configuration types
        list.
        """
        expectations = {'HTTP_STATUS':HttpStatus, 
         'LATENCY':Latency, 
         'REGEX':Regex}
        if configuration['type'] not in expectations:
            raise ConfigurationValidationError(f"Invalid type: {configuration['type']}")
        return expectations.get(configuration['type'])(configuration)

    def __init__(self, configuration):
        self.incident_status = self.parse_incident_status(configuration)

    @abc.abstractmethod
    def get_status(self, response) -> ComponentStatus:
        """Returns the status of the API, following cachet's component status
        documentation: https://docs.cachethq.io/docs/component-statuses
        """
        pass

    @abc.abstractmethod
    def get_message(self, response) -> str:
        """Gets the error message."""
        pass

    @abc.abstractmethod
    def get_default_incident(self):
        """Returns the default status when this incident happens."""
        pass

    def parse_incident_status(self, configuration) -> ComponentStatus:
        return st.INCIDENT_MAP.get(configuration.get('incident', None), self.get_default_incident())


class HttpStatus(Expectation):

    def __init__(self, configuration):
        self.status_range = HttpStatus.parse_range(configuration['status_range'])
        super(HttpStatus, self).__init__(configuration)

    @staticmethod
    def parse_range(range_string):
        if isinstance(range_string, int):
            return (range_string, range_string + 1)
        statuses = range_string.split('-')
        if len(statuses) == 1:
            return (int(statuses[0]), int(statuses[0]) + 1)
        return (
         int(statuses[0]), int(statuses[1]))

    def get_status(self, response) -> ComponentStatus:
        if self.status_range[0] <= response.status_code < self.status_range[1]:
            return st.ComponentStatus.OPERATIONAL
        return self.incident_status

    def get_default_incident(self):
        return st.ComponentStatus.PARTIAL_OUTAGE

    def get_message(self, response):
        return f"Unexpected HTTP status ({response.status_code})"

    def __str__(self):
        return repr(f"HTTP status range: [{self.status_range[0]}, {self.status_range[1]}[")


class Latency(Expectation):

    def __init__(self, configuration):
        self.threshold = configuration['threshold']
        super(Latency, self).__init__(configuration)

    def get_status(self, response) -> ComponentStatus:
        if response.elapsed.total_seconds() <= self.threshold:
            return st.ComponentStatus.OPERATIONAL
        return self.incident_status

    def get_default_incident(self):
        return st.ComponentStatus.PERFORMANCE_ISSUES

    def get_message(self, response):
        return 'Latency above threshold: %.4f seconds' % (response.elapsed.total_seconds(),)

    def __str__(self):
        return repr('Latency threshold: %.4f seconds' % (self.threshold,))


class Regex(Expectation):

    def __init__(self, configuration):
        self.regex_string = configuration['regex']
        self.regex = re.compile(configuration['regex'], re.UNICODE + re.DOTALL)
        super(Regex, self).__init__(configuration)

    def get_status(self, response) -> ComponentStatus:
        if self.regex.match(response.text):
            return st.ComponentStatus.OPERATIONAL
        return self.incident_status

    def get_default_incident(self):
        return st.ComponentStatus.PARTIAL_OUTAGE

    def get_message(self, response):
        return 'Regex did not match anything in the body'

    def __str__(self):
        return repr(f"Regex: {self.regex_string}")