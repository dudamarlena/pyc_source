# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/snapshot.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 7539 bytes
__doc__ = '\nRepresents an EC2 Elastic Block Store Snapshot\n'
from boto.ec2.ec2object import TaggedEC2Object
from boto.ec2.zone import Zone

class Snapshot(TaggedEC2Object):
    """Snapshot"""
    AttrName = 'createVolumePermission'

    def __init__(self, connection=None):
        super(Snapshot, self).__init__(connection)
        self.id = None
        self.volume_id = None
        self.status = None
        self.progress = None
        self.start_time = None
        self.owner_id = None
        self.owner_alias = None
        self.volume_size = None
        self.description = None
        self.encrypted = None

    def __repr__(self):
        return 'Snapshot:%s' % self.id

    def endElement(self, name, value, connection):
        if name == 'snapshotId':
            self.id = value
        else:
            if name == 'volumeId':
                self.volume_id = value
            else:
                if name == 'status':
                    self.status = value
                else:
                    if name == 'startTime':
                        self.start_time = value
                    else:
                        if name == 'ownerId':
                            self.owner_id = value
                        else:
                            if name == 'ownerAlias':
                                self.owner_alias = value
                            elif name == 'volumeSize':
                                try:
                                    self.volume_size = int(value)
                                except:
                                    self.volume_size = value

                            else:
                                if name == 'description':
                                    self.description = value
                                else:
                                    if name == 'encrypted':
                                        self.encrypted = value.lower() == 'true'
                                    else:
                                        setattr(self, name, value)

    def _update(self, updated):
        self.progress = updated.progress
        self.status = updated.status

    def update(self, validate=False, dry_run=False):
        """
        Update the data associated with this snapshot by querying EC2.

        :type validate: bool
        :param validate: By default, if EC2 returns no data about the
                         snapshot the update method returns quietly.  If
                         the validate param is True, however, it will
                         raise a ValueError exception if no data is
                         returned from EC2.
        """
        rs = self.connection.get_all_snapshots([self.id], dry_run=dry_run)
        if len(rs) > 0:
            self._update(rs[0])
        elif validate:
            raise ValueError('%s is not a valid Snapshot ID' % self.id)
        return self.progress

    def delete(self, dry_run=False):
        return self.connection.delete_snapshot(self.id, dry_run=dry_run)

    def get_permissions(self, dry_run=False):
        attrs = self.connection.get_snapshot_attribute(self.id, self.AttrName, dry_run=dry_run)
        return attrs.attrs

    def share(self, user_ids=None, groups=None, dry_run=False):
        return self.connection.modify_snapshot_attribute(self.id, self.AttrName, 'add', user_ids, groups, dry_run=dry_run)

    def unshare(self, user_ids=None, groups=None, dry_run=False):
        return self.connection.modify_snapshot_attribute(self.id, self.AttrName, 'remove', user_ids, groups, dry_run=dry_run)

    def reset_permissions(self, dry_run=False):
        return self.connection.reset_snapshot_attribute(self.id, self.AttrName, dry_run=dry_run)

    def create_volume(self, zone, size=None, volume_type=None, iops=None, dry_run=False):
        """
        Create a new EBS Volume from this Snapshot

        :type zone: string or :class:`boto.ec2.zone.Zone`
        :param zone: The availability zone in which the Volume will be created.

        :type size: int
        :param size: The size of the new volume, in GiB. (optional). Defaults to
            the size of the snapshot.

        :type volume_type: string
        :param volume_type: The type of the volume. (optional).  Valid
            values are: standard | io1 | gp2.

        :type iops: int
        :param iops: The provisioned IOPs you want to associate with
            this volume. (optional)
        """
        if isinstance(zone, Zone):
            zone = zone.name
        return self.connection.create_volume(size, zone, self.id, volume_type, iops, self.encrypted, dry_run=dry_run)


class SnapshotAttribute(object):

    def __init__(self, parent=None):
        self.snapshot_id = None
        self.attrs = {}

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'createVolumePermission':
            self.name = 'create_volume_permission'
        else:
            if name == 'group':
                if 'groups' in self.attrs:
                    self.attrs['groups'].append(value)
                else:
                    self.attrs['groups'] = [
                     value]
            else:
                if name == 'userId':
                    if 'user_ids' in self.attrs:
                        self.attrs['user_ids'].append(value)
                    else:
                        self.attrs['user_ids'] = [
                         value]
                else:
                    if name == 'snapshotId':
                        self.snapshot_id = value
                    else:
                        setattr(self, name, value)