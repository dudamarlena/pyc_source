# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snowpenguin/nagmail/nagios.py
# Compiled at: 2015-07-26 09:27:42
# Size of source mod 2**32: 1937 bytes
import nagiosplugin
from .postfix import *

class MailQueue(nagiosplugin.Resource):
    name = 'MAILQ'

    def __init__(self, mailq_interface: MailQueueInterface):
        self.mailq_interface = mailq_interface

    def probe(self):
        self.mailq_interface.update()
        if self.mailq_interface.has_total_counter():
            yield nagiosplugin.Metric('total', self.mailq_interface.get_total_counter(), min=0)
        if self.mailq_interface.has_active_counter():
            yield nagiosplugin.Metric('active', self.mailq_interface.get_active_counter(), min=0)
        if self.mailq_interface.has_deferred_counter():
            yield nagiosplugin.Metric('deferred', self.mailq_interface.get_deferred_counter(), min=0)


class MailQueueSummary(nagiosplugin.Summary):

    def __init__(self, contexts):
        self.contexts = contexts

    def ok(self, results):
        first = True
        result = ''
        for c in self.contexts:
            if first:
                first = False
            else:
                result += ' - '
            result += '%s: %s' % (c, str(results[c].metric))

        return result


def create_mailq_check(mq_interface, total_warning, total_critical, deferred_warning, deferred_critical):
    check = nagiosplugin.Check(MailQueue(mq_interface))
    summary_contexts = []
    if mq_interface.has_total_counter():
        check.add(nagiosplugin.ScalarContext('total', total_warning, total_critical))
        summary_contexts.append('total')
    if mq_interface.has_active_counter():
        check.add(nagiosplugin.ScalarContext('active', total_warning, total_critical))
        summary_contexts.append('active')
    if mq_interface.has_deferred_counter():
        check.add(nagiosplugin.ScalarContext('deferred', deferred_warning, deferred_critical))
        summary_contexts.append('deferred')
    check.add(MailQueueSummary(summary_contexts))
    return check