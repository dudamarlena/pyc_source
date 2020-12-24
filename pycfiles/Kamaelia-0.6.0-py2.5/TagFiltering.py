# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Whiteboard/TagFiltering.py
# Compiled at: 2008-10-19 12:19:52
from Axon.Component import component
from Axon.Ipc import WaitComplete, producerFinished, shutdownMicroprocess
from Kamaelia.Chassis.Graphline import Graphline

class UidTagger(component):
    Inboxes = {'inbox': 'incoming items', 'control': 'shutdown signalling'}
    Outboxes = {'outbox': 'items tagged with uid', 'signal': 'shutdown signalling', 
       'uid': 'uid used for tagging, emitted at start'}

    def finished(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True

        return False

    def main(self):
        uid = self.name
        self.send(uid, 'uid')
        while not self.finished():
            while self.dataReady('inbox'):
                item = self.recv('inbox')
                self.send((uid, item), 'outbox')

            self.pause()
            yield 1


class FilterTag(component):
    Inboxes = {'inbox': 'incoming tagged items', 'control': 'shutdown signalling', 
       'uid': 'uid to filter'}
    Outboxes = {'outbox': 'items, not tagged with uid', 'signal': 'shutdown signalling'}

    def finished(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True

        return False

    def main(self):
        uid = object()
        while not self.finished():
            while self.dataReady('uid'):
                uid = self.recv('uid')

            while self.dataReady('inbox'):
                (ID, item) = self.recv('inbox')
                if not ID == uid:
                    self.send(item, 'outbox')

            self.pause()
            yield 1


class FilterButKeepTag(component):
    Inboxes = {'inbox': 'incoming tagged items', 'control': 'shutdown signalling', 
       'uid': 'uid to filter'}
    Outboxes = {'outbox': 'items, not tagged with uid', 'signal': 'shutdown signalling'}

    def finished(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            self.send(msg, 'signal')
            if isinstance(msg, (producerFinished, shutdownMicroprocess)):
                return True

        return False

    def main(self):
        uid = object()
        while not self.finished():
            while self.dataReady('uid'):
                uid = self.recv('uid')

            while self.dataReady('inbox'):
                (ID, item) = self.recv('inbox')
                if not ID == uid:
                    self.send((ID, item), 'outbox')

            self.pause()
            yield 1


def TagAndFilterWrapper(target, dontRemoveTag=False):
    """    Returns a component that wraps a target component, tagging all traffic
    coming from its outbox; and filtering outany traffic coming into its inbox
    with the same unique id.
    """
    if dontRemoveTag:
        Filter = FilterButKeepTag
    else:
        Filter = FilterTag
    return Graphline(TAGGER=UidTagger(), FILTER=Filter(), TARGET=target, linkages={('TARGET', 'outbox'): ('TAGGER', 'inbox'), 
       ('TAGGER', 'outbox'): ('self', 'outbox'), 
       ('TAGGER', 'uid'): ('FILTER', 'uid'), 
       ('self', 'inbox'): ('FILTER', 'inbox'), 
       ('FILTER', 'outbox'): ('TARGET', 'inbox'), 
       ('self', 'control'): ('TARGET', 'control'), 
       ('TARGET', 'signal'): ('TAGGER', 'control'), 
       ('TAGGER', 'signal'): ('FILTER', 'control'), 
       ('FILTER', 'signal'): ('self', 'signal')})


def FilterAndTagWrapper(target, dontRemoveTag=False):
    """    Returns a component that wraps a target component, tagging all traffic
    going into its inbox; and filtering outany traffic coming out of its outbox
    with the same unique id.
    """
    if dontRemoveTag:
        Filter = FilterButKeepTag
    else:
        Filter = FilterTag
    return Graphline(TAGGER=UidTagger(), FILTER=Filter(), TARGET=target, linkages={('TARGET', 'outbox'): ('FILTER', 'inbox'), 
       ('FILTER', 'outbox'): ('self', 'outbox'), 
       ('TAGGER', 'uid'): ('FILTER', 'uid'), 
       ('self', 'inbox'): ('TAGGER', 'inbox'), 
       ('TAGGER', 'outbox'): ('TARGET', 'inbox'), 
       ('self', 'control'): ('TARGET', 'control'), 
       ('TARGET', 'signal'): ('TAGGER', 'control'), 
       ('TAGGER', 'signal'): ('FILTER', 'control'), 
       ('FILTER', 'signal'): ('self', 'signal')})


def TagAndFilterWrapperKeepingTag(target):
    return TagAndFilterWrapper(target, dontRemoveTag=True)


def FilterAndTagWrapperKeepingTag(target):
    return FilterAndTagWrapper(target, dontRemoveTag=True)