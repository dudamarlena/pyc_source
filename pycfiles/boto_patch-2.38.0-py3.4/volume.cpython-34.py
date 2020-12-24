# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/manage/volume.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 16296 bytes
from __future__ import print_function
from boto.sdb.db.model import Model
from boto.sdb.db.property import StringProperty, IntegerProperty, ListProperty, ReferenceProperty, CalculatedProperty
from boto.manage.server import Server
from boto.manage import propget
import boto.utils, boto.ec2, time, traceback
from contextlib import closing
import datetime

class CommandLineGetter(object):

    def get_region(self, params):
        if not params.get('region', None):
            prop = self.cls.find_property('region_name')
            params['region'] = propget.get(prop, choices=boto.ec2.regions)

    def get_zone(self, params):
        if not params.get('zone', None):
            prop = StringProperty(name='zone', verbose_name='EC2 Availability Zone', choices=self.ec2.get_all_zones)
            params['zone'] = propget.get(prop)

    def get_name(self, params):
        if not params.get('name', None):
            prop = self.cls.find_property('name')
            params['name'] = propget.get(prop)

    def get_size(self, params):
        if not params.get('size', None):
            prop = IntegerProperty(name='size', verbose_name='Size (GB)')
            params['size'] = propget.get(prop)

    def get_mount_point(self, params):
        if not params.get('mount_point', None):
            prop = self.cls.find_property('mount_point')
            params['mount_point'] = propget.get(prop)

    def get_device(self, params):
        if not params.get('device', None):
            prop = self.cls.find_property('device')
            params['device'] = propget.get(prop)

    def get(self, cls, params):
        self.cls = cls
        self.get_region(params)
        self.ec2 = params['region'].connect()
        self.get_zone(params)
        self.get_name(params)
        self.get_size(params)
        self.get_mount_point(params)
        self.get_device(params)


class Volume(Model):
    name = StringProperty(required=True, unique=True, verbose_name='Name')
    region_name = StringProperty(required=True, verbose_name='EC2 Region')
    zone_name = StringProperty(required=True, verbose_name='EC2 Zone')
    mount_point = StringProperty(verbose_name='Mount Point')
    device = StringProperty(verbose_name='Device Name', default='/dev/sdp')
    volume_id = StringProperty(required=True)
    past_volume_ids = ListProperty(item_type=str)
    server = ReferenceProperty(Server, collection_name='volumes', verbose_name='Server Attached To')
    volume_state = CalculatedProperty(verbose_name='Volume State', calculated_type=str, use_method=True)
    attachment_state = CalculatedProperty(verbose_name='Attachment State', calculated_type=str, use_method=True)
    size = CalculatedProperty(verbose_name='Size (GB)', calculated_type=int, use_method=True)

    @classmethod
    def create(cls, **params):
        getter = CommandLineGetter()
        getter.get(cls, params)
        region = params.get('region')
        ec2 = region.connect()
        zone = params.get('zone')
        size = params.get('size')
        ebs_volume = ec2.create_volume(size, zone.name)
        v = cls()
        v.ec2 = ec2
        v.volume_id = ebs_volume.id
        v.name = params.get('name')
        v.mount_point = params.get('mount_point')
        v.device = params.get('device')
        v.region_name = region.name
        v.zone_name = zone.name
        v.put()
        return v

    @classmethod
    def create_from_volume_id(cls, region_name, volume_id, name):
        vol = None
        ec2 = boto.ec2.connect_to_region(region_name)
        rs = ec2.get_all_volumes([volume_id])
        if len(rs) == 1:
            v = rs[0]
            vol = cls()
            vol.volume_id = v.id
            vol.name = name
            vol.region_name = v.region.name
            vol.zone_name = v.zone
            vol.put()
        return vol

    def create_from_latest_snapshot(self, name, size=None):
        snapshot = self.get_snapshots()[(-1)]
        return self.create_from_snapshot(name, snapshot, size)

    def create_from_snapshot(self, name, snapshot, size=None):
        if size < self.size:
            size = self.size
        ec2 = self.get_ec2_connection()
        if self.zone_name is None or self.zone_name == '':
            current_volume = ec2.get_all_volumes([self.volume_id])[0]
            self.zone_name = current_volume.zone
        ebs_volume = ec2.create_volume(size, self.zone_name, snapshot)
        v = Volume()
        v.ec2 = self.ec2
        v.volume_id = ebs_volume.id
        v.name = name
        v.mount_point = self.mount_point
        v.device = self.device
        v.region_name = self.region_name
        v.zone_name = self.zone_name
        v.put()
        return v

    def get_ec2_connection(self):
        if self.server:
            return self.server.ec2
        if not hasattr(self, 'ec2') or self.ec2 is None:
            self.ec2 = boto.ec2.connect_to_region(self.region_name)
        return self.ec2

    def _volume_state(self):
        ec2 = self.get_ec2_connection()
        rs = ec2.get_all_volumes([self.volume_id])
        return rs[0].volume_state()

    def _attachment_state(self):
        ec2 = self.get_ec2_connection()
        rs = ec2.get_all_volumes([self.volume_id])
        return rs[0].attachment_state()

    def _size(self):
        if not hasattr(self, '__size'):
            ec2 = self.get_ec2_connection()
            rs = ec2.get_all_volumes([self.volume_id])
            self._Volume__size = rs[0].size
        return self._Volume__size

    def install_xfs(self):
        if self.server:
            self.server.install('xfsprogs xfsdump')

    def get_snapshots(self):
        """
        Returns a list of all completed snapshots for this volume ID.
        """
        ec2 = self.get_ec2_connection()
        rs = ec2.get_all_snapshots()
        all_vols = [self.volume_id] + self.past_volume_ids
        snaps = []
        for snapshot in rs:
            if snapshot.volume_id in all_vols:
                if snapshot.progress == '100%':
                    snapshot.date = boto.utils.parse_ts(snapshot.start_time)
                    snapshot.keep = True
                    snaps.append(snapshot)
                else:
                    continue

        snaps.sort(cmp=lambda x, y: cmp(x.date, y.date))
        return snaps

    def attach(self, server=None):
        if self.attachment_state == 'attached':
            print('already attached')
            return
        if server:
            self.server = server
            self.put()
        ec2 = self.get_ec2_connection()
        ec2.attach_volume(self.volume_id, self.server.instance_id, self.device)

    def detach(self, force=False):
        state = self.attachment_state
        if state == 'available' or state is None or state == 'detaching':
            print('already detached')
            return
        ec2 = self.get_ec2_connection()
        ec2.detach_volume(self.volume_id, self.server.instance_id, self.device, force)
        self.server = None
        self.put()

    def checkfs(self, use_cmd=None):
        if self.server is None:
            raise ValueError('server attribute must be set to run this command')
        if use_cmd:
            cmd = use_cmd
        else:
            cmd = self.server.get_cmdshell()
        status = cmd.run('xfs_check %s' % self.device)
        if not use_cmd:
            cmd.close()
        if status[1].startswith('bad superblock magic number 0'):
            return False
        return True

    def wait(self):
        if self.server is None:
            raise ValueError('server attribute must be set to run this command')
        with closing(self.server.get_cmdshell()) as (cmd):
            cmd = self.server.get_cmdshell()
            while not cmd.exists(self.device):
                boto.log.info('%s still does not exist, waiting 10 seconds' % self.device)
                time.sleep(10)

    def format(self):
        if self.server is None:
            raise ValueError('server attribute must be set to run this command')
        status = None
        with closing(self.server.get_cmdshell()) as (cmd):
            if not self.checkfs(cmd):
                boto.log.info('make_fs...')
                status = cmd.run('mkfs -t xfs %s' % self.device)
        return status

    def mount(self):
        if self.server is None:
            raise ValueError('server attribute must be set to run this command')
        boto.log.info('handle_mount_point')
        with closing(self.server.get_cmdshell()) as (cmd):
            cmd = self.server.get_cmdshell()
            if not cmd.isdir(self.mount_point):
                boto.log.info('making directory')
                cmd.run('mkdir %s' % self.mount_point)
            else:
                boto.log.info('directory exists already')
                status = cmd.run('mount -l')
                lines = status[1].split('\n')
                for line in lines:
                    t = line.split()
                    if t and t[2] == self.mount_point:
                        if t[0] != self.device:
                            cmd.run('umount %s' % self.mount_point)
                            cmd.run('mount %s /tmp' % t[0])
                            cmd.run('chmod 777 /tmp')
                            break
                        else:
                            continue

            cmd.run('mount %s %s' % (self.device, self.mount_point))
            cmd.run('xfs_growfs %s' % self.mount_point)

    def make_ready(self, server):
        self.server = server
        self.put()
        self.install_xfs()
        self.attach()
        self.wait()
        self.format()
        self.mount()

    def freeze(self):
        if self.server:
            return self.server.run('/usr/sbin/xfs_freeze -f %s' % self.mount_point)

    def unfreeze(self):
        if self.server:
            return self.server.run('/usr/sbin/xfs_freeze -u %s' % self.mount_point)

    def snapshot(self):
        try:
            try:
                self.freeze()
                if self.server is None:
                    snapshot = self.get_ec2_connection().create_snapshot(self.volume_id)
                else:
                    snapshot = self.server.ec2.create_snapshot(self.volume_id)
                boto.log.info('Snapshot of Volume %s created: %s' % (self.name, snapshot))
            except Exception:
                boto.log.info('Snapshot error')
                boto.log.info(traceback.format_exc())

        finally:
            status = self.unfreeze()
            return status

    def get_snapshot_range(self, snaps, start_date=None, end_date=None):
        l = []
        for snap in snaps:
            if start_date and end_date:
                if snap.date >= start_date:
                    if snap.date <= end_date:
                        l.append(snap)
            elif start_date:
                if snap.date >= start_date:
                    l.append(snap)
            elif end_date:
                if snap.date <= end_date:
                    l.append(snap)
            else:
                l.append(snap)

        return l

    def trim_snapshots(self, delete=False):
        """
        Trim the number of snapshots for this volume.  This method always
        keeps the oldest snapshot.  It then uses the parameters passed in
        to determine how many others should be kept.

        The algorithm is to keep all snapshots from the current day.  Then
        it will keep the first snapshot of the day for the previous seven days.
        Then, it will keep the first snapshot of the week for the previous
        four weeks.  After than, it will keep the first snapshot of the month
        for as many months as there are.

        """
        snaps = self.get_snapshots()
        if len(snaps) <= 2:
            return snaps
        snaps = snaps[1:-1]
        now = datetime.datetime.now(snaps[0].date.tzinfo)
        midnight = datetime.datetime(year=now.year, month=now.month, day=now.day, tzinfo=now.tzinfo)
        one_week = datetime.timedelta(days=7, seconds=3600)
        print(midnight - one_week, midnight)
        previous_week = self.get_snapshot_range(snaps, midnight - one_week, midnight)
        print(previous_week)
        if not previous_week:
            return snaps
        current_day = None
        for snap in previous_week:
            if current_day and current_day == snap.date.day:
                snap.keep = False
            else:
                current_day = snap.date.day

        if previous_week:
            week_boundary = previous_week[0].date
            if week_boundary.weekday() != 0:
                delta = datetime.timedelta(days=week_boundary.weekday())
                week_boundary = week_boundary - delta
        partial_week = self.get_snapshot_range(snaps, week_boundary, previous_week[0].date)
        if len(partial_week) > 1:
            for snap in partial_week[1:]:
                snap.keep = False

        for i in range(0, 4):
            weeks_worth = self.get_snapshot_range(snaps, week_boundary - one_week, week_boundary)
            if len(weeks_worth) > 1:
                for snap in weeks_worth[1:]:
                    snap.keep = False

            week_boundary = week_boundary - one_week

        remainder = self.get_snapshot_range(snaps, end_date=week_boundary)
        current_month = None
        for snap in remainder:
            if current_month and current_month == snap.date.month:
                snap.keep = False
            else:
                current_month = snap.date.month

        if delete:
            for snap in snaps:
                if not snap.keep:
                    boto.log.info('Deleting %s(%s) for %s' % (snap, snap.date, self.name))
                    snap.delete()
                    continue

        return snaps

    def grow(self, size):
        pass

    def copy(self, snapshot):
        pass

    def get_snapshot_from_date(self, date):
        pass

    def delete(self, delete_ebs_volume=False):
        if delete_ebs_volume:
            self.detach()
            ec2 = self.get_ec2_connection()
            ec2.delete_volume(self.volume_id)
        super(Volume, self).delete()

    def archive(self):
        pass