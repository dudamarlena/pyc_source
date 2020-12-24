# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/dbsnapshot.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6398 bytes


class DBSnapshot(object):
    """DBSnapshot"""

    def __init__(self, connection=None, id=None):
        self.connection = connection
        self.id = id
        self.engine = None
        self.engine_version = None
        self.snapshot_create_time = None
        self.instance_create_time = None
        self.port = None
        self.status = None
        self.availability_zone = None
        self.master_username = None
        self.allocated_storage = None
        self.instance_id = None
        self.availability_zone = None
        self.license_model = None
        self.iops = None
        self.option_group_name = None
        self.percent_progress = None
        self.snapshot_type = None
        self.source_region = None
        self.vpc_id = None

    def __repr__(self):
        return 'DBSnapshot:%s' % self.id

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Engine':
            self.engine = value
        else:
            if name == 'EngineVersion':
                self.engine_version = value
            else:
                if name == 'InstanceCreateTime':
                    self.instance_create_time = value
                else:
                    if name == 'SnapshotCreateTime':
                        self.snapshot_create_time = value
                    else:
                        if name == 'DBInstanceIdentifier':
                            self.instance_id = value
                        else:
                            if name == 'DBSnapshotIdentifier':
                                self.id = value
                            else:
                                if name == 'Port':
                                    self.port = int(value)
                                else:
                                    if name == 'Status':
                                        self.status = value
                                    else:
                                        if name == 'AvailabilityZone':
                                            self.availability_zone = value
                                        else:
                                            if name == 'MasterUsername':
                                                self.master_username = value
                                            else:
                                                if name == 'AllocatedStorage':
                                                    self.allocated_storage = int(value)
                                                else:
                                                    if name == 'SnapshotTime':
                                                        self.time = value
                                                    else:
                                                        if name == 'LicenseModel':
                                                            self.license_model = value
                                                        else:
                                                            if name == 'Iops':
                                                                self.iops = int(value)
                                                            else:
                                                                if name == 'OptionGroupName':
                                                                    self.option_group_name = value
                                                                else:
                                                                    if name == 'PercentProgress':
                                                                        self.percent_progress = int(value)
                                                                    else:
                                                                        if name == 'SnapshotType':
                                                                            self.snapshot_type = value
                                                                        else:
                                                                            if name == 'SourceRegion':
                                                                                self.source_region = value
                                                                            else:
                                                                                if name == 'VpcId':
                                                                                    self.vpc_id = value
                                                                                else:
                                                                                    setattr(self, name, value)

    def update(self, validate=False):
        """
        Update the DB snapshot's status information by making a call to fetch
        the current snapshot attributes from the service.

        :type validate: bool
        :param validate: By default, if EC2 returns no data about the
                         instance the update method returns quietly.  If
                         the validate param is True, however, it will
                         raise a ValueError exception if no data is
                         returned from EC2.
        """
        rs = self.connection.get_all_dbsnapshots(self.id)
        if len(rs) > 0:
            for i in rs:
                if i.id == self.id:
                    self.__dict__.update(i.__dict__)
                    continue

        elif validate:
            raise ValueError('%s is not a valid Snapshot ID' % self.id)
        return self.status