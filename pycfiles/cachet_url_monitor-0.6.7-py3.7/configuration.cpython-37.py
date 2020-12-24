# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/cachet_url_monitor/configuration.py
# Compiled at: 2020-02-10 01:49:27
# Size of source mod 2**32: 12156 bytes
import copy, logging, time
from typing import Dict
import requests
from yaml import dump
import cachet_url_monitor.status as st
from cachet_url_monitor.client import CachetClient, normalize_url
from cachet_url_monitor.exceptions import ConfigurationValidationError
from cachet_url_monitor.expectation import Expectation
from cachet_url_monitor.status import ComponentStatus
configuration_mandatory_fields = [
 'url', 'method', 'timeout', 'expectation', 'component_id', 'frequency']

class Configuration(object):
    __doc__ = 'Represents a configuration file, but it also includes the functionality\n    of assessing the API and pushing the results to cachet.\n    '
    endpoint_index: int
    endpoint: str
    client: CachetClient
    token: str
    current_fails: int
    trigger_update: bool
    headers: Dict[(str, str)]
    endpoint_method: str
    endpoint_url: str
    endpoint_timeout: int
    endpoint_header: Dict[(str, str)]
    allowed_fails: int
    component_id: int
    metric_id: int
    default_metric_value: int
    latency_unit: str
    status: ComponentStatus
    previous_status: ComponentStatus
    message: str

    def __init__(self, config, endpoint_index: int, client: CachetClient, token: str):
        self.endpoint_index = endpoint_index
        self.data = config
        self.endpoint = self.data['endpoints'][endpoint_index]
        self.client = client
        self.token = token
        self.current_fails = 0
        self.trigger_update = True
        if 'name' not in self.endpoint:
            raise ConfigurationValidationError('name')
        self.logger = logging.getLogger(f"cachet_url_monitor.configuration.Configuration.{self.endpoint['name']}")
        self.print_out()
        self.validate()
        self.headers = {'X-Cachet-Token': self.token}
        self.endpoint_method = self.endpoint['method']
        self.endpoint_url = normalize_url(self.endpoint['url'])
        self.endpoint_timeout = self.endpoint.get('timeout') or 1
        self.endpoint_header = self.endpoint.get('header') or None
        self.allowed_fails = self.endpoint.get('allowed_fails') or 0
        self.component_id = self.endpoint['component_id']
        self.metric_id = self.endpoint.get('metric_id')
        if self.metric_id is not None:
            self.default_metric_value = self.client.get_default_metric_value(self.metric_id)
        self.latency_unit = self.data['cachet'].get('latency_unit') or 's'
        self.status = self.client.get_component_status(self.component_id)
        self.previous_status = self.status
        self.logger.info(f"Component current status: {self.status}")
        self.public_incidents = int(self.endpoint['public_incidents'])
        self.logger.info('Monitoring URL: %s %s' % (self.endpoint_method, self.endpoint_url))
        self.expectations = [Expectation.create(expectation) for expectation in self.endpoint['expectation']]
        for expectation in self.expectations:
            self.logger.info('Registered expectation: %s' % (expectation,))

    def get_action(self):
        """Retrieves the action list from the configuration. If it's empty, returns an empty list.
        :return: The list of actions, which can be an empty list.
        """
        if self.endpoint.get('action') is None:
            return []
        return self.endpoint['action']

    def validate(self):
        """Validates the configuration by verifying the mandatory fields are
        present and in the correct format. If the validation fails, a
        ConfigurationValidationError is raised. Otherwise nothing will happen.
        """
        configuration_errors = []
        for key in configuration_mandatory_fields:
            if key not in self.endpoint:
                configuration_errors.append(key)

        if 'expectation' in self.endpoint:
            if isinstance(self.endpoint['expectation'], list):
                if not isinstance(self.endpoint['expectation'], list) or len(self.endpoint['expectation']) == 0:
                    configuration_errors.append('endpoint.expectation')
        if len(configuration_errors) > 0:
            raise ConfigurationValidationError('Endpoint [%s] failed validation. Missing keys: %s' % (self.endpoint,
             ', '.join(configuration_errors)))

    def evaluate(self):
        """Sends the request to the URL set in the configuration and executes
        each one of the expectations, one by one. The status will be updated
        according to the expectation results.
        """
        try:
            if self.endpoint_header is not None:
                self.request = requests.request((self.endpoint_method), (self.endpoint_url), timeout=(self.endpoint_timeout), headers=(self.endpoint_header))
            else:
                self.request = requests.request((self.endpoint_method), (self.endpoint_url), timeout=(self.endpoint_timeout))
            self.current_timestamp = int(time.time())
        except requests.ConnectionError:
            self.message = 'The URL is unreachable: %s %s' % (self.endpoint_method, self.endpoint_url)
            self.logger.warning(self.message)
            self.status = st.ComponentStatus.PARTIAL_OUTAGE
            return
        except requests.HTTPError:
            self.message = 'Unexpected HTTP response'
            self.logger.exception(self.message)
            self.status = st.ComponentStatus.PARTIAL_OUTAGE
            return
        except (requests.Timeout, requests.ConnectTimeout):
            self.message = 'Request timed out'
            self.logger.warning(self.message)
            self.status = st.ComponentStatus.PERFORMANCE_ISSUES
            return
        else:
            self.status = st.ComponentStatus.OPERATIONAL
            self.message = ''
            for expectation in self.expectations:
                status = expectation.get_status(self.request)
                if status.value > self.status.value:
                    self.status = status
                    self.message = expectation.get_message(self.request)
                    self.logger.info(self.message)

    def print_out(self):
        self.logger.info(f"Current configuration:\n{self.__repr__()}")

    def __repr__(self):
        temporary_data = copy.deepcopy(self.data)
        del temporary_data['cachet']['token']
        temporary_data['endpoints'] = temporary_data['endpoints'][self.endpoint_index]
        return dump(temporary_data, default_flow_style=False)

    def if_trigger_update(self):
        """
        Checks if update should be triggered - trigger it for all operational states
        and only for non-operational ones above the configured threshold (allowed_fails).
        """
        if self.status != st.ComponentStatus.OPERATIONAL:
            self.current_fails = self.current_fails + 1
            self.logger.warning(f"Failure #{self.current_fails} with threshold set to {self.allowed_fails}")
            if self.current_fails <= self.allowed_fails:
                self.trigger_update = False
                return
        self.current_fails = 0
        self.trigger_update = True

    def push_status(self):
        """Pushes the status of the component to the cachet server. It will update the component
        status based on the previous call to evaluate().
        """
        if self.previous_status == self.status:
            self.logger.info('No changes to component status.')
            self.trigger_update = False
            return
        else:
            self.previous_status = self.status
            if not self.trigger_update:
                return
                api_component_status = self.client.get_component_status(self.component_id)
                if self.status == api_component_status:
                    return
                component_request = self.client.push_status(self.component_id, self.status)
                if component_request.ok:
                    self.logger.info(f"Component update: status [{self.status}]")
            else:
                self.logger.warning(f"Component update failed with HTTP status: {component_request.status_code}. API status: {self.status}")

    def push_metrics(self):
        """Pushes the total amount of seconds the request took to get a response from the URL.
        It only will send a request if the metric id was set in the configuration.
        In case of failed connection trial pushes the default metric value.
        """
        if 'metric_id' in self.data['cachet']:
            if hasattr(self, 'request'):
                metrics_request = self.client.push_metrics(self.metric_id, self.latency_unit, self.request.elapsed.total_seconds(), self.current_timestamp)
                if metrics_request.ok:
                    self.logger.info('Metric uploaded: %.6f %s' % (self.request.elapsed.total_seconds(), self.latency_unit))
                else:
                    self.logger.warning(f"Metric upload failed with status [{metrics_request.status_code}]")

    def push_incident(self):
        """If the component status has changed, we create a new incident (if this is the first time it becomes unstable)
        or updates the existing incident once it becomes healthy again.
        """
        if not self.trigger_update:
            return
        if hasattr(self, 'incident_id'):
            if self.status == st.ComponentStatus.OPERATIONAL:
                incident_request = self.client.push_incident((self.status), (self.public_incidents), (self.component_id), previous_incident_id=(self.incident_id))
                if incident_request.ok:
                    self.logger.info(f'Incident updated, API healthy again: component status [{self.status}], message: "{self.message}"')
                    del self.incident_id
            else:
                self.logger.warning(f'Incident update failed with status [{incident_request.status_code}], message: "{self.message}"')
        else:
            if not hasattr(self, 'incident_id'):
                if self.status != st.ComponentStatus.OPERATIONAL:
                    incident_request = self.client.push_incident((self.status), (self.public_incidents), (self.component_id), message=(self.message))
                    if incident_request.ok:
                        self.incident_id = incident_request.json()['data']['id']
                        self.logger.info(f'Incident uploaded, API unhealthy: component status [{self.status}], message: "{self.message}"')
                    else:
                        self.logger.warning(f'Incident upload failed with status [{incident_request.status_code}], message: "{self.message}"')