# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/aws_sqs_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3692 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_sqs_hook import SQSHook
from airflow.exceptions import AirflowException

class SQSSensor(BaseSensorOperator):
    __doc__ = '\n    Get messages from an SQS queue and then deletes  the message from the SQS queue.\n    If deletion of messages fails an AirflowException is thrown otherwise, the message\n    is pushed through XCom with the key ``message``.\n\n    :param aws_conn_id: AWS connection id\n    :type aws_conn_id: str\n    :param sqs_queue: The SQS queue url (templated)\n    :type sqs_queue: str\n    :param max_messages: The maximum number of messages to retrieve for each poke (templated)\n    :type max_messages: int\n    :param wait_time_seconds: The time in seconds to wait for receiving messages (default: 1 second)\n    :type wait_time_seconds: int\n    '
    template_fields = ('sqs_queue', 'max_messages')

    @apply_defaults
    def __init__(self, sqs_queue, aws_conn_id='aws_default', max_messages=5, wait_time_seconds=1, *args, **kwargs):
        (super(SQSSensor, self).__init__)(*args, **kwargs)
        self.sqs_queue = sqs_queue
        self.aws_conn_id = aws_conn_id
        self.max_messages = max_messages
        self.wait_time_seconds = wait_time_seconds

    def poke(self, context):
        """
        Check for message on subscribed queue and write to xcom the message with key ``messages``

        :param context: the context object
        :type context: dict
        :return: ``True`` if message is available or ``False``
        """
        sqs_hook = SQSHook(aws_conn_id=(self.aws_conn_id))
        sqs_conn = sqs_hook.get_conn()
        self.log.info('SQSSensor checking for message on queue: %s', self.sqs_queue)
        messages = sqs_conn.receive_message(QueueUrl=(self.sqs_queue), MaxNumberOfMessages=(self.max_messages),
          WaitTimeSeconds=(self.wait_time_seconds))
        self.log.info('reveived message %s', str(messages))
        if 'Messages' in messages:
            if len(messages['Messages']) > 0:
                entries = [{'Id':message['MessageId'],  'ReceiptHandle':message['ReceiptHandle']} for message in messages['Messages']]
                result = sqs_conn.delete_message_batch(QueueUrl=(self.sqs_queue), Entries=entries)
                if 'Successful' in result:
                    context['ti'].xcom_push(key='messages', value=messages)
                    return True
                raise AirflowException('Delete SQS Messages failed ' + str(result) + ' for messages ' + str(messages))
        return False