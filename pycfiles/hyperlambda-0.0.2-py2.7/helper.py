# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hyperlambda/helper.py
# Compiled at: 2018-02-21 02:19:03
from __future__ import division, print_function, unicode_literals
from functools import partial
from tempfile import NamedTemporaryFile
import logging
from . import settings
import requests, json, boto3, base64, requests, threading
from . import exceptions
import time, datetime, traceback
from collections import OrderedDict
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class warp_lambda(object):
    """
    A Hyperlambda is a web service that allows a client to securely supply an algorithm, 
    which the server will evaluate on its side, and (optionally) return the results of its evaluation back to the client. 
    This completely reverses the responsibility between the “client” and the “server”, and allows for a whole range of really interesting scenarios, 
    arguably facilitating for that your machines can engage in a “meaningful semantic discussion”, 
    communicating intent back and forth, the same way two human beings can.
    """

    def __init__(self, description=b'hyperlambda Function', version=1.0, verbose=1, function_name=None, region=settings.region, zip_file=None, code=None, role=None, handler=None, runtime=b'python2.7', timeout=180, data={}, environment=None, userdata=b'', tags=None, security_group_ids=settings.security_group_ids, key_name=settings.key_name, callback_url=None, aws_access_key_id=settings.aws_access_key_id, aws_secret_access_key=settings.aws_secret_access_key, instance_type=settings.instance_type, image_id=settings.image_id, spot_price=settings.spot_price):
        self.description = description
        self.function_name = function_name
        self.region = region
        self.zip_file = zip_file
        self.code = code
        self.role = role
        self.handler = handler
        self.runtime = runtime
        self.timeout = timeout
        self.data = data
        self.environment = environment
        self.userdata = userdata
        self.tags = tags
        self.security_group_ids = security_group_ids
        self.key_name = key_name
        self.callback_url = callback_url
        self.spot_price = spot_price
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.instance_type = instance_type
        self.image_id = image_id
        self.created_time = datetime.datetime.now()
        self.started_time = None
        self.finishedtime = None
        self.message = b'reequest accepted'
        self.state = b'initial'
        self.response = None
        self.timeout_terminate = False
        self.client = boto3.client(b'ec2', region_name=self.region, aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
        self.ec2 = boto3.resource(b'ec2', self.region, aws_access_key_id=self.aws_access_key_id, aws_secret_access_key=self.aws_secret_access_key)
        logging.info(b'HyperLambda Initializing... ')
        return

    def create_bash(self):
        user_data = b'#!/bin/bash\n'
        if self.environment != None:
            for key, itm in self.environment[b'Variables'].iteritems():
                user_data += b'echo ' + key + b'=' + b'"' + str(itm) + b'"' + b' >> ' + b' /etc/environment \n'

        return user_data

    def create_instance(self):
        logging.info(b'bidding for instance ')
        self.message = b'Instance Creating'
        self.state = b'pending'
        instance_arg = dict(InstanceCount=1, LaunchSpecification=dict(BlockDeviceMappings=[
         dict(DeviceName=b'/dev/sda1', Ebs=dict(VolumeSize=settings.volume_size, VolumeType=b'gp2'))], ImageId=settings.image_id, InstanceType=self.instance_type, SecurityGroupIds=self.security_group_ids, UserData=base64.b64encode(self.create_bash() + settings.user_data.format(self.runtime, self.runtime) + b'\n' + self.userdata)), Type=b'one-time', SpotPrice=self.spot_price)
        if self.key_name:
            instance_arg[b'LaunchSpecification'][b'KeyName'] = settings.key_name
        logging.debug(instance_arg)
        response = self.client.request_spot_instances(**instance_arg)
        logging.info(response[b'SpotInstanceRequests'][0][b'Status'][b'Message'])
        spot_instance_id = None
        spot_instance_req_id = response[b'SpotInstanceRequests'][0][b'SpotInstanceRequestId']
        if response[b'SpotInstanceRequests'][0][b'State'] == b'active':
            spot_instance_id = response[b'SpotInstanceRequests'][0][b'InstanceId']
        elif response[b'SpotInstanceRequests'][0][b'State'] == b'open':
            if response[b'SpotInstanceRequests'][0][b'Status'][b'Code'] == b'pending-evaluation' or response[b'SpotInstanceRequests'][0][b'Status'][b'Code'] == b'pending-fulfillment':
                try:
                    logging.info(b'Waiting for the spot instance request to be fullfilled')
                    waiter = self.client.get_waiter(b'spot_instance_request_fulfilled')
                    waiter.wait(SpotInstanceRequestIds=[spot_instance_req_id])
                except Exception as e:
                    logging.debug(e.message)

                instance_req = self.client.describe_spot_instance_requests(SpotInstanceRequestIds=[response[b'SpotInstanceRequests'][0][b'SpotInstanceRequestId']])
                if instance_req[b'SpotInstanceRequests'][0][b'State'] == b'active':
                    spot_instance_id = instance_req[b'SpotInstanceRequests'][0][b'InstanceId']
                    logging.info(instance_req[b'SpotInstanceRequests'][0][b'Status'][b'Message'])
        if spot_instance_id:
            reservations = self.client.describe_instances(InstanceIds=[spot_instance_id])
            if reservations:
                ip_address = reservations[b'Reservations'][0][b'Instances'][0][b'PublicIpAddress']
                logging.info(b'PublicIpAddress: ' + ip_address)
                instance_obj = self.ec2.Instance(reservations[b'Reservations'][0][b'Instances'][0][b'InstanceId'])
                instance_obj.create_tags(Tags=[{b'Key': b'Name', b'Value': self.function_name}])
                self.instance = {b'ip_address': ip_address, b'instance_req_id': spot_instance_req_id, b'instance_id': spot_instance_id}
                logging.info((b'Waits until this instance {} is exists').format(spot_instance_id))
                instance_obj.wait_until_exists()
                logging.info((b'Waits until this instance {} is running').format(spot_instance_id))
                instance_obj.wait_until_running()
                logging.info(b'Instance Started Running')
                logging.debug(self.instance)
                self.thread_terminate_timeout_instance = threading.Timer(self.timeout + 60, self.terminate_instance, [True])
                self.thread_terminate_timeout_instance.start()
                self.message = b'Your Instance is created'
                self.state = b'queued'
                return True
        else:
            logging.debug((b'Cancelling Spot Instance Request with error message: {}').format(instance_req[b'SpotInstanceRequests'][0][b'Status'][b'Message']))
            instance_req = self.client.describe_spot_instance_requests(SpotInstanceRequestIds=[response[b'SpotInstanceRequests'][0][b'SpotInstanceRequestId']])
            logging.info(instance_req[b'SpotInstanceRequests'][0][b'Status'][b'Message'])
            self.client.cancel_spot_instance_requests(SpotInstanceRequestIds=[spot_instance_req_id])
            self.message = instance_req[b'SpotInstanceRequests'][0][b'Status'][b'Message']
            self.State = b'cancelled'
            self.finishedtime = datetime.datetime.now()
        return False

    def execute_lambda(self):
        try:
            data = {b'url': self.zip_file, b'handler': self.handler, b'payload': self.data, b'callback_url': self.callback_url}
            logging.debug(data)
            logging.debug(b'sending script for processing...')
            self.started_time = datetime.datetime.now()
            try:
                post_req = requests.post(b'http://' + self.instance[b'ip_address'] + b'/lambda_processing/', data=json.dumps(data))
            except Exception as e:
                logging.info(e.message)
                self.message = b'Sending Request failed, will try again.'
                self.state = b'delayed'
                time.sleep(30)
                post_req = requests.post(b'http://' + self.instance[b'ip_address'] + b'/lambda_processing/', data=json.dumps(data))

            response = post_req.json()
            if post_req.status_code == 202:
                self.message = response[b'message']
                self.state = response[b'status']
                self.response = response.get(b'response', None)
                logging.info(b'Request Accepted for processing')
                exec_status = self.check_instance()
                return exec_status
            logging.info(b'client server rejected requests')
            self.message = response[b'message']
            self.state = b'cancelled'
            self.terminate_instance(timeout=False)
            self.finishedtime = datetime.datetime.now()
            duration = self.finishedtime - self.started_time
            logging.error((b'HyperLambda script Execution Failed with time duration of {} seconds with error message: {}').format(duration.total_seconds(), self.message))
            return 1
        except exceptions.FunctionTimeoutError as e:
            self.finishedtime = datetime.datetime.now()
            raise exceptions.FunctionTimeoutError(timeout=self.timeout)
        except exceptions.InstanceTerminatedError as e:
            self.finishedtime = datetime.datetime.now()
            raise exceptions.InstanceTerminatedError(message=e.message)
        except Exception as e:
            logging.info((b'Something went wrong with error message: {}').format(e.message))
            self.message = e.message
            self.state = b'cancelled'
            self.terminate_instance(timeout=False)
            self.finishedtime = datetime.datetime.now()
            duration = self.finishedtime - self.started_time
            logging.error((b'HyperLambda script Execution Failed with time duration of {} seconds with error message: {}').format(duration.total_seconds(), self.message))
            return 1

        return

    def check_instance(self):
        try:
            response = self.client.describe_instance_status(InstanceIds=[self.instance[b'instance_id']], IncludeAllInstances=True)
            if response[b'InstanceStatuses'][0][b'InstanceState'][b'Name'] != b'running':
                if self.timeout_terminate == True:
                    self.message = (b'{} Task timed out after {} seconds').format(self.function_name, self.timeout)
                    self.state = b'timeout'
                    raise exceptions.FunctionTimeoutError(timeout=self.timeout)
                elif self.instance[b'spot_instance_req_id']:
                    response = self.client.describe_spot_instance_requests(SpotInstanceRequestIds=[
                     self.instance[b'spot_instance_req_id']])
                    self.terminate_instance()
                    self.message = response[b'SpotInstanceRequests'][0][b'Status'][b'Code'][b'Message']
                    self.state = b'failed'
                    raise exceptions.InstanceTerminatedError(message=response[b'SpotInstanceRequests'][0][b'Status'][b'Code'][b'Message'])
                else:
                    instance_response = self.client.describe_instances(InstanceIds=[self.instance[b'instance_id']])
                    self.terminate_instance()
                    self.message = instance_response[b'Reservations'][0][b'Instances'][0][b'StateReason']
                    self.state = b'failed'
                    raise exceptions.InstanceTerminatedError(message=instance_response[b'Reservations'][0][b'Instances'][0][b'StateReason'])
            else:
                try:
                    get_req = requests.get(b'http://' + self.instance[b'ip_address'] + b'/lambda_status/')
                    if get_req.status_code == 200:
                        result = get_req.json()
                        self.message = result[b'message']
                        self.state = result[b'status']
                        self.response = result.get(b'response', None)
                except Exception as e:
                    logging.debug(e.message)

                if self.state == b'success':
                    self.terminate_instance()
                    self.finishedtime = datetime.datetime.now()
                    duration = self.finishedtime - self.started_time
                    logging.info((b'HyperLambda script Execution completed successfully with time duration of {} seconds with response: {}').format(duration.total_seconds(), self.response))
                    return 0
                if self.state == b'failed':
                    self.terminate_instance()
                    self.finishedtime = datetime.datetime.now()
                    duration = self.finishedtime - self.started_time
                    logging.error((b'HyperLambda script Execution Failed with time duration of {} seconds with error message: {}').format(duration.total_seconds()), self.message)
                    self.finishedtime = datetime.datetime.now()
                    return 1
                time.sleep(20)
                self.check_instance()
        except exceptions.FunctionTimeoutError as e:
            self.finishedtime = datetime.datetime.now()
            raise exceptions.FunctionTimeoutError(timeout=self.timeout)
        except exceptions.InstanceTerminatedError as e:
            self.finishedtime = datetime.datetime.now()
            raise exceptions.InstanceTerminatedError(message=e.message)
        except Exception as e:
            logging.debug(e.message)
            self.finishedtime = datetime.datetime.now()
            duration = self.finishedtime - self.started_time
            logging.info((b'Failed with time duration of {} seconds with error message: {}').format(duration.total_seconds(), e.message))
            return 1

        return

    def terminate_instance(self, timeout=False):
        try:
            if self.instance[b'instance_req_id']:
                self.client.cancel_spot_instance_requests(SpotInstanceRequestIds=[self.instance[b'instance_req_id']])
            self.client.terminate_instances(InstanceIds=[self.instance[b'instance_id']])
            self.timeout_terminate = timeout
            if timeout:
                logging.info((b'Timeout of {} seconds reached. Closed the instance').format(self.timeout))
                self.check_instance()
            else:
                logging.info(b'Instance Closed Successfully')
        except Exception as e:
            logging.debug(e.message)

    def lambda_status(self):
        try:
            instance_response = self.client.describe_instances(InstanceIds=[self.instance[b'instance_id']])
            instance_details = instance_response[b'Reservations'][0][b'Instances'][0]
            response = dict(HyperLambda=[
             dict(Status=dict(Message=self.message, State=self.state, RequestedTime=datetime.datetime.now(), Response=self.response), Configuration=dict(FunctionName=self.function_name, Runtime=self.runtime, Role=self.role, ZipFile=self.zip_file, Handler=self.handler, Data=self.data, TimeOut=self.timeout, Environment=self.environment, SecurityGroupIds=self.security_group_ids, KeyName=self.key_name, CallbackURL=self.callback_url, InstanceType=self.instance_type, CreatedTime=self.created_time, StartedTime=self.started_time, FinishedTime=self.finishedtime), Instance=dict(InstanceType=instance_details[b'InstanceType'], ImageId=instance_details[b'ImageId'], KeyName=instance_details[b'KeyName'], SecurityGroups=instance_details[b'SecurityGroups'], SpotPrice=self.spot_price, PublicIpAddress=instance_details[b'PublicIpAddress'], LaunchTime=instance_details[b'LaunchTime'], SpotInstanceRequestId=instance_details[b'SpotInstanceRequestId'], InstanceId=instance_details[b'InstanceId'], Status=instance_details[b'State'][b'Name']))])
            return response
        except Exception as e:
            logging.debug(e.message)
            response = dict(HyperLambda=[
             dict(Status=dict(Message=self.message, State=self.state, RequestedTime=datetime.datetime.now(), Response=self.response), Configuration=dict(FunctionName=self.function_name, Runtime=self.runtime, Role=self.role, ZipFile=self.zip_file, Handler=self.handler, Data=self.data, TimeOut=self.timeout, Environment=self.environment, SecurityGroupIds=self.security_group_ids, KeyName=self.key_name, CallbackURL=self.callback_url, InstanceType=self.instance_type, CreatedTime=self.created_time, StartedTime=self.started_time, FinishedTime=self.finishedtime))])
            return response