# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/snowpenguin/nagmail/postfix.py
# Compiled at: 2015-07-26 08:18:09
# Size of source mod 2**32: 2053 bytes
import io, subprocess
from .common import MailQueueInterface, MailQueueDataFetchError

class PostfixMailQueue(MailQueueInterface):

    def __init__(self, data_generator):
        super(PostfixMailQueue, self).__init__(data_generator)
        self.deferred = 0
        self.active = 0
        self.total = 0

    def has_deferred_counter(self):
        return True

    def get_deferred_counter(self):
        return self.deferred

    def has_active_counter(self):
        return True

    def get_active_counter(self):
        return self.active

    def has_total_counter(self):
        return True

    def get_total_counter(self):
        return self.total

    def update(self):
        mailq_output = self.data_generator()
        self.deferred = 0
        self.active = 0
        self.total = 0
        if mailq_output is None:
            return
        for line in mailq_output:
            if not line is None:
                if not len(line) == 0:
                    if line[0] not in '0123456789ABCDEF':
                        continue
                    queue_item = line.split(' ')
                    queue_item_id = queue_item[0]
                    self.total += 1
                    if queue_item_id.endswith('*'):
                        self.active += 1
            elif queue_item_id.endswith('!'):
                continue
                self.deferred += 1


MailQueueInterface.register(PostfixMailQueue)

class PostfixMailqFetcher:

    def __init__(self, use_sudo=False):
        self.sudo = use_sudo

    def get_data(self):
        popen_target = ['sudo', 'mailq'] if self.sudo else ['mailq']
        try:
            p = subprocess.Popen(popen_target, stderr=subprocess.PIPE, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            pres, err = p.communicate()
        except FileNotFoundError as e:
            raise MailQueueDataFetchError(e)

        if err:
            raise MailQueueDataFetchError(err)
        if pres:
            return io.StringIO(pres.decode('utf-8'))