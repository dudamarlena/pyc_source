# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/command/push.py
# Compiled at: 2010-08-17 19:03:01
import boto.s3, logging, os, urllib, apps.command.base

class push(apps.command.base.Command):
    help = 'Push the packaged project to a remote resource.'
    user_options = [
     ('aws-secret=', None, 'aws secret for S3 upload', None),
     ('aws-key=', None, 'aws key for S3 upload', None),
     ('url=', None, 'url to upload to', None)]
    default_options = {'path': ''}
    pre_commands = [
     'package']

    def run(self):
        if 'url' not in self.options:
            logging.error('Must include an url to upload to. (ex. s3://apps.bittorrent.com/foo/bar.btapp')
            return
        protocol = self.options['url'].split(':')[0]
        try:
            getattr(self, 'push_%s' % (protocol,))()
        except AttributeError:
            logging.error('The <%s> protocol is not supported. Supported protocols are %s' % (
             protocol,
             (',').join([ x.split('_')[(-1)] for x in filter(lambda x: x.startswith('push_'), dir(self))
             ])))
            return

    def package_name(self):
        extension = 'pkg' if self.project.metadata.get('bt:package', False) else 'btapp'
        return os.path.join('dist', '%s.%s' % (self.project.metadata['name'],
         extension))

    def push_s3(self):
        base_url = self.options['url'][5:]
        (bucket, fname) = base_url.split('/', 1)
        if 'aws-secret' not in self.options:
            logging.error('Must include your aws secret. (--aws-secret)')
            return
        else:
            if 'aws-key' not in self.options:
                logging.error('Must include your aws key. (--aws-key)')
                return
            conn = boto.connect_s3(self.options['aws-key'], self.options['aws-secret'])
            try:
                bucket = conn.get_bucket(bucket)
            except:
                bucket = conn.create_bucket(bucket)

            key = bucket.new_key(fname)
            acl = key.get_acl() if key.exists() else None
            key.set_contents_from_filename(self.package_name(), replace=True)
            if acl:
                key.set_acl(acl)
            return