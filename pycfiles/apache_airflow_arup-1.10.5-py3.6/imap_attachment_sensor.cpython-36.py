# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/imap_attachment_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3024 bytes
from airflow.contrib.hooks.imap_hook import ImapHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class ImapAttachmentSensor(BaseSensorOperator):
    __doc__ = "\n    Waits for a specific attachment on a mail server.\n\n    :param attachment_name: The name of the attachment that will be checked.\n    :type attachment_name: str\n    :param check_regex: If set to True the attachment's name will be parsed as regular expression.\n                        Through this you can get a broader set of attachments\n                        that it will look for than just only the equality of the attachment name.\n                        The default value is False.\n    :type check_regex: bool\n    :param mail_folder: The mail folder in where to search for the attachment.\n                        The default value is 'INBOX'.\n    :type mail_folder: str\n    :param conn_id: The connection to run the sensor against.\n                    The default value is 'imap_default'.\n    :type conn_id: str\n    "
    template_fields = ('attachment_name', )

    @apply_defaults
    def __init__(self, attachment_name, mail_folder='INBOX', check_regex=False, conn_id='imap_default', *args, **kwargs):
        (super(ImapAttachmentSensor, self).__init__)(*args, **kwargs)
        self.attachment_name = attachment_name
        self.mail_folder = mail_folder
        self.check_regex = check_regex
        self.conn_id = conn_id

    def poke(self, context):
        """
        Pokes for a mail attachment on the mail server.

        :param context: The context that is being provided when poking.
        :type context: dict
        :return: True if attachment with the given name is present and False if not.
        :rtype: bool
        """
        self.log.info('Poking for %s', self.attachment_name)
        with ImapHook(imap_conn_id=(self.conn_id)) as (imap_hook):
            return imap_hook.has_mail_attachment(name=(self.attachment_name),
              mail_folder=(self.mail_folder),
              check_regex=(self.check_regex))