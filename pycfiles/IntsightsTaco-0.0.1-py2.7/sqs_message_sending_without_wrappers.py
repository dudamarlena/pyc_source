# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/samples/sqs_message_sending_without_wrappers.py
# Compiled at: 2019-09-05 09:49:59
import boto3
from botocore.exceptions import ClientError
import taco.aws_wrappers.sqs_wrapper.sqs_wrapper as sqs_wrapper, taco.aws_wrappers.sqs_wrapper.configs as sqs_configs

def send_message_without_wrappers_example(aws_access_key, aws_secret_key, queue_name, message_body, region_name='us-east-1', delay_seconds=None):
    session = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)
    sqs_resource = session.resource(service_name='sqs', region_name=region_name)
    queue_creation_config = {'QueueName': queue_name, 
       'Attributes': {'DelaySeconds': '0', 
                      'MessageRetentionPeriod': '345600', 
                      'VisibilityTimeout': '60'}}
    queue = sqs_resource.create_queue(**queue_creation_config)
    requested_data = {'MessageBody': message_body}
    if delay_seconds is not None:
        requested_data['DelaySeconds'] = delay_seconds
    print 'Getting queue'
    try:
        queue = sqs_resource.get_queue_by_name(QueueName=queue_name)
    except ClientError as exc:
        print ('Failed to get queue named "{0}"').format(queue_name)
        raise exc

    print ('Sending message {data}').format(data=requested_data)
    try:
        result = queue.send_message(**requested_data)
        print ('Send message result: {result}').format(result=str(result))
    except ClientError as exc:
        print 'Failed to send message'
        raise exc

    return


def send_message_with_wrappers(aws_access_key, aws_secret_key, queue_name, message_body, region_name='us-east-1', delay_seconds=None):
    sqs = sqs_wrapper.SQSWrapper(aws_access_key=aws_access_key, aws_secret_key=aws_secret_key, region_name=region_name)
    creating_sqs_config = sqs_configs.SQSCreationConfig(queue_name, enable_dead_letter_queue=True, force_clean_queue=False, visibility_timeout_seconds=60)
    sqs.create_queue(creating_sqs_config)
    sqs.send_message(queue_name=queue_name, data=message_body, delay_seconds=delay_seconds)


def main():
    send_message_without_wrappers_example(aws_access_key=None, aws_secret_key=None, queue_name='queue_name_number_2', message_body='message_body')
    send_message_with_wrappers(aws_access_key=None, aws_secret_key=None, queue_name='queue_name', message_body='new message body')
    return


if __name__ == '__main__':
    main()