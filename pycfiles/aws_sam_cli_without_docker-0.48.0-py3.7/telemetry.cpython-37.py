# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/telemetry/telemetry.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 4137 bytes
"""
Class to publish metrics
"""
import platform, uuid, logging, requests
from samcli import __version__ as samcli_version
from samcli.cli.context import Context
from samcli.cli.global_config import GlobalConfig
import samcli.settings as DEFAULT_ENDPOINT_URL
LOG = logging.getLogger(__name__)

class Telemetry:

    def __init__(self, url=None):
        """
        Initialize the Telemetry object.

        Parameters
        ----------
        url : str
            Optional, URL where the metrics should be published to
        """
        self._session_id = self._default_session_id()
        if not self._session_id:
            raise RuntimeError('Unable to retrieve session_id from Click Context')
        self._gc = GlobalConfig()
        self._url = url or DEFAULT_ENDPOINT_URL
        LOG.debug('Telemetry endpoint configured to be %s', self._url)

    def emit(self, metric_name, attrs):
        """
        Emits the metric with given name and the attributes and send it immediately to the HTTP backend. This method
        will return immediately without waiting for response from the backend. Before sending, this method will
        also update ``attrs`` with some common attributes used by all metrics.

        Parameters
        ----------
        metric_name : str
            Name of the metric to publish

        attrs : dict
            Attributes sent along with the metric
        """
        attrs = self._add_common_metric_attributes(attrs)
        self._send({metric_name: attrs})

    def _send(self, metric, wait_for_response=False):
        """
        Serializes the metric data to JSON and sends to the backend.

        Parameters
        ----------

        metric : dict
            Dictionary of metric data to send to backend.

        wait_for_response : bool
            If set to True, this method will wait until the HTTP server returns a response. If not, it will return
            immediately after the request is sent.
        """
        if not self._url:
            LOG.debug('Not sending telemetry. Endpoint URL not configured')
            return
        payload = {'metrics': [metric]}
        LOG.debug('Sending Telemetry: %s', payload)
        timeout_ms = 2000 if wait_for_response else 100
        timeout = (
         2,
         timeout_ms / 1000.0)
        try:
            r = requests.post((self._url), json=payload, timeout=timeout)
            LOG.debug('Telemetry response: %d', r.status_code)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as ex:
            try:
                LOG.debug(str(ex))
            finally:
                ex = None
                del ex

    def _add_common_metric_attributes(self, attrs):
        attrs['requestId'] = str(uuid.uuid4())
        attrs['installationId'] = self._gc.installation_id
        attrs['sessionId'] = self._session_id
        attrs['executionEnvironment'] = self._get_execution_environment()
        attrs['pyversion'] = platform.python_version()
        attrs['samcliVersion'] = samcli_version
        return attrs

    def _default_session_id(self):
        """
        Get the default SessionId from Click Context.
        """
        ctx = Context.get_current_context()
        if ctx:
            return ctx.session_id

    def _get_execution_environment(self):
        """
        Returns the environment in which SAM CLI is running. Possible options are:

        CLI (default) - SAM CLI was executed from terminal or a script.
        IDEToolkit    - SAM CLI was executed by IDE Toolkit
        CodeBuild     - SAM CLI was executed from within CodeBuild

        Returns
        -------
        str
            Name of the environment where SAM CLI is executed in.
        """
        return 'CLI'