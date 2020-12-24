# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/fedmsg_atomic_composer/consumer.py
# Compiled at: 2017-02-21 11:50:59
import fedmsg.consumers
from twisted.internet import reactor
from .composer import AtomicComposer

class AtomicConsumer(fedmsg.consumers.FedmsgConsumer):
    """A fedmsg-driven atomic ostree composer.

    This consumer runs in the fedmsg-hub and reacts to whenever repositories
    sync to the master mirror.
    """
    config_key = 'atomic_composer'

    def __init__(self, hub, *args, **kw):
        for key, item in hub.config.items():
            setattr(self, key, item)

        self.topic = getattr(self, 'fedmsg_atomic_topic', None)
        super(AtomicConsumer, self).__init__(hub, *args, **kw)
        if not self.topic:
            self.log.warn("No 'fedmsg_atomic_topic' set.")
        return

    def consume(self, msg):
        """Called with each incoming fedmsg.

        From here we trigger an rpm-ostree compose by touching a specific file
        under the `touch_dir`. Then our `doRead` method is called with the
        output of the rpm-ostree-toolbox treecompose, which we monitor to
        determine when it has completed.
        """
        self.log.info(msg)
        body = msg['body']
        topic = body['topic']
        repo = None
        if 'rawhide' in topic:
            arch = body['msg']['arch']
            self.log.info('New rawhide %s compose ready', arch)
            repo = 'rawhide'
        elif 'branched' in topic:
            arch = body['msg']['arch']
            branch = body['msg']['branch']
            self.log.info('New %s %s branched compose ready', branch, arch)
            log = body['msg']['log']
            if log != 'done':
                self.log.warn('Compose not done?')
                return
            repo = branch
        elif 'updates.fedora' in topic:
            self.log.info('New Fedora %(release)s %(repo)s compose ready', body['msg'])
            repo = 'f%(release)s-%(repo)s' % body['msg']
        else:
            self.log.warn('Unknown topic: %s', topic)
        release = self.releases[repo]
        reactor.callInThread(self.compose, release)
        return

    def compose(self, release):
        self.composer = AtomicComposer()
        result = self.composer.compose(release)
        if result['result'] == 'success':
            self.log.info(result)
        else:
            self.log.error(result)