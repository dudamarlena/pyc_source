# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jiangyuanshu/thrift4p/thrift4p/gen-py/im_chat_logic_service/ImChatLogicService.py
# Compiled at: 2018-11-20 03:04:26
from thrift.Thrift import TType, TMessageType, TException, TApplicationException
import logging
from ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
    from thrift.protocol import fastbinary
except:
    fastbinary = None

class Iface():

    def send(self, sender, receiver, message):
        """
    Parameters:
     - sender
     - receiver
     - message
    """
        pass

    def send4Comet(self, sender, receiver, message):
        """
    Parameters:
     - sender
     - receiver
     - message
    """
        pass

    def sync(self, cid, sid, syncKey):
        """
    Parameters:
     - cid
     - sid
     - syncKey
    """
        pass

    def syncFin(self, cid, sid, syncKey):
        """
    Parameters:
     - cid
     - sid
     - syncKey
    """
        pass

    def subscribe(self, cid1, cid2):
        """
    Parameters:
     - cid1
     - cid2
    """
        pass

    def subscribeByPlat(self, cid1, cid2, exp, platType):
        """
    Parameters:
     - cid1
     - cid2
     - exp
     - platType
    """
        pass

    def subscribeExp(self, cid1, cid2, exp):
        """
    Parameters:
     - cid1
     - cid2
     - exp
    """
        pass

    def unSubscribe(self, cid1, cid2):
        """
    Parameters:
     - cid1
     - cid2
    """
        pass

    def loadNotifies(self, cid):
        """
    Parameters:
     - cid
    """
        pass

    def deleteTempRelation(self, cid1, cid2):
        """
    Parameters:
     - cid1
     - cid2
    """
        pass

    def sendUser(self, sender, receiver, message):
        """
    Parameters:
     - sender
     - receiver
     - message
    """
        pass

    def subscribeUser(self, sender, receiver):
        """
    Parameters:
     - sender
     - receiver
    """
        pass

    def subscribeUserExp(self, sender, receiver, exp):
        """
    Parameters:
     - sender
     - receiver
     - exp
    """
        pass

    def unSubscribeUser(self, user1, user2):
        """
    Parameters:
     - user1
     - user2
    """
        pass

    def deleteUserTempRelation(self, user1, user2):
        """
    Parameters:
     - user1
     - user2
    """
        pass

    def rsend(self, sender, receiver, syncKey):
        """
    Parameters:
     - sender
     - receiver
     - syncKey
    """
        pass

    def rsync(self, sender, receiver, syncKey):
        """
    Parameters:
     - sender
     - receiver
     - syncKey
    """
        pass

    def rsyncFin(self, sender, receiver, syncKey):
        """
    Parameters:
     - sender
     - receiver
     - syncKey
    """
        pass

    def hasUnread(self, sender, receiver):
        """
    Parameters:
     - sender
     - receiver
    """
        pass


class Client(Iface):

    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0
        return

    def send(self, sender, receiver, message):
        """
    Parameters:
     - sender
     - receiver
     - message
    """
        self.send_send(sender, receiver, message)
        self.recv_send()

    def send_send(self, sender, receiver, message):
        self._oprot.writeMessageBegin('send', TMessageType.CALL, self._seqid)
        args = send_args()
        args.sender = sender
        args.receiver = receiver
        args.message = message
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_send(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = send_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def send4Comet(self, sender, receiver, message):
        """
    Parameters:
     - sender
     - receiver
     - message
    """
        self.send_send4Comet(sender, receiver, message)
        return self.recv_send4Comet()

    def send_send4Comet(self, sender, receiver, message):
        self._oprot.writeMessageBegin('send4Comet', TMessageType.CALL, self._seqid)
        args = send4Comet_args()
        args.sender = sender
        args.receiver = receiver
        args.message = message
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_send4Comet(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = send4Comet_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        else:
            if result.e is not None:
                raise result.e
            raise TApplicationException(TApplicationException.MISSING_RESULT, 'send4Comet failed: unknown result')
            return

    def sync(self, cid, sid, syncKey):
        """
    Parameters:
     - cid
     - sid
     - syncKey
    """
        self.send_sync(cid, sid, syncKey)
        return self.recv_sync()

    def send_sync(self, cid, sid, syncKey):
        self._oprot.writeMessageBegin('sync', TMessageType.CALL, self._seqid)
        args = sync_args()
        args.cid = cid
        args.sid = sid
        args.syncKey = syncKey
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_sync(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = sync_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        else:
            if result.e is not None:
                raise result.e
            raise TApplicationException(TApplicationException.MISSING_RESULT, 'sync failed: unknown result')
            return

    def syncFin(self, cid, sid, syncKey):
        """
    Parameters:
     - cid
     - sid
     - syncKey
    """
        self.send_syncFin(cid, sid, syncKey)
        self.recv_syncFin()

    def send_syncFin(self, cid, sid, syncKey):
        self._oprot.writeMessageBegin('syncFin', TMessageType.CALL, self._seqid)
        args = syncFin_args()
        args.cid = cid
        args.sid = sid
        args.syncKey = syncKey
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_syncFin(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = syncFin_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def subscribe(self, cid1, cid2):
        """
    Parameters:
     - cid1
     - cid2
    """
        self.send_subscribe(cid1, cid2)
        self.recv_subscribe()

    def send_subscribe(self, cid1, cid2):
        self._oprot.writeMessageBegin('subscribe', TMessageType.CALL, self._seqid)
        args = subscribe_args()
        args.cid1 = cid1
        args.cid2 = cid2
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_subscribe(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = subscribe_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def subscribeByPlat(self, cid1, cid2, exp, platType):
        """
    Parameters:
     - cid1
     - cid2
     - exp
     - platType
    """
        self.send_subscribeByPlat(cid1, cid2, exp, platType)
        self.recv_subscribeByPlat()

    def send_subscribeByPlat(self, cid1, cid2, exp, platType):
        self._oprot.writeMessageBegin('subscribeByPlat', TMessageType.CALL, self._seqid)
        args = subscribeByPlat_args()
        args.cid1 = cid1
        args.cid2 = cid2
        args.exp = exp
        args.platType = platType
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_subscribeByPlat(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = subscribeByPlat_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def subscribeExp(self, cid1, cid2, exp):
        """
    Parameters:
     - cid1
     - cid2
     - exp
    """
        self.send_subscribeExp(cid1, cid2, exp)
        self.recv_subscribeExp()

    def send_subscribeExp(self, cid1, cid2, exp):
        self._oprot.writeMessageBegin('subscribeExp', TMessageType.CALL, self._seqid)
        args = subscribeExp_args()
        args.cid1 = cid1
        args.cid2 = cid2
        args.exp = exp
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_subscribeExp(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = subscribeExp_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def unSubscribe(self, cid1, cid2):
        """
    Parameters:
     - cid1
     - cid2
    """
        self.send_unSubscribe(cid1, cid2)
        self.recv_unSubscribe()

    def send_unSubscribe(self, cid1, cid2):
        self._oprot.writeMessageBegin('unSubscribe', TMessageType.CALL, self._seqid)
        args = unSubscribe_args()
        args.cid1 = cid1
        args.cid2 = cid2
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_unSubscribe(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = unSubscribe_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def loadNotifies(self, cid):
        """
    Parameters:
     - cid
    """
        self.send_loadNotifies(cid)
        self.recv_loadNotifies()

    def send_loadNotifies(self, cid):
        self._oprot.writeMessageBegin('loadNotifies', TMessageType.CALL, self._seqid)
        args = loadNotifies_args()
        args.cid = cid
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_loadNotifies(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = loadNotifies_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def deleteTempRelation(self, cid1, cid2):
        """
    Parameters:
     - cid1
     - cid2
    """
        self.send_deleteTempRelation(cid1, cid2)
        self.recv_deleteTempRelation()

    def send_deleteTempRelation(self, cid1, cid2):
        self._oprot.writeMessageBegin('deleteTempRelation', TMessageType.CALL, self._seqid)
        args = deleteTempRelation_args()
        args.cid1 = cid1
        args.cid2 = cid2
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_deleteTempRelation(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = deleteTempRelation_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def sendUser(self, sender, receiver, message):
        """
    Parameters:
     - sender
     - receiver
     - message
    """
        self.send_sendUser(sender, receiver, message)
        self.recv_sendUser()

    def send_sendUser(self, sender, receiver, message):
        self._oprot.writeMessageBegin('sendUser', TMessageType.CALL, self._seqid)
        args = sendUser_args()
        args.sender = sender
        args.receiver = receiver
        args.message = message
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_sendUser(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = sendUser_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def subscribeUser(self, sender, receiver):
        """
    Parameters:
     - sender
     - receiver
    """
        self.send_subscribeUser(sender, receiver)
        self.recv_subscribeUser()

    def send_subscribeUser(self, sender, receiver):
        self._oprot.writeMessageBegin('subscribeUser', TMessageType.CALL, self._seqid)
        args = subscribeUser_args()
        args.sender = sender
        args.receiver = receiver
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_subscribeUser(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = subscribeUser_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def subscribeUserExp(self, sender, receiver, exp):
        """
    Parameters:
     - sender
     - receiver
     - exp
    """
        self.send_subscribeUserExp(sender, receiver, exp)
        self.recv_subscribeUserExp()

    def send_subscribeUserExp(self, sender, receiver, exp):
        self._oprot.writeMessageBegin('subscribeUserExp', TMessageType.CALL, self._seqid)
        args = subscribeUserExp_args()
        args.sender = sender
        args.receiver = receiver
        args.exp = exp
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_subscribeUserExp(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = subscribeUserExp_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def unSubscribeUser(self, user1, user2):
        """
    Parameters:
     - user1
     - user2
    """
        self.send_unSubscribeUser(user1, user2)
        self.recv_unSubscribeUser()

    def send_unSubscribeUser(self, user1, user2):
        self._oprot.writeMessageBegin('unSubscribeUser', TMessageType.CALL, self._seqid)
        args = unSubscribeUser_args()
        args.user1 = user1
        args.user2 = user2
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_unSubscribeUser(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = unSubscribeUser_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def deleteUserTempRelation(self, user1, user2):
        """
    Parameters:
     - user1
     - user2
    """
        self.send_deleteUserTempRelation(user1, user2)
        self.recv_deleteUserTempRelation()

    def send_deleteUserTempRelation(self, user1, user2):
        self._oprot.writeMessageBegin('deleteUserTempRelation', TMessageType.CALL, self._seqid)
        args = deleteUserTempRelation_args()
        args.user1 = user1
        args.user2 = user2
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_deleteUserTempRelation(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = deleteUserTempRelation_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def rsend(self, sender, receiver, syncKey):
        """
    Parameters:
     - sender
     - receiver
     - syncKey
    """
        self.send_rsend(sender, receiver, syncKey)
        self.recv_rsend()

    def send_rsend(self, sender, receiver, syncKey):
        self._oprot.writeMessageBegin('rsend', TMessageType.CALL, self._seqid)
        args = rsend_args()
        args.sender = sender
        args.receiver = receiver
        args.syncKey = syncKey
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_rsend(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = rsend_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def rsync(self, sender, receiver, syncKey):
        """
    Parameters:
     - sender
     - receiver
     - syncKey
    """
        self.send_rsync(sender, receiver, syncKey)
        return self.recv_rsync()

    def send_rsync(self, sender, receiver, syncKey):
        self._oprot.writeMessageBegin('rsync', TMessageType.CALL, self._seqid)
        args = rsync_args()
        args.sender = sender
        args.receiver = receiver
        args.syncKey = syncKey
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_rsync(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = rsync_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        else:
            if result.e is not None:
                raise result.e
            raise TApplicationException(TApplicationException.MISSING_RESULT, 'rsync failed: unknown result')
            return

    def rsyncFin(self, sender, receiver, syncKey):
        """
    Parameters:
     - sender
     - receiver
     - syncKey
    """
        self.send_rsyncFin(sender, receiver, syncKey)
        self.recv_rsyncFin()

    def send_rsyncFin(self, sender, receiver, syncKey):
        self._oprot.writeMessageBegin('rsyncFin', TMessageType.CALL, self._seqid)
        args = rsyncFin_args()
        args.sender = sender
        args.receiver = receiver
        args.syncKey = syncKey
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_rsyncFin(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = rsyncFin_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.e is not None:
            raise result.e
        return

    def hasUnread(self, sender, receiver):
        """
    Parameters:
     - sender
     - receiver
    """
        self.send_hasUnread(sender, receiver)
        return self.recv_hasUnread()

    def send_hasUnread(self, sender, receiver):
        self._oprot.writeMessageBegin('hasUnread', TMessageType.CALL, self._seqid)
        args = hasUnread_args()
        args.sender = sender
        args.receiver = receiver
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_hasUnread(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = hasUnread_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        else:
            if result.e is not None:
                raise result.e
            raise TApplicationException(TApplicationException.MISSING_RESULT, 'hasUnread failed: unknown result')
            return


class Processor(Iface, TProcessor):

    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap['send'] = Processor.process_send
        self._processMap['send4Comet'] = Processor.process_send4Comet
        self._processMap['sync'] = Processor.process_sync
        self._processMap['syncFin'] = Processor.process_syncFin
        self._processMap['subscribe'] = Processor.process_subscribe
        self._processMap['subscribeByPlat'] = Processor.process_subscribeByPlat
        self._processMap['subscribeExp'] = Processor.process_subscribeExp
        self._processMap['unSubscribe'] = Processor.process_unSubscribe
        self._processMap['loadNotifies'] = Processor.process_loadNotifies
        self._processMap['deleteTempRelation'] = Processor.process_deleteTempRelation
        self._processMap['sendUser'] = Processor.process_sendUser
        self._processMap['subscribeUser'] = Processor.process_subscribeUser
        self._processMap['subscribeUserExp'] = Processor.process_subscribeUserExp
        self._processMap['unSubscribeUser'] = Processor.process_unSubscribeUser
        self._processMap['deleteUserTempRelation'] = Processor.process_deleteUserTempRelation
        self._processMap['rsend'] = Processor.process_rsend
        self._processMap['rsync'] = Processor.process_rsync
        self._processMap['rsyncFin'] = Processor.process_rsyncFin
        self._processMap['hasUnread'] = Processor.process_hasUnread

    def process(self, iprot, oprot):
        name, type, seqid = iprot.readMessageBegin()
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % name)
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_send(self, seqid, iprot, oprot):
        args = send_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = send_result()
        try:
            self._handler.send(args.sender, args.receiver, args.message)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('send', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_send4Comet(self, seqid, iprot, oprot):
        args = send4Comet_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = send4Comet_result()
        try:
            result.success = self._handler.send4Comet(args.sender, args.receiver, args.message)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('send4Comet', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_sync(self, seqid, iprot, oprot):
        args = sync_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = sync_result()
        try:
            result.success = self._handler.sync(args.cid, args.sid, args.syncKey)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('sync', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_syncFin(self, seqid, iprot, oprot):
        args = syncFin_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = syncFin_result()
        try:
            self._handler.syncFin(args.cid, args.sid, args.syncKey)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('syncFin', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_subscribe(self, seqid, iprot, oprot):
        args = subscribe_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = subscribe_result()
        try:
            self._handler.subscribe(args.cid1, args.cid2)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('subscribe', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_subscribeByPlat(self, seqid, iprot, oprot):
        args = subscribeByPlat_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = subscribeByPlat_result()
        try:
            self._handler.subscribeByPlat(args.cid1, args.cid2, args.exp, args.platType)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('subscribeByPlat', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_subscribeExp(self, seqid, iprot, oprot):
        args = subscribeExp_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = subscribeExp_result()
        try:
            self._handler.subscribeExp(args.cid1, args.cid2, args.exp)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('subscribeExp', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_unSubscribe(self, seqid, iprot, oprot):
        args = unSubscribe_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = unSubscribe_result()
        try:
            self._handler.unSubscribe(args.cid1, args.cid2)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('unSubscribe', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_loadNotifies(self, seqid, iprot, oprot):
        args = loadNotifies_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = loadNotifies_result()
        try:
            self._handler.loadNotifies(args.cid)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('loadNotifies', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_deleteTempRelation(self, seqid, iprot, oprot):
        args = deleteTempRelation_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = deleteTempRelation_result()
        try:
            self._handler.deleteTempRelation(args.cid1, args.cid2)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('deleteTempRelation', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_sendUser(self, seqid, iprot, oprot):
        args = sendUser_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = sendUser_result()
        try:
            self._handler.sendUser(args.sender, args.receiver, args.message)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('sendUser', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_subscribeUser(self, seqid, iprot, oprot):
        args = subscribeUser_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = subscribeUser_result()
        try:
            self._handler.subscribeUser(args.sender, args.receiver)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('subscribeUser', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_subscribeUserExp(self, seqid, iprot, oprot):
        args = subscribeUserExp_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = subscribeUserExp_result()
        try:
            self._handler.subscribeUserExp(args.sender, args.receiver, args.exp)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('subscribeUserExp', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_unSubscribeUser(self, seqid, iprot, oprot):
        args = unSubscribeUser_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = unSubscribeUser_result()
        try:
            self._handler.unSubscribeUser(args.user1, args.user2)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('unSubscribeUser', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_deleteUserTempRelation(self, seqid, iprot, oprot):
        args = deleteUserTempRelation_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = deleteUserTempRelation_result()
        try:
            self._handler.deleteUserTempRelation(args.user1, args.user2)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('deleteUserTempRelation', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_rsend(self, seqid, iprot, oprot):
        args = rsend_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = rsend_result()
        try:
            self._handler.rsend(args.sender, args.receiver, args.syncKey)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('rsend', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_rsync(self, seqid, iprot, oprot):
        args = rsync_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = rsync_result()
        try:
            result.success = self._handler.rsync(args.sender, args.receiver, args.syncKey)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('rsync', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_rsyncFin(self, seqid, iprot, oprot):
        args = rsyncFin_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = rsyncFin_result()
        try:
            self._handler.rsyncFin(args.sender, args.receiver, args.syncKey)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('rsyncFin', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_hasUnread(self, seqid, iprot, oprot):
        args = hasUnread_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = hasUnread_result()
        try:
            result.success = self._handler.hasUnread(args.sender, args.receiver)
            msg_type = TMessageType.REPLY
        except (TTransport.TTransportException, KeyboardInterrupt, SystemExit):
            raise
        except ChatLogicException as e:
            msg_type = TMessageType.REPLY
            result.e = e
        except Exception as ex:
            msg_type = TMessageType.EXCEPTION
            logging.exception(ex)
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('hasUnread', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()


class send_args():
    """
  Attributes:
   - sender
   - receiver
   - message
  """
    thrift_spec = (
     None,
     (
      1, TType.STRING, 'sender', None, None),
     (
      2, TType.STRING, 'receiver', None, None),
     (
      3, TType.STRUCT, 'message', (ChatMessage, ChatMessage.thrift_spec), None))

    def __init__(self, sender=None, receiver=None, message=None):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRING:
                        self.sender = iprot.readString()
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRING:
                        self.receiver = iprot.readString()
                    else:
                        iprot.skip(ftype)
                elif fid == 3:
                    if ftype == TType.STRUCT:
                        self.message = ChatMessage()
                        self.message.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('send_args')
            if self.sender is not None:
                oprot.writeFieldBegin('sender', TType.STRING, 1)
                oprot.writeString(self.sender)
                oprot.writeFieldEnd()
            if self.receiver is not None:
                oprot.writeFieldBegin('receiver', TType.STRING, 2)
                oprot.writeString(self.receiver)
                oprot.writeFieldEnd()
            if self.message is not None:
                oprot.writeFieldBegin('message', TType.STRUCT, 3)
                self.message.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.sender)
        value = value * 31 ^ hash(self.receiver)
        value = value * 31 ^ hash(self.message)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class send_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('send_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class send4Comet_args():
    """
  Attributes:
   - sender
   - receiver
   - message
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'sender', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'receiver', (User, User.thrift_spec), None),
     (
      3, TType.STRUCT, 'message', (ChatMessage, ChatMessage.thrift_spec), None))

    def __init__(self, sender=None, receiver=None, message=None):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.sender = User()
                        self.sender.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRUCT:
                        self.receiver = User()
                        self.receiver.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 3:
                    if ftype == TType.STRUCT:
                        self.message = ChatMessage()
                        self.message.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('send4Comet_args')
            if self.sender is not None:
                oprot.writeFieldBegin('sender', TType.STRUCT, 1)
                self.sender.write(oprot)
                oprot.writeFieldEnd()
            if self.receiver is not None:
                oprot.writeFieldBegin('receiver', TType.STRUCT, 2)
                self.receiver.write(oprot)
                oprot.writeFieldEnd()
            if self.message is not None:
                oprot.writeFieldBegin('message', TType.STRUCT, 3)
                self.message.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.sender)
        value = value * 31 ^ hash(self.receiver)
        value = value * 31 ^ hash(self.message)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class send4Comet_result():
    """
  Attributes:
   - success
   - e
  """
    thrift_spec = (
     (
      0, TType.I64, 'success', None, None),
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 0:
                    if ftype == TType.I64:
                        self.success = iprot.readI64()
                    else:
                        iprot.skip(ftype)
                elif fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('send4Comet_result')
            if self.success is not None:
                oprot.writeFieldBegin('success', TType.I64, 0)
                oprot.writeI64(self.success)
                oprot.writeFieldEnd()
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.success)
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class sync_args():
    """
  Attributes:
   - cid
   - sid
   - syncKey
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'cid', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'sid', (User, User.thrift_spec), None),
     (
      3, TType.I64, 'syncKey', None, None))

    def __init__(self, cid=None, sid=None, syncKey=None):
        self.cid = cid
        self.sid = sid
        self.syncKey = syncKey

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.cid = User()
                    self.cid.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.sid = User()
                    self.sid.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.syncKey = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()
        return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('sync_args')
            if self.cid is not None:
                oprot.writeFieldBegin('cid', TType.STRUCT, 1)
                self.cid.write(oprot)
                oprot.writeFieldEnd()
            if self.sid is not None:
                oprot.writeFieldBegin('sid', TType.STRUCT, 2)
                self.sid.write(oprot)
                oprot.writeFieldEnd()
            if self.syncKey is not None:
                oprot.writeFieldBegin('syncKey', TType.I64, 3)
                oprot.writeI64(self.syncKey)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.cid)
        value = value * 31 ^ hash(self.sid)
        value = value * 31 ^ hash(self.syncKey)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class sync_result():
    """
  Attributes:
   - success
   - e
  """
    thrift_spec = (
     (
      0, TType.STRUCT, 'success', (ChatSyncRet, ChatSyncRet.thrift_spec), None),
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 0:
                    if ftype == TType.STRUCT:
                        self.success = ChatSyncRet()
                        self.success.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('sync_result')
            if self.success is not None:
                oprot.writeFieldBegin('success', TType.STRUCT, 0)
                self.success.write(oprot)
                oprot.writeFieldEnd()
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.success)
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class syncFin_args():
    """
  Attributes:
   - cid
   - sid
   - syncKey
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'cid', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'sid', (User, User.thrift_spec), None),
     (
      3, TType.I64, 'syncKey', None, None))

    def __init__(self, cid=None, sid=None, syncKey=None):
        self.cid = cid
        self.sid = sid
        self.syncKey = syncKey

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.cid = User()
                    self.cid.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.sid = User()
                    self.sid.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.syncKey = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()
        return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('syncFin_args')
            if self.cid is not None:
                oprot.writeFieldBegin('cid', TType.STRUCT, 1)
                self.cid.write(oprot)
                oprot.writeFieldEnd()
            if self.sid is not None:
                oprot.writeFieldBegin('sid', TType.STRUCT, 2)
                self.sid.write(oprot)
                oprot.writeFieldEnd()
            if self.syncKey is not None:
                oprot.writeFieldBegin('syncKey', TType.I64, 3)
                oprot.writeI64(self.syncKey)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.cid)
        value = value * 31 ^ hash(self.sid)
        value = value * 31 ^ hash(self.syncKey)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class syncFin_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('syncFin_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribe_args():
    """
  Attributes:
   - cid1
   - cid2
  """
    thrift_spec = (
     None,
     (
      1, TType.STRING, 'cid1', None, None),
     (
      2, TType.STRING, 'cid2', None, None))

    def __init__(self, cid1=None, cid2=None):
        self.cid1 = cid1
        self.cid2 = cid2

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRING:
                        self.cid1 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRING:
                        self.cid2 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribe_args')
            if self.cid1 is not None:
                oprot.writeFieldBegin('cid1', TType.STRING, 1)
                oprot.writeString(self.cid1)
                oprot.writeFieldEnd()
            if self.cid2 is not None:
                oprot.writeFieldBegin('cid2', TType.STRING, 2)
                oprot.writeString(self.cid2)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.cid1)
        value = value * 31 ^ hash(self.cid2)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribe_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribe_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribeByPlat_args():
    """
  Attributes:
   - cid1
   - cid2
   - exp
   - platType
  """
    thrift_spec = (
     None,
     (
      1, TType.STRING, 'cid1', None, None),
     (
      2, TType.STRING, 'cid2', None, None),
     (
      3, TType.I32, 'exp', None, None),
     (
      4, TType.I32, 'platType', None, None))

    def __init__(self, cid1=None, cid2=None, exp=None, platType=None):
        self.cid1 = cid1
        self.cid2 = cid2
        self.exp = exp
        self.platType = platType

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRING:
                        self.cid1 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRING:
                        self.cid2 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                elif fid == 3:
                    if ftype == TType.I32:
                        self.exp = iprot.readI32()
                    else:
                        iprot.skip(ftype)
                elif fid == 4:
                    if ftype == TType.I32:
                        self.platType = iprot.readI32()
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribeByPlat_args')
            if self.cid1 is not None:
                oprot.writeFieldBegin('cid1', TType.STRING, 1)
                oprot.writeString(self.cid1)
                oprot.writeFieldEnd()
            if self.cid2 is not None:
                oprot.writeFieldBegin('cid2', TType.STRING, 2)
                oprot.writeString(self.cid2)
                oprot.writeFieldEnd()
            if self.exp is not None:
                oprot.writeFieldBegin('exp', TType.I32, 3)
                oprot.writeI32(self.exp)
                oprot.writeFieldEnd()
            if self.platType is not None:
                oprot.writeFieldBegin('platType', TType.I32, 4)
                oprot.writeI32(self.platType)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.cid1)
        value = value * 31 ^ hash(self.cid2)
        value = value * 31 ^ hash(self.exp)
        value = value * 31 ^ hash(self.platType)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribeByPlat_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribeByPlat_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribeExp_args():
    """
  Attributes:
   - cid1
   - cid2
   - exp
  """
    thrift_spec = (
     None,
     (
      1, TType.STRING, 'cid1', None, None),
     (
      2, TType.STRING, 'cid2', None, None),
     (
      3, TType.I32, 'exp', None, None))

    def __init__(self, cid1=None, cid2=None, exp=None):
        self.cid1 = cid1
        self.cid2 = cid2
        self.exp = exp

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRING:
                        self.cid1 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRING:
                        self.cid2 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                elif fid == 3:
                    if ftype == TType.I32:
                        self.exp = iprot.readI32()
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribeExp_args')
            if self.cid1 is not None:
                oprot.writeFieldBegin('cid1', TType.STRING, 1)
                oprot.writeString(self.cid1)
                oprot.writeFieldEnd()
            if self.cid2 is not None:
                oprot.writeFieldBegin('cid2', TType.STRING, 2)
                oprot.writeString(self.cid2)
                oprot.writeFieldEnd()
            if self.exp is not None:
                oprot.writeFieldBegin('exp', TType.I32, 3)
                oprot.writeI32(self.exp)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.cid1)
        value = value * 31 ^ hash(self.cid2)
        value = value * 31 ^ hash(self.exp)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribeExp_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribeExp_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class unSubscribe_args():
    """
  Attributes:
   - cid1
   - cid2
  """
    thrift_spec = (
     None,
     (
      1, TType.STRING, 'cid1', None, None),
     (
      2, TType.STRING, 'cid2', None, None))

    def __init__(self, cid1=None, cid2=None):
        self.cid1 = cid1
        self.cid2 = cid2

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRING:
                        self.cid1 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRING:
                        self.cid2 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('unSubscribe_args')
            if self.cid1 is not None:
                oprot.writeFieldBegin('cid1', TType.STRING, 1)
                oprot.writeString(self.cid1)
                oprot.writeFieldEnd()
            if self.cid2 is not None:
                oprot.writeFieldBegin('cid2', TType.STRING, 2)
                oprot.writeString(self.cid2)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.cid1)
        value = value * 31 ^ hash(self.cid2)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class unSubscribe_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('unSubscribe_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class loadNotifies_args():
    """
  Attributes:
   - cid
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'cid', (User, User.thrift_spec), None))

    def __init__(self, cid=None):
        self.cid = cid

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.cid = User()
                        self.cid.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('loadNotifies_args')
            if self.cid is not None:
                oprot.writeFieldBegin('cid', TType.STRUCT, 1)
                self.cid.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.cid)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class loadNotifies_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('loadNotifies_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class deleteTempRelation_args():
    """
  Attributes:
   - cid1
   - cid2
  """
    thrift_spec = (
     None,
     (
      1, TType.STRING, 'cid1', None, None),
     (
      2, TType.STRING, 'cid2', None, None))

    def __init__(self, cid1=None, cid2=None):
        self.cid1 = cid1
        self.cid2 = cid2

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRING:
                        self.cid1 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRING:
                        self.cid2 = iprot.readString()
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('deleteTempRelation_args')
            if self.cid1 is not None:
                oprot.writeFieldBegin('cid1', TType.STRING, 1)
                oprot.writeString(self.cid1)
                oprot.writeFieldEnd()
            if self.cid2 is not None:
                oprot.writeFieldBegin('cid2', TType.STRING, 2)
                oprot.writeString(self.cid2)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.cid1)
        value = value * 31 ^ hash(self.cid2)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class deleteTempRelation_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('deleteTempRelation_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class sendUser_args():
    """
  Attributes:
   - sender
   - receiver
   - message
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'sender', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'receiver', (User, User.thrift_spec), None),
     (
      3, TType.STRUCT, 'message', (ChatMessage, ChatMessage.thrift_spec), None))

    def __init__(self, sender=None, receiver=None, message=None):
        self.sender = sender
        self.receiver = receiver
        self.message = message

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.sender = User()
                        self.sender.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRUCT:
                        self.receiver = User()
                        self.receiver.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 3:
                    if ftype == TType.STRUCT:
                        self.message = ChatMessage()
                        self.message.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('sendUser_args')
            if self.sender is not None:
                oprot.writeFieldBegin('sender', TType.STRUCT, 1)
                self.sender.write(oprot)
                oprot.writeFieldEnd()
            if self.receiver is not None:
                oprot.writeFieldBegin('receiver', TType.STRUCT, 2)
                self.receiver.write(oprot)
                oprot.writeFieldEnd()
            if self.message is not None:
                oprot.writeFieldBegin('message', TType.STRUCT, 3)
                self.message.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.sender)
        value = value * 31 ^ hash(self.receiver)
        value = value * 31 ^ hash(self.message)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class sendUser_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('sendUser_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribeUser_args():
    """
  Attributes:
   - sender
   - receiver
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'sender', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'receiver', (User, User.thrift_spec), None))

    def __init__(self, sender=None, receiver=None):
        self.sender = sender
        self.receiver = receiver

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.sender = User()
                        self.sender.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRUCT:
                        self.receiver = User()
                        self.receiver.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribeUser_args')
            if self.sender is not None:
                oprot.writeFieldBegin('sender', TType.STRUCT, 1)
                self.sender.write(oprot)
                oprot.writeFieldEnd()
            if self.receiver is not None:
                oprot.writeFieldBegin('receiver', TType.STRUCT, 2)
                self.receiver.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.sender)
        value = value * 31 ^ hash(self.receiver)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribeUser_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribeUser_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribeUserExp_args():
    """
  Attributes:
   - sender
   - receiver
   - exp
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'sender', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'receiver', (User, User.thrift_spec), None),
     (
      3, TType.I32, 'exp', None, None))

    def __init__(self, sender=None, receiver=None, exp=None):
        self.sender = sender
        self.receiver = receiver
        self.exp = exp

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.sender = User()
                    self.sender.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.receiver = User()
                    self.receiver.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.exp = iprot.readI32()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()
        return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribeUserExp_args')
            if self.sender is not None:
                oprot.writeFieldBegin('sender', TType.STRUCT, 1)
                self.sender.write(oprot)
                oprot.writeFieldEnd()
            if self.receiver is not None:
                oprot.writeFieldBegin('receiver', TType.STRUCT, 2)
                self.receiver.write(oprot)
                oprot.writeFieldEnd()
            if self.exp is not None:
                oprot.writeFieldBegin('exp', TType.I32, 3)
                oprot.writeI32(self.exp)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.sender)
        value = value * 31 ^ hash(self.receiver)
        value = value * 31 ^ hash(self.exp)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class subscribeUserExp_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('subscribeUserExp_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class unSubscribeUser_args():
    """
  Attributes:
   - user1
   - user2
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'user1', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'user2', (User, User.thrift_spec), None))

    def __init__(self, user1=None, user2=None):
        self.user1 = user1
        self.user2 = user2

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.user1 = User()
                        self.user1.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRUCT:
                        self.user2 = User()
                        self.user2.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('unSubscribeUser_args')
            if self.user1 is not None:
                oprot.writeFieldBegin('user1', TType.STRUCT, 1)
                self.user1.write(oprot)
                oprot.writeFieldEnd()
            if self.user2 is not None:
                oprot.writeFieldBegin('user2', TType.STRUCT, 2)
                self.user2.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.user1)
        value = value * 31 ^ hash(self.user2)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class unSubscribeUser_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('unSubscribeUser_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class deleteUserTempRelation_args():
    """
  Attributes:
   - user1
   - user2
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'user1', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'user2', (User, User.thrift_spec), None))

    def __init__(self, user1=None, user2=None):
        self.user1 = user1
        self.user2 = user2

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.user1 = User()
                        self.user1.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRUCT:
                        self.user2 = User()
                        self.user2.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('deleteUserTempRelation_args')
            if self.user1 is not None:
                oprot.writeFieldBegin('user1', TType.STRUCT, 1)
                self.user1.write(oprot)
                oprot.writeFieldEnd()
            if self.user2 is not None:
                oprot.writeFieldBegin('user2', TType.STRUCT, 2)
                self.user2.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.user1)
        value = value * 31 ^ hash(self.user2)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class deleteUserTempRelation_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('deleteUserTempRelation_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class rsend_args():
    """
  Attributes:
   - sender
   - receiver
   - syncKey
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'sender', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'receiver', (User, User.thrift_spec), None),
     (
      3, TType.I64, 'syncKey', None, None))

    def __init__(self, sender=None, receiver=None, syncKey=None):
        self.sender = sender
        self.receiver = receiver
        self.syncKey = syncKey

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.sender = User()
                    self.sender.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.receiver = User()
                    self.receiver.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.syncKey = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()
        return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('rsend_args')
            if self.sender is not None:
                oprot.writeFieldBegin('sender', TType.STRUCT, 1)
                self.sender.write(oprot)
                oprot.writeFieldEnd()
            if self.receiver is not None:
                oprot.writeFieldBegin('receiver', TType.STRUCT, 2)
                self.receiver.write(oprot)
                oprot.writeFieldEnd()
            if self.syncKey is not None:
                oprot.writeFieldBegin('syncKey', TType.I64, 3)
                oprot.writeI64(self.syncKey)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.sender)
        value = value * 31 ^ hash(self.receiver)
        value = value * 31 ^ hash(self.syncKey)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class rsend_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('rsend_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class rsync_args():
    """
  Attributes:
   - sender
   - receiver
   - syncKey
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'sender', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'receiver', (User, User.thrift_spec), None),
     (
      3, TType.I64, 'syncKey', None, None))

    def __init__(self, sender=None, receiver=None, syncKey=None):
        self.sender = sender
        self.receiver = receiver
        self.syncKey = syncKey

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.sender = User()
                    self.sender.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.receiver = User()
                    self.receiver.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.syncKey = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()
        return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('rsync_args')
            if self.sender is not None:
                oprot.writeFieldBegin('sender', TType.STRUCT, 1)
                self.sender.write(oprot)
                oprot.writeFieldEnd()
            if self.receiver is not None:
                oprot.writeFieldBegin('receiver', TType.STRUCT, 2)
                self.receiver.write(oprot)
                oprot.writeFieldEnd()
            if self.syncKey is not None:
                oprot.writeFieldBegin('syncKey', TType.I64, 3)
                oprot.writeI64(self.syncKey)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.sender)
        value = value * 31 ^ hash(self.receiver)
        value = value * 31 ^ hash(self.syncKey)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class rsync_result():
    """
  Attributes:
   - success
   - e
  """
    thrift_spec = (
     (
      0, TType.STRUCT, 'success', (ChatRSyncRet, ChatRSyncRet.thrift_spec), None),
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 0:
                    if ftype == TType.STRUCT:
                        self.success = ChatRSyncRet()
                        self.success.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('rsync_result')
            if self.success is not None:
                oprot.writeFieldBegin('success', TType.STRUCT, 0)
                self.success.write(oprot)
                oprot.writeFieldEnd()
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.success)
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class rsyncFin_args():
    """
  Attributes:
   - sender
   - receiver
   - syncKey
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'sender', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'receiver', (User, User.thrift_spec), None),
     (
      3, TType.I64, 'syncKey', None, None))

    def __init__(self, sender=None, receiver=None, syncKey=None):
        self.sender = sender
        self.receiver = receiver
        self.syncKey = syncKey

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.sender = User()
                    self.sender.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRUCT:
                    self.receiver = User()
                    self.receiver.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.syncKey = iprot.readI64()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()
        return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('rsyncFin_args')
            if self.sender is not None:
                oprot.writeFieldBegin('sender', TType.STRUCT, 1)
                self.sender.write(oprot)
                oprot.writeFieldEnd()
            if self.receiver is not None:
                oprot.writeFieldBegin('receiver', TType.STRUCT, 2)
                self.receiver.write(oprot)
                oprot.writeFieldEnd()
            if self.syncKey is not None:
                oprot.writeFieldBegin('syncKey', TType.I64, 3)
                oprot.writeI64(self.syncKey)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.sender)
        value = value * 31 ^ hash(self.receiver)
        value = value * 31 ^ hash(self.syncKey)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class rsyncFin_result():
    """
  Attributes:
   - e
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, e=None):
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('rsyncFin_result')
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class hasUnread_args():
    """
  Attributes:
   - sender
   - receiver
  """
    thrift_spec = (
     None,
     (
      1, TType.STRUCT, 'sender', (User, User.thrift_spec), None),
     (
      2, TType.STRUCT, 'receiver', (User, User.thrift_spec), None))

    def __init__(self, sender=None, receiver=None):
        self.sender = sender
        self.receiver = receiver

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 1:
                    if ftype == TType.STRUCT:
                        self.sender = User()
                        self.sender.read(iprot)
                    else:
                        iprot.skip(ftype)
                elif fid == 2:
                    if ftype == TType.STRUCT:
                        self.receiver = User()
                        self.receiver.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('hasUnread_args')
            if self.sender is not None:
                oprot.writeFieldBegin('sender', TType.STRUCT, 1)
                self.sender.write(oprot)
                oprot.writeFieldEnd()
            if self.receiver is not None:
                oprot.writeFieldBegin('receiver', TType.STRUCT, 2)
                self.receiver.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.sender)
        value = value * 31 ^ hash(self.receiver)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


class hasUnread_result():
    """
  Attributes:
   - success
   - e
  """
    thrift_spec = (
     (
      0, TType.I64, 'success', None, None),
     (
      1, TType.STRUCT, 'e', (ChatLogicException, ChatLogicException.thrift_spec), None))

    def __init__(self, success=None, e=None):
        self.success = success
        self.e = e

    def read(self, iprot):
        if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
            fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
            return
        else:
            iprot.readStructBegin()
            while True:
                fname, ftype, fid = iprot.readFieldBegin()
                if ftype == TType.STOP:
                    break
                if fid == 0:
                    if ftype == TType.I64:
                        self.success = iprot.readI64()
                    else:
                        iprot.skip(ftype)
                elif fid == 1:
                    if ftype == TType.STRUCT:
                        self.e = ChatLogicException()
                        self.e.read(iprot)
                    else:
                        iprot.skip(ftype)
                else:
                    iprot.skip(ftype)
                iprot.readFieldEnd()

            iprot.readStructEnd()
            return

    def write(self, oprot):
        if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
            oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
            return
        else:
            oprot.writeStructBegin('hasUnread_result')
            if self.success is not None:
                oprot.writeFieldBegin('success', TType.I64, 0)
                oprot.writeI64(self.success)
                oprot.writeFieldEnd()
            if self.e is not None:
                oprot.writeFieldBegin('e', TType.STRUCT, 1)
                self.e.write(oprot)
                oprot.writeFieldEnd()
            oprot.writeFieldStop()
            oprot.writeStructEnd()
            return

    def validate(self):
        pass

    def __hash__(self):
        value = 17
        value = value * 31 ^ hash(self.success)
        value = value * 31 ^ hash(self.e)
        return value

    def __repr__(self):
        L = [ '%s=%r' % (key, value) for key, value in self.__dict__.iteritems()
            ]
        return '%s(%s)' % (self.__class__.__name__, (', ').join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other