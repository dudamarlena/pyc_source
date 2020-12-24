# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Grey/GreyListingPolicy.py
# Compiled at: 2008-10-19 12:19:52
"""========================================================
Greylisting Policy For/Subclass Of Concrete Mail Handler
========================================================

This component implements a greylisting SMTP proxy protocol, by subclassing
ConcreteMailHandler and overriding the appropriate methods (primarily the
shouldWeAcceptMail method).

For more detail, please see http://www.kamaelia.org/KamaeliaGrey

Example Usage
-------------

You use this as follows (at minimum)::

    ServerCore(protocol=GreyListingPolicy, port=25)

If you want to have a hardcoded/configured greylisting server you could do this::

    class GreyLister(ServerCore):
        class protocol(GreyListingPolicy):
            allowed_senders = []
            allowed_sender_nets = []
            allowed_domains = [ ]

    GreyLister(port=25)

How does it work?
-----------------

Primarily it override the method shouldWeAcceptMail, and implements the
following logic::

        if self.sentFromAllowedIPAddress():  return True # Allowed hosts can always send to anywhere through us
        if self.sentFromAllowedNetwork():    return True # People on truste networks can always do the same
        if self.sentToADomainWeForwardFor():
            try:
                for recipient in self.recipients:
                    if self.whiteListed(recipient):
                        return True
                    if not self.isGreylisted(recipient):
                        return False
            except Exception, e:
                pass
            return True # Anyone can always send to hosts we own

Clearly AllowedIPAddress, AllowedNetwork, whiteListed, and
DomainWeForwardFor are fairly clear concepts, so for more details on those
please look at the implementation. 

isGreylisted by comparison is slightly more complex. Fundamentally this
works on the basis of saying this:

 - have we seen the triple (ip, sender, recipient) before ?
 - if we have, then allow the message through
 - otherwise, defer the message

Now there is a little more subtlty here, based on the following conditions:

 - If greylisted, and not been there too long, allow through
 - If grey too long, refuse (restarting the greylisting for that combo)
 - If not seen this triplet before, defer and note triplet
 - If triplet retrying waaay too soon, reset their timer & defer
 - If triplet retrying too soon generally speaking just defer
 - If triplet hasn't been seen in aaaages, defer
 - Otherwise, allow through & greylist them
"""
import anydbm, math, time
from Kamaelia.Apps.Grey.ConcreteMailHandler import ConcreteMailHandler

class GreyListingPolicy(ConcreteMailHandler):
    allowed_senders = []
    allowed_sender_nets = []
    allowed_domains = []

    def sentFromAllowedIPAddress(self):
        if self.peer in self.allowed_senders:
            return True
        return False

    def sentFromAllowedNetwork(self):
        for network_prefix in self.allowed_sender_nets:
            if self.peer[:len(network_prefix)] == network_prefix:
                return True

        return False

    def sentToADomainWeForwardFor(self):
        for recipient in self.recipients:
            recipient = recipient.replace('<', '')
            recipient = recipient.replace('>', '')
            try:
                domain = recipient[recipient.find('@') + 1:]
                domain = domain.lower()
                if domain not in self.allowed_domains:
                    return False
            except:
                raise
                return False

        return True

    def isGreylisted(self, recipient):
        max_grey = 3000000
        too_soon = 180
        min_defer_time = 3600
        max_defer_time = 25000
        IP = self.peer
        sender = self.sender

        def _isGreylisted(greylist, seen, IP, sender, recipient):
            if greylist.get(triplet, None) is not None:
                greytime = float(greylist[triplet])
                if time.time() - greytime > max_grey:
                    del greylist[triplet]
                    try:
                        del seen[triplet]
                    except KeyError:
                        pass

                else:
                    greylist[triplet] = str(time.time())
                    return True
            if seen.get(triplet, None) is None:
                seen[triplet] = str(time.time())
                return False
            last_tried = float(seen[triplet])
            if time.time() - last_tried < too_soon:
                seen[triplet] = str(time.time())
                return False
            if time.time() - last_tried < min_defer_time:
                return False
            if time.time() - last_tried > max_defer_time:
                seen[triplet] = str(time.time())
                return False
            greylist[triplet] = str(time.time())
            return True

        greylist = anydbm.open('greylisted.dbm', 'c')
        seen = anydbm.open('attempters.dbm', 'c')
        triplet = repr((IP, sender, recipient))
        result = _isGreylisted(greylist, seen, IP, sender, recipient)
        seen.close()
        greylist.close()
        return result

    def whiteListed(self, recipient):
        for (IP, sender, r) in self.whitelisted_triples:
            if self.peer == IP:
                if self.sender == sender:
                    if recipient == r:
                        return True

        for (remotename, network_prefix, r) in self.whitelisted_nonstandard_triples:
            if remotename == self.remotename:
                if self.peer[:len(network_prefix)] == network_prefix:
                    if r == recipient:
                        return True

        return False

    def shouldWeAcceptMail(self):
        if self.sentFromAllowedIPAddress():
            return True
        if self.sentFromAllowedNetwork():
            return True
        if self.sentToADomainWeForwardFor():
            try:
                for recipient in self.recipients:
                    if self.whiteListed(recipient):
                        return True
                    if not self.isGreylisted(recipient):
                        return False

            except Exception, e:
                pass
            else:
                return True
        return False

    def logResult(self):

        def m(x, w=2):
            return '0' * (w - len(str(x))) + str(x)

        now = time.time()
        msec = int((now - math.floor(now)) * 1000)
        x = time.gmtime(now)
        stamp = ('').join([ str(z) for z in [m(x.tm_year, 4), m(x.tm_mon, 2), m(x.tm_mday, 2), m(x.tm_hour, 2), m(x.tm_min, 2), m(x.tm_sec, 2), '.', m(msec, 3)] ])
        logline = str(stamp) + ' | '
        logline += str(self.remotename) + ' | '
        logline += str(self.peer) + ' | '
        logline += str(self.sender) + ' | '
        logline += str((', ').join(self.recipients)) + ' | '
        logline += str(self.mailStatus) + ' | '
        self.noteToLog(logline)


__kamaelia_components__ = (
 GreyListingPolicy,)