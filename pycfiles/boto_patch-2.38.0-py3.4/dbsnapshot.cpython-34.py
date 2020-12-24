# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/dbsnapshot.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6398 bytes


class DBSnapshot(object):
    __doc__ = '\n    Represents a RDS DB Snapshot\n\n    Properties reference available from the AWS documentation at http://docs.amazonwebservices.com/AmazonRDS/latest/APIReference/API_DBSnapshot.html\n\n    :ivar engine_version: Specifies the version of the database engine\n    :ivar license_model: License model information for the restored DB instance\n    :ivar allocated_storage: Specifies the allocated storage size in gigabytes (GB)\n    :ivar availability_zone: Specifies the name of the Availability Zone the DB Instance was located in at the time of the DB Snapshot\n    :ivar connection: boto.rds.RDSConnection associated with the current object\n    :ivar engine: Specifies the name of the database engine\n    :ivar id: Specifies the identifier for the DB Snapshot (DBSnapshotIdentifier)\n    :ivar instance_create_time: Specifies the time (UTC) when the snapshot was taken\n    :ivar instance_id: Specifies the the DBInstanceIdentifier of the DB Instance this DB Snapshot was created from (DBInstanceIdentifier)\n    :ivar master_username: Provides the master username for the DB Instance\n    :ivar port: Specifies the port that the database engine was listening on at the time of the snapshot\n    :ivar snapshot_create_time: Provides the time (UTC) when the snapshot was taken\n    :ivar status: Specifies the status of this DB Snapshot. Possible values are [ available, backing-up, creating, deleted, deleting, failed, modifying, rebooting, resetting-master-credentials ]\n    :ivar iops: Specifies the Provisioned IOPS (I/O operations per second) value of the DB instance at the time of the snapshot.\n    :ivar option_group_name: Provides the option group name for the DB snapshot.\n    :ivar percent_progress: The percentage of the estimated data that has been transferred.\n    :ivar snapshot_type: Provides the type of the DB snapshot.\n    :ivar source_region: The region that the DB snapshot was created in or copied from.\n    :ivar vpc_id: Provides the Vpc Id associated with the DB snapshot.\n    '

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