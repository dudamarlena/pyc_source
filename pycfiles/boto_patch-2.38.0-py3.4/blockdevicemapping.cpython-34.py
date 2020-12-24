# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/blockdevicemapping.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6372 bytes


class BlockDeviceType(object):
    __doc__ = '\n    Represents parameters for a block device.\n    '

    def __init__(self, connection=None, ephemeral_name=None, no_device=False, volume_id=None, snapshot_id=None, status=None, attach_time=None, delete_on_termination=False, size=None, volume_type=None, iops=None, encrypted=None):
        self.connection = connection
        self.ephemeral_name = ephemeral_name
        self.no_device = no_device
        self.volume_id = volume_id
        self.snapshot_id = snapshot_id
        self.status = status
        self.attach_time = attach_time
        self.delete_on_termination = delete_on_termination
        self.size = size
        self.volume_type = volume_type
        self.iops = iops
        self.encrypted = encrypted

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        lname = name.lower()
        if name == 'volumeId':
            self.volume_id = value
        else:
            if lname == 'virtualname':
                self.ephemeral_name = value
            else:
                if lname == 'nodevice':
                    self.no_device = value == 'true'
                else:
                    if lname == 'snapshotid':
                        self.snapshot_id = value
                    else:
                        if lname == 'volumesize':
                            self.size = int(value)
                        else:
                            if lname == 'status':
                                self.status = value
                            else:
                                if lname == 'attachtime':
                                    self.attach_time = value
                                else:
                                    if lname == 'deleteontermination':
                                        self.delete_on_termination = value == 'true'
                                    else:
                                        if lname == 'volumetype':
                                            self.volume_type = value
                                        else:
                                            if lname == 'iops':
                                                self.iops = int(value)
                                            else:
                                                if lname == 'encrypted':
                                                    self.encrypted = value == 'true'
                                                else:
                                                    setattr(self, name, value)


EBSBlockDeviceType = BlockDeviceType

class BlockDeviceMapping(dict):
    __doc__ = "\n    Represents a collection of BlockDeviceTypes when creating ec2 instances.\n\n    Example:\n    dev_sda1 = BlockDeviceType()\n    dev_sda1.size = 100   # change root volume to 100GB instead of default\n    bdm = BlockDeviceMapping()\n    bdm['/dev/sda1'] = dev_sda1\n    reservation = image.run(..., block_device_map=bdm, ...)\n    "

    def __init__(self, connection=None):
        """
        :type connection: :class:`boto.ec2.EC2Connection`
        :param connection: Optional connection.
        """
        dict.__init__(self)
        self.connection = connection
        self.current_name = None
        self.current_value = None

    def startElement(self, name, attrs, connection):
        lname = name.lower()
        if lname in ('ebs', 'virtualname'):
            self.current_value = BlockDeviceType(self)
            return self.current_value

    def endElement(self, name, value, connection):
        lname = name.lower()
        if lname in ('device', 'devicename'):
            self.current_name = value
        elif lname in ('item', 'member'):
            self[self.current_name] = self.current_value

    def ec2_build_list_params(self, params, prefix=''):
        pre = '%sBlockDeviceMapping' % prefix
        return self._build_list_params(params, prefix=pre)

    def autoscale_build_list_params(self, params, prefix=''):
        pre = '%sBlockDeviceMappings.member' % prefix
        return self._build_list_params(params, prefix=pre)

    def _build_list_params(self, params, prefix=''):
        i = 1
        for dev_name in self:
            pre = '%s.%d' % (prefix, i)
            params['%s.DeviceName' % pre] = dev_name
            block_dev = self[dev_name]
            if block_dev.ephemeral_name:
                params['%s.VirtualName' % pre] = block_dev.ephemeral_name
            else:
                if block_dev.no_device:
                    params['%s.NoDevice' % pre] = ''
                else:
                    if block_dev.snapshot_id:
                        params['%s.Ebs.SnapshotId' % pre] = block_dev.snapshot_id
                    if block_dev.size:
                        params['%s.Ebs.VolumeSize' % pre] = block_dev.size
                    if block_dev.delete_on_termination:
                        params['%s.Ebs.DeleteOnTermination' % pre] = 'true'
                    else:
                        params['%s.Ebs.DeleteOnTermination' % pre] = 'false'
                    if block_dev.volume_type:
                        params['%s.Ebs.VolumeType' % pre] = block_dev.volume_type
                    if block_dev.iops is not None:
                        params['%s.Ebs.Iops' % pre] = block_dev.iops
                    if block_dev.encrypted is not None:
                        if block_dev.encrypted:
                            params['%s.Ebs.Encrypted' % pre] = 'true'
                        else:
                            params['%s.Ebs.Encrypted' % pre] = 'false'
            i += 1