# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/keypair.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 4351 bytes
"""
Represents an EC2 Keypair
"""
import os
from boto.ec2.ec2object import EC2Object
from boto.exception import BotoClientError

class KeyPair(EC2Object):

    def __init__(self, connection=None):
        super(KeyPair, self).__init__(connection)
        self.name = None
        self.fingerprint = None
        self.material = None

    def __repr__(self):
        return 'KeyPair:%s' % self.name

    def endElement(self, name, value, connection):
        if name == 'keyName':
            self.name = value
        else:
            if name == 'keyFingerprint':
                self.fingerprint = value
            else:
                if name == 'keyMaterial':
                    self.material = value
                else:
                    setattr(self, name, value)

    def delete(self, dry_run=False):
        """
        Delete the KeyPair.

        :rtype: bool
        :return: True if successful, otherwise False.
        """
        return self.connection.delete_key_pair(self.name, dry_run=dry_run)

    def save(self, directory_path):
        """
        Save the material (the unencrypted PEM encoded RSA private key)
        of a newly created KeyPair to a local file.

        :type directory_path: string
        :param directory_path: The fully qualified path to the directory
                               in which the keypair will be saved.  The
                               keypair file will be named using the name
                               of the keypair as the base name and .pem
                               for the file extension.  If a file of that
                               name already exists in the directory, an
                               exception will be raised and the old file
                               will not be overwritten.

        :rtype: bool
        :return: True if successful.
        """
        if self.material:
            directory_path = os.path.expanduser(directory_path)
            file_path = os.path.join(directory_path, '%s.pem' % self.name)
            if os.path.exists(file_path):
                raise BotoClientError('%s already exists, it will not be overwritten' % file_path)
            fp = open(file_path, 'wb')
            fp.write(self.material)
            fp.close()
            os.chmod(file_path, 384)
            return True
        raise BotoClientError('KeyPair contains no material')

    def copy_to_region(self, region, dry_run=False):
        """
        Create a new key pair of the same new in another region.
        Note that the new key pair will use a different ssh
        cert than the this key pair.  After doing the copy,
        you will need to save the material associated with the
        new key pair (use the save method) to a local file.

        :type region: :class:`boto.ec2.regioninfo.RegionInfo`
        :param region: The region to which this security group will be copied.

        :rtype: :class:`boto.ec2.keypair.KeyPair`
        :return: The new key pair
        """
        if region.name == self.region:
            raise BotoClientError('Unable to copy to the same Region')
        conn_params = self.connection.get_params()
        rconn = region.connect(**conn_params)
        kp = rconn.create_key_pair(self.name, dry_run=dry_run)
        return kp