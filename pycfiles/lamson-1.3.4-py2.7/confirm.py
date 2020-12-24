# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/lamson/confirm.py
# Compiled at: 2011-05-21 19:39:14
"""
Confirmation handling API that helps you get the whole confirm/pending/verify 
process correct.  It doesn't implement any handlers, but what it does do is
provide the logic for doing the following:

    * Take an email, put it in a "pending" queue, and then send out a confirm
    email with a strong random id.
    * Store the pending message ID and the random secret someplace for later
    verification.
    * Verify an incoming email against the expected ID, and get back the
    original.

You then just work this into your project's state flow, write your own
templates, and possibly write your own storage.
"""
import uuid
from lamson import queue, view
from email.utils import parseaddr

class ConfirmationStorage(object):
    """
    This is the basic confirmation storage.  For simple testing purposes
    you can just use the default hash db parameter.  If you do a deployment
    you can probably get away with a shelf hash instead.

    You can write your own version of this and use it.  The confirmation engine
    only cares that it gets something that supports all of these methods.
    """

    def __init__(self, db={}):
        """
        Change the db parameter to a shelf to get persistent storage.
        """
        self.confirmations = db

    def clear(self):
        """
        Used primarily in testing, this clears out all pending confirmations.
        """
        self.confirmations.clear()

    def key(self, target, from_address):
        """
        Used internally to construct a string key, if you write
        your own you don't need this.

        NOTE: To support proper equality and shelve storage, this encodes the
        key into ASCII.  Make a different subclass if you need unicode and your
        storage supports it.
        """
        key = target + ':' + from_address
        return key.encode('ascii')

    def get(self, target, from_address):
        """
        Given a target and a from address, this returns a tuple of (expected_secret, pending_message_id).
        If it doesn't find that target+from_address, then it should return a (None, None) tuple.
        """
        return self.confirmations.get(self.key(target, from_address), (None, None))

    def delete(self, target, from_address):
        """
        Removes a target+from_address from the storage.
        """
        try:
            del self.confirmations[self.key(target, from_address)]
        except KeyError:
            pass

    def store(self, target, from_address, expected_secret, pending_message_id):
        """
        Given a target, from_address it will store the expected_secret and pending_message_id
        of later verification.  The target should be a string indicating what is being
        confirmed.  Like "subscribe", "post", etc.

        When implementing your own you should *never* allow more than one target+from_address
        combination.
        """
        self.confirmations[self.key(target, from_address)] = (
         expected_secret,
         pending_message_id)


class ConfirmationEngine(object):
    """
    The confirmation engine is what does the work of sending a confirmation, 
    and verifying that it was confirmed properly.  In order to use it you
    have to construct the ConfirmationEngine (usually in config/settings.py) and
    you write your confirmation message templates for sending.

    The primary methods you use are ConfirmationEngine.send and ConfirmationEngine.verify.
    """

    def __init__(self, pending_queue, storage):
        """
        The pending_queue should be a string with the path to the lamson.queue.Queue 
        that will store pending messages.  These messages are the originals the user
        sent when they tried to confirm.

        Storage should be something that is like ConfirmationStorage so that this
        can store things for later verification.
        """
        self.pending = queue.Queue(pending_queue)
        self.storage = storage

    def get_pending(self, pending_id):
        """
        Returns the pending message for the given ID.
        """
        return self.pending.get(pending_id)

    def push_pending(self, message):
        """
        Puts a pending message into the pending queue.
        """
        return self.pending.push(message)

    def delete_pending(self, pending_id):
        """
        Removes the pending message from the pending queue.
        """
        self.pending.remove(pending_id)

    def cancel(self, target, from_address, expect_secret):
        """
        Used to cancel a pending confirmation.
        """
        name, addr = parseaddr(from_address)
        secret, pending_id = self.storage.get(target, addr)
        if secret == expect_secret:
            self.storage.delete(target, addr)
            self.delete_pending(pending_id)

    def make_random_secret(self):
        """
        Generates a random uuid as the secret, in hex form.
        """
        return uuid.uuid4().hex

    def register(self, target, message):
        """
        Don't call this directly unless you know what you are doing.
        It does the job of registering the original message and the
        expected confirmation into the storage.
        """
        from_address = message.route_from
        pending_id = self.push_pending(message)
        secret = self.make_random_secret()
        self.storage.store(target, from_address, secret, pending_id)
        return '%s-confirm-%s' % (target, secret)

    def verify--- This code section failed: ---

 L. 167         0  LOAD_FAST             3  'expect_secret'
                3  POP_JUMP_IF_TRUE     15  'to 15'
                6  LOAD_ASSERT              AssertionError
                9  LOAD_CONST               'Must give an expected ID number.'
               12  RAISE_VARARGS_2       2  None

 L. 168        15  LOAD_GLOBAL           1  'parseaddr'
               18  LOAD_FAST             2  'from_address'
               21  CALL_FUNCTION_1       1  None
               24  UNPACK_SEQUENCE_2     2 
               27  STORE_FAST            4  'name'
               30  STORE_FAST            5  'addr'

 L. 170        33  LOAD_FAST             0  'self'
               36  LOAD_ATTR             2  'storage'
               39  LOAD_ATTR             3  'get'
               42  LOAD_FAST             1  'target'
               45  LOAD_FAST             5  'addr'
               48  CALL_FUNCTION_2       2  None
               51  UNPACK_SEQUENCE_2     2 
               54  STORE_FAST            6  'secret'
               57  STORE_FAST            7  'pending_id'

 L. 172        60  LOAD_FAST             6  'secret'
               63  LOAD_FAST             3  'expect_secret'
               66  COMPARE_OP            2  ==
               69  POP_JUMP_IF_FALSE   104  'to 104'

 L. 173        72  LOAD_FAST             0  'self'
               75  LOAD_ATTR             2  'storage'
               78  LOAD_ATTR             4  'delete'
               81  LOAD_FAST             1  'target'
               84  LOAD_FAST             5  'addr'
               87  CALL_FUNCTION_2       2  None
               90  POP_TOP          

 L. 174        91  LOAD_FAST             0  'self'
               94  LOAD_ATTR             5  'get_pending'
               97  LOAD_FAST             7  'pending_id'
              100  CALL_FUNCTION_1       1  None
              103  RETURN_END_IF    
            104_0  COME_FROM            69  '69'

 L. 176       104  LOAD_CONST               None
              107  RETURN_VALUE     
              108  LOAD_CONST               None
              111  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 108

    def send(self, relay, target, message, template, vars):
        """
        This is the method you should use to send out confirmation messages.
        You give it the relay, a target (i.e. "subscribe"), the message they
        sent requesting the confirm, your confirmation template, and any
        vars that template needs.

        The result of calling this is that the template message gets sent through
        the relay, the original message is stored in the pending queue, and 
        data is put into the storage for later calls to verify.
        """
        confirm_address = self.register(target, message)
        vars.update(locals())
        msg = view.respond(vars, template, To=message['from'], From='%(confirm_address)s@%(host)s', Subject='Confirmation required')
        msg['Reply-To'] = '%(confirm_address)s@%(host)s' % vars
        relay.deliver(msg)

    def clear(self):
        """
        Used in testing to make sure there's nothing in the pending
        queue or storage.
        """
        self.pending.clear()
        self.storage.clear()