# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/appevents.py
# Compiled at: 2017-04-06 03:55:39
# Size of source mod 2**32: 3104 bytes
"""Process application events."""
import tempfile, logging, os, time, kazoo.client, yaml
from treadmill import exc
from treadmill import idirwatch
from treadmill import sysinfo
from treadmill import zkutils
from treadmill import zknamespace as z
_LOGGER = logging.getLogger(__name__)
_SERVERS_ACL = zkutils.make_role_acl('servers', 'rwcd')
_HOSTNAME = sysinfo.hostname()

def post(events_dir, event):
    """Post application event to event directory.
    """
    _LOGGER.debug('post: %s: %r', events_dir, event)
    _ts, _src, instanceid, event_type, event_data, payload = event.to_data()
    filename = '%s,%s,%s,%s' % (
     time.time(),
     instanceid,
     event_type,
     '' if event_data is None else event_data)
    with tempfile.NamedTemporaryFile(dir=events_dir, delete=False, prefix='.tmp', mode='w') as (temp):
        if isinstance(payload, str):
            temp.write(payload)
        else:
            yaml.dump(payload, stream=temp)
    os.rename(temp.name, os.path.join(events_dir, filename))


class AppEventsWatcher(object):
    __doc__ = 'Publish app events from the queue.'

    def __init__(self, zkclient, events_dir):
        self.zkclient = zkclient
        self.events_dir = events_dir

    def run(self):
        """Monitores events directory and publish events."""
        watch = idirwatch.DirWatcher(self.events_dir)
        watch.on_created = self._on_created
        for eventfile in os.listdir(self.events_dir):
            filename = os.path.join(self.events_dir, eventfile)
            self._on_created(filename)

        while 1:
            if watch.wait_for_events(60):
                watch.process_events()
                continue

    @exc.exit_on_unhandled
    def _on_created(self, path):
        """This is the handler function when new files are seen"""
        if not os.path.exists(path):
            return
        localpath = os.path.basename(path)
        if localpath.startswith('.'):
            return
        _LOGGER.info('New event file - %r', path)
        eventtime, appname, event, data = localpath.split(',', 4)
        with open(path) as (f):
            eventnode = '%s,%s,%s,%s' % (eventtime, _HOSTNAME, event, data)
            _LOGGER.debug('Creating %s', z.path.task(appname, eventnode))
            try:
                zkutils.with_retry(self.zkclient.create, z.path.task(appname, eventnode), f.read(), acl=[
                 _SERVERS_ACL], makepath=True)
            except kazoo.client.NodeExistsError:
                pass

        if event in ('aborted', 'killed', 'finished'):
            scheduled_node = z.path.scheduled(appname)
            _LOGGER.info('Unscheduling, event=%s: %s', event, scheduled_node)
            zkutils.with_retry(zkutils.ensure_deleted, self.zkclient, scheduled_node)
        os.unlink(path)