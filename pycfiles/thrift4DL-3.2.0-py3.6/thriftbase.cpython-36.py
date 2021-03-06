# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thrift4DL/server/tcp/thriftbase.py
# Compiled at: 2020-01-12 21:21:44
# Size of source mod 2**32: 12139 bytes
from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec
import sys, logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
all_structs = []

class Iface(object):

    def predict(self, image_binary):
        """
        Parameters:
         - image_binary

        """
        pass

    def ping(self):
        pass


class Client(Iface):

    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def predict(self, image_binary):
        """
        Parameters:
         - image_binary

        """
        self.send_predict(image_binary)
        return self.recv_predict()

    def send_predict(self, image_binary):
        self._oprot.writeMessageBegin('predict', TMessageType.CALL, self._seqid)
        args = predict_args()
        args.image_binary = image_binary
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_predict(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = predict_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        raise TApplicationException(TApplicationException.MISSING_RESULT, 'predict failed: unknown result')

    def ping(self):
        self.send_ping()
        self.recv_ping()

    def send_ping(self):
        self._oprot.writeMessageBegin('ping', TMessageType.CALL, self._seqid)
        args = ping_args()
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_ping(self):
        iprot = self._iprot
        fname, mtype, rseqid = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = ping_result()
        result.read(iprot)
        iprot.readMessageEnd()


class Processor(Iface, TProcessor):

    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap['predict'] = Processor.process_predict
        self._processMap['ping'] = Processor.process_ping

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
        else:
            self._processMap[name](self, seqid, iprot, oprot)
            return True

    def process_predict(self, seqid, iprot, oprot):
        args = predict_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = predict_result()
        try:
            result.success = self._handler.predict(args.image_binary)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('predict', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_ping(self, seqid, iprot, oprot):
        args = ping_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = ping_result()
        try:
            self._handler.ping()
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')

        oprot.writeMessageBegin('ping', msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()


class predict_args(object):
    __doc__ = '\n    Attributes:\n     - image_binary\n\n    '

    def __init__(self, image_binary=None):
        self.image_binary = image_binary

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.image_binary = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('predict_args')
        if self.image_binary is not None:
            oprot.writeFieldBegin('image_binary', TType.STRING, 1)
            oprot.writeString(self.image_binary.encode('utf-8') if sys.version_info[0] == 2 else self.image_binary)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(predict_args)
predict_args.thrift_spec = (
 None,
 (
  1, TType.STRING, 'image_binary', 'UTF8', None))

class predict_result(object):
    __doc__ = '\n    Attributes:\n     - success\n\n    '

    def __init__(self, success=None):
        self.success = success

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRING:
                    self.success = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('predict_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRING, 0)
            oprot.writeString(self.success.encode('utf-8') if sys.version_info[0] == 2 else self.success)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(predict_result)
predict_result.thrift_spec = (
 (
  0, TType.STRING, 'success', 'UTF8', None),)

class ping_args(object):

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('ping_args')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(ping_args)
ping_args.thrift_spec = ()

class ping_result(object):

    def read(self, iprot):
        if iprot._fast_decode is not None:
            if isinstance(iprot.trans, TTransport.CReadableTransport):
                if self.thrift_spec is not None:
                    iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
                    return
        iprot.readStructBegin()
        while True:
            fname, ftype, fid = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()

        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None:
            if self.thrift_spec is not None:
                oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
                return
        oprot.writeStructBegin('ping_result')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        pass

    def __repr__(self):
        L = ['%s=%r' % (key, value) for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other


all_structs.append(ping_result)
ping_result.thrift_spec = ()
fix_spec(all_structs)
del all_structs