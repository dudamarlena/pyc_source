# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/jenkins_job_trigger_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 11063 bytes
import time, socket, json
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.jenkins_hook import JenkinsHook
import jenkins
from jenkins import JenkinsException
from requests import Request
import six
from six.moves.urllib.error import HTTPError, URLError

def jenkins_request_with_headers(jenkins_server, req):
    """
    We need to get the headers in addition to the body answer
    to get the location from them
    This function uses jenkins_request method from python-jenkins library
    with just the return call changed

    :param jenkins_server: The server to query
    :param req: The request to execute
    :return: Dict containing the response body (key body)
        and the headers coming along (headers)
    """
    try:
        response = jenkins_server.jenkins_request(req)
        response_body = response.content
        response_headers = response.headers
        if response_body is None:
            raise jenkins.EmptyResponseException('Error communicating with server[%s]: empty response' % jenkins_server.server)
        return {'body':response_body.decode('utf-8'), 
         'headers':response_headers}
    except HTTPError as e:
        if e.code in (401, 403, 500):
            raise JenkinsException('Error in request. ' + 'Possibly authentication failed [%s]: %s' % (
             e.code, e.msg))
        else:
            if e.code == 404:
                raise jenkins.NotFoundException('Requested item could not be found')
            else:
                raise
    except socket.timeout as e:
        raise jenkins.TimeoutException('Error in request: %s' % e)
    except URLError as e:
        if str(e.reason) == 'timed out':
            raise jenkins.TimeoutException('Error in request: %s' % e.reason)
        raise JenkinsException('Error in request: %s' % e.reason)


class JenkinsJobTriggerOperator(BaseOperator):
    __doc__ = "\n    Trigger a Jenkins Job and monitor it's execution.\n    This operator depend on python-jenkins library,\n    version >= 0.4.15 to communicate with jenkins server.\n    You'll also need to configure a Jenkins connection in the connections screen.\n\n    :param jenkins_connection_id: The jenkins connection to use for this job\n    :type jenkins_connection_id: str\n    :param job_name: The name of the job to trigger\n    :type job_name: str\n    :param parameters: The parameters block to provide to jenkins. (templated)\n    :type parameters: str\n    :param sleep_time: How long will the operator sleep between each status\n        request for the job (min 1, default 10)\n    :type sleep_time: int\n    :param max_try_before_job_appears: The maximum number of requests to make\n        while waiting for the job to appears on jenkins server (default 10)\n    :type max_try_before_job_appears: int\n    "
    template_fields = ('parameters', )
    template_ext = ('.json', )
    ui_color = '#f9ec86'

    @apply_defaults
    def __init__(self, jenkins_connection_id, job_name, parameters='', sleep_time=10, max_try_before_job_appears=10, *args, **kwargs):
        (super(JenkinsJobTriggerOperator, self).__init__)(*args, **kwargs)
        self.job_name = job_name
        self.parameters = parameters
        if sleep_time < 1:
            sleep_time = 1
        self.sleep_time = sleep_time
        self.jenkins_connection_id = jenkins_connection_id
        self.max_try_before_job_appears = max_try_before_job_appears

    def build_job(self, jenkins_server):
        """
        This function makes an API call to Jenkins to trigger a build for 'job_name'
        It returned a dict with 2 keys : body and headers.
        headers contains also a dict-like object which can be queried to get
        the location to poll in the queue.

        :param jenkins_server: The jenkins server where the job should be triggered
        :return: Dict containing the response body (key body)
            and the headers coming along (headers)
        """
        if self.parameters:
            if isinstance(self.parameters, six.string_types):
                import ast
                self.parameters = ast.literal_eval(self.parameters)
        if not self.parameters:
            self.parameters = None
        request = Request(method='POST',
          url=(jenkins_server.build_job_url(self.job_name, self.parameters, None)))
        return jenkins_request_with_headers(jenkins_server, request)

    def poll_job_in_queue(self, location, jenkins_server):
        """
        This method poll the jenkins queue until the job is executed.
        When we trigger a job through an API call,
        the job is first put in the queue without having a build number assigned.
        Thus we have to wait the job exit the queue to know its build number.
        To do so, we have to add /api/json (or /api/xml) to the location
        returned by the build_job call and poll this file.
        When a 'executable' block appears in the json, it means the job execution started
        and the field 'number' then contains the build number.

        :param location: Location to poll, returned in the header of the build_job call
        :param jenkins_server: The jenkins server to poll
        :return: The build_number corresponding to the triggered job
        """
        try_count = 0
        location = location + '/api/json'
        self.log.info('Polling jenkins queue at the url %s', location)
        while try_count < self.max_try_before_job_appears:
            location_answer = jenkins_request_with_headers(jenkins_server, Request(method='POST', url=location))
            if location_answer is not None:
                json_response = json.loads(location_answer['body'])
                if 'executable' in json_response:
                    build_number = json_response['executable']['number']
                    self.log.info('Job executed on Jenkins side with the build number %s', build_number)
                    return build_number
            try_count += 1
            time.sleep(self.sleep_time)

        raise AirflowException("The job hasn't been executed after polling the queue %d times", self.max_try_before_job_appears)

    def get_hook(self):
        return JenkinsHook(self.jenkins_connection_id)

    def execute(self, context):
        if not self.jenkins_connection_id:
            self.log.error('Please specify the jenkins connection id to use.You must create a Jenkins connection before being able to use this operator')
            raise AirflowException('The jenkins_connection_id parameter is missing,impossible to trigger the job')
        else:
            if not self.job_name:
                self.log.error('Please specify the job name to use in the job_name parameter')
                raise AirflowException('The job_name parameter is missing,impossible to trigger the job')
            self.log.info('Triggering the job %s on the jenkins : %s with the parameters : %s', self.job_name, self.jenkins_connection_id, self.parameters)
            jenkins_server = self.get_hook().get_jenkins_server()
            jenkins_response = self.build_job(jenkins_server)
            build_number = self.poll_job_in_queue(jenkins_response['headers']['Location'], jenkins_server)
            time.sleep(self.sleep_time)
            keep_polling_job = True
            build_info = None
            while keep_polling_job:
                try:
                    build_info = jenkins_server.get_build_info(name=(self.job_name), number=build_number)
                    if build_info['result'] is not None:
                        keep_polling_job = False
                        if build_info['result'] != 'SUCCESS':
                            raise AirflowException('Jenkins job failed, final state : %s.Find more information on job url : %s' % (
                             build_info['result'], build_info['url']))
                    else:
                        self.log.info('Waiting for job to complete : %s , build %s', self.job_name, build_number)
                        time.sleep(self.sleep_time)
                except jenkins.NotFoundException as err:
                    raise AirflowException('Jenkins job status check failed. Final error was: %s' % err.resp.status)
                except jenkins.JenkinsException as err:
                    raise AirflowException('Jenkins call failed with error : %s, if you have parameters double check them, jenkins sends back this exception for unknown parametersYou can also check logs for more details on this exception (jenkins_url/log/rss)', str(err))

            if build_info:
                return build_info['url']