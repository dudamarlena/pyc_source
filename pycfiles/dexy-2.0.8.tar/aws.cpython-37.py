# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/aws.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 3484 bytes
from datetime import datetime
from dexy.filters.api import ApiFilter
import dexy.exceptions, getpass, os, urllib
try:
    import boto
    from boto.s3.key import Key
    BOTO_AVAILABLE = True
except ImportError:
    BOTO_AVAILABLE = False

class BotoUploadFilter(ApiFilter):
    __doc__ = '\n    Uses boto library to upload content to S3, returns the URL.\n\n    You can set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY variables in your\n    system environment (the environment that runs the dexy command) or you can\n    set defaults in your ~/.dexyapis file (these will override the\n    environment):\n\n    "AWS" : {\n        "AWS_ACCESS_KEY_ID" : "AKIA...",\n        "AWS_SECRET_ACCESS_KEY" : "hY6cw...",\n        "AWS_BUCKET_NAME" : "my-unique-bucket-name"\n    }\n\n    You can also have a .dexyapis file in the directory in which you run Dexy,\n    and this will override the user-wide .dexyapis file. You can use this to\n    specify a per-project bucket.\n\n    You can add a date to your bucket by specifying strftime codes in your\n    bucket name, this is useful so you don\'t have to worry about all your\n    filenames being unique.\n\n    If you do not set bucket-name, it will default to a name based on your\n    username. This may not be unique across all S3 buckets so it may be\n    necessary for you to specify a name. You can use an existing S3 bucket,\n    a new bucket will be created if your bucket does not already exist.\n    '
    aliases = ['s3', 'botoup']
    _settings = {'api-key-name':'AWS', 
     'output-extensions':[
      '.txt']}
    API_KEY_KEYS = [
     'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_BUCKET_NAME']

    def is_active(self):
        return BOTO_AVAILABLE

    def bucket_name(self):
        """
        Figure out which S3 bucket name to use and create the bucket if it doesn't exist.
        """
        bucket_name = self.read_param('AWS_BUCKET_NAME')
        if not bucket_name:
            try:
                username = getpass.getuser()
                bucket_name = 'dexy-%s' % username
                return bucket_name
            except dexy.exceptions.UserFeedback:
                print("Can't automatically determine username. Please specify AWS_BUCKET_NAME for upload to S3.")
                raise

        bucket_name = datetime.now().strftime(bucket_name)
        self.log_debug('S3 bucket name is %s' % bucket_name)
        return bucket_name

    def boto_connection(self):
        if os.getenv('AWS_ACCESS_KEY_ID'):
            if os.getenv('AWS_SECRET_ACCESS_KEY'):
                return boto.connect_s3()
        aws_access_key_id = self.read_param('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = self.read_param('AWS_SECRET_ACCESS_KEY')
        return boto.connect_s3(aws_access_key_id, aws_secret_access_key)

    def get_bucket(self):
        conn = self.boto_connection()
        return conn.create_bucket(self.bucket_name())

    def process(self):
        b = self.get_bucket()
        k = Key(b)
        k.key = self.input_data.web_safe_document_key()
        self.log_debug('Uploading contents of %s' % self.input_data.storage.data_file())
        k.set_contents_from_filename(self.input_data.storage.data_file())
        k.set_acl('public-read')
        url = 'https://s3.amazonaws.com/%s/%s' % (self.bucket_name(), urllib.quote(k.key))
        self.output_data.set_data(url)