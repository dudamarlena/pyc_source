# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/appservice.py
# Compiled at: 2020-01-29 15:49:54
"""
Application Layer
"""
from time import time as _time
from .debugging import ModuleLogger, DebugContents, bacpypes_debugging
from .comm import Client, ServiceAccessPoint, ApplicationServiceElement
from .task import OneShotTask
from .pdu import Address
from .apdu import encode_max_segments_accepted, decode_max_segments_accepted, encode_max_apdu_length_accepted, decode_max_apdu_length_accepted, AbortPDU, AbortReason, ComplexAckPDU, ConfirmedRequestPDU, Error, ErrorPDU, RejectPDU, SegmentAckPDU, SimpleAckPDU, UnconfirmedRequestPDU, apdu_types, unconfirmed_request_types, confirmed_request_types, complex_ack_types, error_types
from .errors import RejectException, AbortException, UnrecognizedService
_debug = 0
_log = ModuleLogger(globals())
IDLE = 0
SEGMENTED_REQUEST = 1
AWAIT_CONFIRMATION = 2
AWAIT_RESPONSE = 3
SEGMENTED_RESPONSE = 4
SEGMENTED_CONFIRMATION = 5
COMPLETED = 6
ABORTED = 7

@bacpypes_debugging
class SSM(OneShotTask, DebugContents):
    transactionLabels = [
     'IDLE',
     'SEGMENTED_REQUEST', 'AWAIT_CONFIRMATION', 'AWAIT_RESPONSE',
     'SEGMENTED_RESPONSE', 'SEGMENTED_CONFIRMATION', 'COMPLETED', 'ABORTED']
    _debug_contents = ('ssmSAP', 'localDevice', 'device_info', 'invokeID', 'state',
                       'segmentAPDU', 'segmentSize', 'segmentCount', 'maxSegmentsAccepted',
                       'retryCount', 'segmentRetryCount', 'sentAllSegments', 'lastSequenceNumber',
                       'initialSequenceNumber', 'actualWindowSize')

    def __init__(self, sap, pdu_address):
        """Common parts for client and server segmentation."""
        if _debug:
            SSM._debug('__init__ %r %r', sap, pdu_address)
        OneShotTask.__init__(self)
        self.ssmSAP = sap
        self.pdu_address = pdu_address
        self.device_info = sap.deviceInfoCache.get_device_info(pdu_address)
        self.invokeID = None
        self.state = IDLE
        self.segmentAPDU = None
        self.segmentSize = None
        self.segmentCount = None
        self.retryCount = None
        self.segmentRetryCount = None
        self.sentAllSegments = None
        self.lastSequenceNumber = None
        self.initialSequenceNumber = None
        self.actualWindowSize = None
        self.numberOfApduRetries = getattr(sap.localDevice, 'numberOfApduRetries', sap.numberOfApduRetries)
        self.apduTimeout = getattr(sap.localDevice, 'apduTimeout', sap.apduTimeout)
        self.segmentationSupported = getattr(sap.localDevice, 'segmentationSupported', sap.segmentationSupported)
        self.segmentTimeout = getattr(sap.localDevice, 'apduSegmentTimeout', sap.segmentTimeout)
        self.maxSegmentsAccepted = getattr(sap.localDevice, 'maxSegmentsAccepted', sap.maxSegmentsAccepted)
        self.maxApduLengthAccepted = getattr(sap.localDevice, 'maxApduLengthAccepted', sap.maxApduLengthAccepted)
        return

    def start_timer(self, msecs):
        if _debug:
            SSM._debug('start_timer %r', msecs)
        if self.isScheduled:
            if _debug:
                SSM._debug('    - is scheduled')
            self.suspend_task()
        self.install_task(delta=msecs / 1000.0)

    def stop_timer(self):
        if _debug:
            SSM._debug('stop_timer')
        if self.isScheduled:
            if _debug:
                SSM._debug('    - is scheduled')
            self.suspend_task()

    def restart_timer(self, msecs):
        if _debug:
            SSM._debug('restart_timer %r', msecs)
        if self.isScheduled:
            if _debug:
                SSM._debug('    - is scheduled')
            self.suspend_task()
        self.install_task(delta=msecs / 1000.0)

    def set_state(self, newState, timer=0):
        """This function is called when the derived class wants to change state."""
        if _debug:
            SSM._debug('set_state %r (%s) timer=%r', newState, SSM.transactionLabels[newState], timer)
        if self.state == COMPLETED or self.state == ABORTED:
            e = RuntimeError('invalid state transition from %s to %s' % (SSM.transactionLabels[self.state], SSM.transactionLabels[newState]))
            SSM._exception(e)
            raise e
        self.stop_timer()
        self.state = newState
        if timer:
            self.start_timer(timer)

    def set_segmentation_context(self, apdu):
        """This function is called to set the segmentation context."""
        if _debug:
            SSM._debug('set_segmentation_context %s', repr(apdu))
        self.segmentAPDU = apdu

    def get_segment(self, indx):
        """This function returns an APDU coorisponding to a particular
        segment of a confirmed request or complex ack.  The segmentAPDU
        is the context."""
        if _debug:
            SSM._debug('get_segment %r', indx)
        if not self.segmentAPDU:
            raise RuntimeError('no segmentation context established')
        if indx >= self.segmentCount:
            raise RuntimeError('invalid segment number %r, APDU has %r segments' % (indx, self.segmentCount))
        if self.segmentAPDU.apduType == ConfirmedRequestPDU.pduType:
            if _debug:
                SSM._debug('    - confirmed request context')
            segAPDU = ConfirmedRequestPDU(self.segmentAPDU.apduService)
            segAPDU.apduMaxSegs = encode_max_segments_accepted(self.maxSegmentsAccepted)
            segAPDU.apduMaxResp = encode_max_apdu_length_accepted(self.maxApduLengthAccepted)
            segAPDU.apduInvokeID = self.invokeID
            segAPDU.apduSA = self.segmentationSupported in ('segmentedReceive', 'segmentedBoth')
            if _debug:
                SSM._debug('    - segmented response accepted: %r', segAPDU.apduSA)
        elif self.segmentAPDU.apduType == ComplexAckPDU.pduType:
            if _debug:
                SSM._debug('    - complex ack context')
            segAPDU = ComplexAckPDU(self.segmentAPDU.apduService, self.segmentAPDU.apduInvokeID)
        else:
            raise RuntimeError('invalid APDU type for segmentation context')
        segAPDU.pduUserData = self.segmentAPDU.pduUserData
        segAPDU.pduDestination = self.pdu_address
        if self.segmentCount != 1:
            segAPDU.apduSeg = True
            segAPDU.apduMor = indx < self.segmentCount - 1
            segAPDU.apduSeq = indx % 256
            if indx == 0:
                if _debug:
                    SSM._debug('    - proposedWindowSize: %r', self.ssmSAP.proposedWindowSize)
                segAPDU.apduWin = self.ssmSAP.proposedWindowSize
            else:
                if _debug:
                    SSM._debug('    - actualWindowSize: %r', self.actualWindowSize)
                segAPDU.apduWin = self.actualWindowSize
        else:
            segAPDU.apduSeg = False
            segAPDU.apduMor = False
        offset = indx * self.segmentSize
        segAPDU.put_data(self.segmentAPDU.pduData[offset:offset + self.segmentSize])
        return segAPDU

    def append_segment(self, apdu):
        """This function appends the apdu content to the end of the current
        APDU being built.  The segmentAPDU is the context."""
        if _debug:
            SSM._debug('append_segment %r', apdu)
        if not self.segmentAPDU:
            raise RuntimeError('no segmentation context established')
        self.segmentAPDU.put_data(apdu.pduData)

    def in_window(self, seqA, seqB):
        if _debug:
            SSM._debug('in_window %r %r', seqA, seqB)
        rslt = (seqA - seqB + 256) % 256 < self.actualWindowSize
        if _debug:
            SSM._debug('    - rslt: %r', rslt)
        return rslt

    def fill_window(self, seqNum):
        """This function sends all of the packets necessary to fill
        out the segmentation window."""
        if _debug:
            SSM._debug('fill_window %r', seqNum)
        if _debug:
            SSM._debug('    - actualWindowSize: %r', self.actualWindowSize)
        for ix in range(self.actualWindowSize):
            apdu = self.get_segment(seqNum + ix)
            self.ssmSAP.request(apdu)
            if not apdu.apduMor:
                self.sentAllSegments = True
                break


@bacpypes_debugging
class ClientSSM(SSM):

    def __init__(self, sap, pdu_address):
        if _debug:
            ClientSSM._debug('__init__ %s %r', sap, pdu_address)
        SSM.__init__(self, sap, pdu_address)
        self.retryCount = 0
        if self.device_info:
            if _debug:
                ClientSSM._debug('    - acquire device information')
            self.ssmSAP.deviceInfoCache.acquire(self.device_info)

    def set_state(self, newState, timer=0):
        """This function is called when the client wants to change state."""
        if _debug:
            ClientSSM._debug('set_state %r (%s) timer=%r', newState, SSM.transactionLabels[newState], timer)
        SSM.set_state(self, newState, timer)
        if newState == COMPLETED or newState == ABORTED:
            if _debug:
                ClientSSM._debug('    - remove from active transactions')
            self.ssmSAP.clientTransactions.remove(self)
            if self.device_info:
                if _debug:
                    ClientSSM._debug('    - release device information')
                self.ssmSAP.deviceInfoCache.release(self.device_info)

    def request(self, apdu):
        """This function is called by client transaction functions when it wants
        to send a message to the device."""
        if _debug:
            ClientSSM._debug('request %r', apdu)
        apdu.pduSource = None
        apdu.pduDestination = self.pdu_address
        self.ssmSAP.request(apdu)
        return

    def indication(self, apdu):
        """This function is called after the device has bound a new transaction
        and wants to start the process rolling."""
        if _debug:
            ClientSSM._debug('indication %r', apdu)
        if apdu.apduType != ConfirmedRequestPDU.pduType:
            raise RuntimeError('invalid APDU (1)')
        self.set_segmentation_context(apdu)
        if not self.device_info or self.device_info.maxApduLengthAccepted is None:
            self.segmentSize = self.maxApduLengthAccepted
        elif self.device_info.maxNpduLength is None:
            self.segmentSize = self.device_info.maxApduLengthAccepted
        else:
            self.segmentSize = min(self.device_info.maxNpduLength, self.device_info.maxApduLengthAccepted)
        if _debug:
            ClientSSM._debug('    - segment size: %r', self.segmentSize)
        self.invokeID = apdu.apduInvokeID
        if _debug:
            ClientSSM._debug('    - invoke ID: %r', self.invokeID)
        if not apdu.pduData:
            self.segmentCount = 1
        else:
            self.segmentCount, more = divmod(len(apdu.pduData), self.segmentSize)
            if more:
                self.segmentCount += 1
        if _debug:
            ClientSSM._debug('    - segment count: %r', self.segmentCount)
        if self.segmentCount > 1:
            if self.segmentationSupported not in ('segmentedTransmit', 'segmentedBoth'):
                if _debug:
                    ClientSSM._debug("    - local device can't send segmented requests")
                abort = self.abort(AbortReason.segmentationNotSupported)
                self.response(abort)
                return
            if not self.device_info:
                if _debug:
                    ClientSSM._debug('    - no server info for segmentation support')
            elif self.device_info.segmentationSupported not in ('segmentedReceive',
                                                                'segmentedBoth'):
                if _debug:
                    ClientSSM._debug("    - server can't receive segmented requests")
                abort = self.abort(AbortReason.segmentationNotSupported)
                self.response(abort)
                return
            if not self.device_info:
                if _debug:
                    ClientSSM._debug('    - no server info for maximum number of segments')
            elif not self.device_info.maxSegmentsAccepted:
                if _debug:
                    ClientSSM._debug("    - server doesn't say maximum number of segments")
            elif self.segmentCount > self.device_info.maxSegmentsAccepted:
                if _debug:
                    ClientSSM._debug("    - server can't receive enough segments")
                abort = self.abort(AbortReason.apduTooLong)
                self.response(abort)
                return
        if self.segmentCount == 1:
            self.sentAllSegments = True
            self.retryCount = 0
            self.set_state(AWAIT_CONFIRMATION, self.apduTimeout)
        else:
            self.sentAllSegments = False
            self.retryCount = 0
            self.segmentRetryCount = 0
            self.initialSequenceNumber = 0
            self.actualWindowSize = None
            self.set_state(SEGMENTED_REQUEST, self.segmentTimeout)
        self.request(self.get_segment(0))
        return

    def response(self, apdu):
        """This function is called by client transaction functions when they want
        to send a message to the application."""
        if _debug:
            ClientSSM._debug('response %r', apdu)
        apdu.pduSource = self.pdu_address
        apdu.pduDestination = None
        self.ssmSAP.sap_response(apdu)
        return

    def confirmation(self, apdu):
        """This function is called by the device for all upstream messages related
        to the transaction."""
        if _debug:
            ClientSSM._debug('confirmation %r', apdu)
        if self.state == SEGMENTED_REQUEST:
            self.segmented_request(apdu)
        elif self.state == AWAIT_CONFIRMATION:
            self.await_confirmation(apdu)
        elif self.state == SEGMENTED_CONFIRMATION:
            self.segmented_confirmation(apdu)
        else:
            raise RuntimeError('invalid state')

    def process_task(self):
        """This function is called when something has taken too long."""
        if _debug:
            ClientSSM._debug('process_task')
        if self.state == SEGMENTED_REQUEST:
            self.segmented_request_timeout()
        elif self.state == AWAIT_CONFIRMATION:
            self.await_confirmation_timeout()
        elif self.state == SEGMENTED_CONFIRMATION:
            self.segmented_confirmation_timeout()
        elif self.state == COMPLETED:
            pass
        elif self.state == ABORTED:
            pass
        else:
            e = RuntimeError('invalid state')
            ClientSSM._exception('exception: %r', e)
            raise e

    def abort(self, reason):
        """This function is called when the transaction should be aborted."""
        if _debug:
            ClientSSM._debug('abort %r', reason)
        self.set_state(ABORTED)
        abort_pdu = AbortPDU(False, self.invokeID, reason)
        return abort_pdu

    def segmented_request(self, apdu):
        """This function is called when the client is sending a segmented request
        and receives an apdu."""
        if _debug:
            ClientSSM._debug('segmented_request %r', apdu)
        if apdu.apduType == SegmentAckPDU.pduType:
            if _debug:
                ClientSSM._debug('    - segment ack')
            self.actualWindowSize = apdu.apduWin
            if not self.in_window(apdu.apduSeq, self.initialSequenceNumber):
                if _debug:
                    ClientSSM._debug('    - not in window')
                self.restart_timer(self.segmentTimeout)
            elif self.sentAllSegments:
                if _debug:
                    ClientSSM._debug('    - all done sending request')
                self.set_state(AWAIT_CONFIRMATION, self.apduTimeout)
            else:
                if _debug:
                    ClientSSM._debug('    - more segments to send')
                self.initialSequenceNumber = (apdu.apduSeq + 1) % 256
                self.segmentRetryCount = 0
                self.fill_window(self.initialSequenceNumber)
                self.restart_timer(self.segmentTimeout)
        elif apdu.apduType == SimpleAckPDU.pduType:
            if _debug:
                ClientSSM._debug('    - simple ack')
            if not self.sentAllSegments:
                abort = self.abort(AbortReason.invalidApduInThisState)
                self.request(abort)
                self.response(abort)
            else:
                self.set_state(COMPLETED)
                self.response(apdu)
        elif apdu.apduType == ComplexAckPDU.pduType:
            if _debug:
                ClientSSM._debug('    - complex ack')
            if not self.sentAllSegments:
                abort = self.abort(AbortReason.invalidApduInThisState)
                self.request(abort)
                self.response(abort)
            elif not apdu.apduSeg:
                self.set_state(COMPLETED)
                self.response(apdu)
            else:
                self.set_segmentation_context(apdu)
                self.actualWindowSize = min(apdu.apduWin, self.ssmSAP.proposedWindowSize)
                self.lastSequenceNumber = 0
                self.initialSequenceNumber = 0
                self.set_state(SEGMENTED_CONFIRMATION, self.segmentTimeout)
        elif apdu.apduType == ErrorPDU.pduType or apdu.apduType == RejectPDU.pduType or apdu.apduType == AbortPDU.pduType:
            if _debug:
                ClientSSM._debug('    - error/reject/abort')
            self.set_state(COMPLETED)
            self.response(apdu)
        else:
            raise RuntimeError('invalid APDU (2)')

    def segmented_request_timeout(self):
        if _debug:
            ClientSSM._debug('segmented_request_timeout')
        if self.segmentRetryCount < self.numberOfApduRetries:
            if _debug:
                ClientSSM._debug('    - retry segmented request')
            self.segmentRetryCount += 1
            self.start_timer(self.segmentTimeout)
            if self.initialSequenceNumber == 0:
                self.request(self.get_segment(0))
            else:
                self.fill_window(self.initialSequenceNumber)
        else:
            if _debug:
                ClientSSM._debug('    - abort, no response from the device')
            abort = self.abort(AbortReason.noResponse)
            self.response(abort)

    def await_confirmation(self, apdu):
        if _debug:
            ClientSSM._debug('await_confirmation %r', apdu)
        if apdu.apduType == AbortPDU.pduType:
            if _debug:
                ClientSSM._debug('    - server aborted')
            self.set_state(ABORTED)
            self.response(apdu)
        elif apdu.apduType == SimpleAckPDU.pduType or apdu.apduType == ErrorPDU.pduType or apdu.apduType == RejectPDU.pduType:
            if _debug:
                ClientSSM._debug('    - simple ack, error, or reject')
            self.set_state(COMPLETED)
            self.response(apdu)
        elif apdu.apduType == ComplexAckPDU.pduType:
            if _debug:
                ClientSSM._debug('    - complex ack')
            if not apdu.apduSeg:
                if _debug:
                    ClientSSM._debug('    - unsegmented')
                self.set_state(COMPLETED)
                self.response(apdu)
            elif self.segmentationSupported not in ('segmentedReceive', 'segmentedBoth'):
                if _debug:
                    ClientSSM._debug("    - local device can't receive segmented messages")
                abort = self.abort(AbortReason.segmentationNotSupported)
                self.response(abort)
            elif apdu.apduSeq == 0:
                if _debug:
                    ClientSSM._debug('    - segmented response')
                self.set_segmentation_context(apdu)
                self.actualWindowSize = apdu.apduWin
                self.lastSequenceNumber = 0
                self.initialSequenceNumber = 0
                self.set_state(SEGMENTED_CONFIRMATION, self.segmentTimeout)
                segack = SegmentAckPDU(0, 0, self.invokeID, self.initialSequenceNumber, self.actualWindowSize)
                self.request(segack)
            else:
                if _debug:
                    ClientSSM._debug('    - invalid APDU in this state')
                abort = self.abort(AbortReason.invalidApduInThisState)
                self.request(abort)
                self.response(abort)
        elif apdu.apduType == SegmentAckPDU.pduType:
            if _debug:
                ClientSSM._debug('    - segment ack(!?)')
            self.restart_timer(self.segmentTimeout)
        else:
            raise RuntimeError('invalid APDU (3)')

    def await_confirmation_timeout(self):
        if _debug:
            ClientSSM._debug('await_confirmation_timeout')
        if self.retryCount < self.numberOfApduRetries:
            if _debug:
                ClientSSM._debug('    - no response, try again (%d < %d)', self.retryCount, self.numberOfApduRetries)
            self.retryCount += 1
            saveCount = self.retryCount
            self.indication(self.segmentAPDU)
            self.retryCount = saveCount
        else:
            if _debug:
                ClientSSM._debug('    - retry count exceeded')
            abort = self.abort(AbortReason.noResponse)
            self.response(abort)

    def segmented_confirmation(self, apdu):
        if _debug:
            ClientSSM._debug('segmented_confirmation %r', apdu)
        if apdu.apduType != ComplexAckPDU.pduType:
            if _debug:
                ClientSSM._debug('    - complex ack required')
            abort = self.abort(AbortReason.invalidApduInThisState)
            self.request(abort)
            self.response(abort)
            return
        if not apdu.apduSeg:
            if _debug:
                ClientSSM._debug('    - must be segmented')
            abort = self.abort(AbortReason.invalidApduInThisState)
            self.request(abort)
            self.response(abort)
            return
        if apdu.apduSeq != (self.lastSequenceNumber + 1) % 256:
            if _debug:
                ClientSSM._debug('    - segment %s received out of order, should be %s', apdu.apduSeq, (self.lastSequenceNumber + 1) % 256)
            self.restart_timer(self.segmentTimeout)
            segack = SegmentAckPDU(1, 0, self.invokeID, self.lastSequenceNumber, self.actualWindowSize)
            self.request(segack)
            return
        self.append_segment(apdu)
        self.lastSequenceNumber = (self.lastSequenceNumber + 1) % 256
        if not apdu.apduMor:
            if _debug:
                ClientSSM._debug('    - no more follows')
            segack = SegmentAckPDU(0, 0, self.invokeID, self.lastSequenceNumber, self.actualWindowSize)
            self.request(segack)
            self.set_state(COMPLETED)
            self.response(self.segmentAPDU)
        elif apdu.apduSeq == (self.initialSequenceNumber + self.actualWindowSize) % 256:
            if _debug:
                ClientSSM._debug('    - last segment in the group')
            self.initialSequenceNumber = self.lastSequenceNumber
            self.restart_timer(self.segmentTimeout)
            segack = SegmentAckPDU(0, 0, self.invokeID, self.lastSequenceNumber, self.actualWindowSize)
            self.request(segack)
        else:
            if _debug:
                ClientSSM._debug('    - wait for more segments')
            self.restart_timer(self.segmentTimeout)

    def segmented_confirmation_timeout(self):
        if _debug:
            ClientSSM._debug('segmented_confirmation_timeout')
        abort = self.abort(AbortReason.noResponse)
        self.response(abort)


@bacpypes_debugging
class ServerSSM(SSM):

    def __init__(self, sap, pdu_address):
        if _debug:
            ServerSSM._debug('__init__ %s %r', sap, pdu_address)
        SSM.__init__(self, sap, pdu_address)
        if self.device_info:
            if _debug:
                ServerSSM._debug('    - acquire device information')
            self.ssmSAP.deviceInfoCache.acquire(self.device_info)

    def set_state(self, newState, timer=0):
        """This function is called when the client wants to change state."""
        if _debug:
            ServerSSM._debug('set_state %r (%s) timer=%r', newState, SSM.transactionLabels[newState], timer)
        SSM.set_state(self, newState, timer)
        if newState == COMPLETED or newState == ABORTED:
            if _debug:
                ServerSSM._debug('    - remove from active transactions')
            self.ssmSAP.serverTransactions.remove(self)
            if self.device_info:
                if _debug:
                    ClientSSM._debug('    - release device information')
                self.ssmSAP.deviceInfoCache.release(self.device_info)

    def request(self, apdu):
        """This function is called by transaction functions to send
        to the application."""
        if _debug:
            ServerSSM._debug('request %r', apdu)
        apdu.pduSource = self.pdu_address
        apdu.pduDestination = None
        self.ssmSAP.sap_request(apdu)
        return

    def indication(self, apdu):
        """This function is called for each downstream packet related to
        the transaction."""
        if _debug:
            ServerSSM._debug('indication %r', apdu)
        if self.state == IDLE:
            self.idle(apdu)
        elif self.state == SEGMENTED_REQUEST:
            self.segmented_request(apdu)
        elif self.state == AWAIT_RESPONSE:
            self.await_response(apdu)
        elif self.state == SEGMENTED_RESPONSE:
            self.segmented_response(apdu)
        elif _debug:
            ServerSSM._debug('    - invalid state')

    def response(self, apdu):
        """This function is called by transaction functions when they want
        to send a message to the device."""
        if _debug:
            ServerSSM._debug('response %r', apdu)
        apdu.pduSource = None
        apdu.pduDestination = self.pdu_address
        self.ssmSAP.request(apdu)
        return

    def confirmation(self, apdu):
        """This function is called when the application has provided a response
        and needs it to be sent to the client."""
        if _debug:
            ServerSSM._debug('confirmation %r', apdu)
        if self.state != AWAIT_RESPONSE:
            if _debug:
                ServerSSM._debug('    - warning: not expecting a response')
        if apdu.apduType == AbortPDU.pduType:
            if _debug:
                ServerSSM._debug('    - abort')
            self.set_state(ABORTED)
            self.response(apdu)
            return
        else:
            if apdu.apduType == SimpleAckPDU.pduType or apdu.apduType == ErrorPDU.pduType or apdu.apduType == RejectPDU.pduType:
                if _debug:
                    ServerSSM._debug('    - simple ack, error, or reject')
                self.set_state(COMPLETED)
                self.response(apdu)
                return
            if apdu.apduType == ComplexAckPDU.pduType:
                if _debug:
                    ServerSSM._debug('    - complex ack')
                self.set_segmentation_context(apdu)
                if not self.device_info or self.device_info.maxNpduLength is None:
                    self.segmentSize = self.maxApduLengthAccepted
                else:
                    self.segmentSize = min(self.device_info.maxNpduLength, self.maxApduLengthAccepted)
                if _debug:
                    ServerSSM._debug('    - segment size: %r', self.segmentSize)
                if not apdu.pduData:
                    self.segmentCount = 1
                else:
                    self.segmentCount, more = divmod(len(apdu.pduData), self.segmentSize)
                    if more:
                        self.segmentCount += 1
                if _debug:
                    ServerSSM._debug('    - segment count: %r', self.segmentCount)
                if self.segmentCount > 1:
                    if _debug:
                        ServerSSM._debug('    - segmentation required, %d segments', self.segmentCount)
                    if self.segmentationSupported not in ('segmentedTransmit', 'segmentedBoth'):
                        if _debug:
                            ServerSSM._debug("    - server can't send segmented responses")
                        abort = self.abort(AbortReason.segmentationNotSupported)
                        self.response(abort)
                        return
                    if not self.segmented_response_accepted:
                        if _debug:
                            ServerSSM._debug("    - client can't receive segmented responses")
                        abort = self.abort(AbortReason.segmentationNotSupported)
                        self.response(abort)
                        return
                    if self.maxSegmentsAccepted is not None and self.segmentCount > self.maxSegmentsAccepted:
                        if _debug:
                            ServerSSM._debug("    - client can't receive enough segments")
                        abort = self.abort(AbortReason.apduTooLong)
                        self.response(abort)
                        return
                self.segmentRetryCount = 0
                self.initialSequenceNumber = 0
                self.actualWindowSize = None
                if self.segmentCount == 1:
                    self.response(apdu)
                    self.set_state(COMPLETED)
                else:
                    self.response(self.get_segment(0))
                    self.set_state(SEGMENTED_RESPONSE, self.segmentTimeout)
            else:
                raise RuntimeError('invalid APDU (4)')
            return

    def process_task(self):
        """This function is called when the client has failed to send all of the
        segments of a segmented request, the application has taken too long to
        complete the request, or the client failed to ack the segments of a
        segmented response."""
        if _debug:
            ServerSSM._debug('process_task')
        if self.state == SEGMENTED_REQUEST:
            self.segmented_request_timeout()
        elif self.state == AWAIT_RESPONSE:
            self.await_response_timeout()
        elif self.state == SEGMENTED_RESPONSE:
            self.segmented_response_timeout()
        elif self.state == COMPLETED:
            pass
        elif self.state == ABORTED:
            pass
        else:
            if _debug:
                ServerSSM._debug('invalid state')
            raise RuntimeError('invalid state')

    def abort(self, reason):
        """This function is called when the application would like to abort the
        transaction.  There is no notification back to the application."""
        if _debug:
            ServerSSM._debug('abort %r', reason)
        self.set_state(ABORTED)
        return AbortPDU(True, self.invokeID, reason)

    def idle(self, apdu):
        if _debug:
            ServerSSM._debug('idle %r', apdu)
        if not isinstance(apdu, ConfirmedRequestPDU):
            raise RuntimeError('invalid APDU (5)')
        self.invokeID = apdu.apduInvokeID
        if _debug:
            ServerSSM._debug('    - invoke ID: %r', self.invokeID)
        self.segmented_response_accepted = apdu.apduSA
        if apdu.apduSA and self.device_info:
            if self.device_info.segmentationSupported == 'noSegmentation':
                if _debug:
                    ServerSSM._debug('    - client actually supports segmented receive')
                self.device_info.segmentationSupported = 'segmentedReceive'
                if _debug:
                    ServerSSM._debug('    - tell the cache the info has been updated')
                self.ssmSAP.deviceInfoCache.update_device_info(self.device_info)
            elif self.device_info.segmentationSupported == 'segmentedTransmit':
                if _debug:
                    ServerSSM._debug('    - client actually supports both segmented transmit and receive')
                self.device_info.segmentationSupported = 'segmentedBoth'
                if _debug:
                    ServerSSM._debug('    - tell the cache the info has been updated')
                self.ssmSAP.deviceInfoCache.update_device_info(self.device_info)
            elif self.device_info.segmentationSupported == 'segmentedReceive':
                pass
            elif self.device_info.segmentationSupported == 'segmentedBoth':
                pass
            else:
                raise RuntimeError('invalid segmentation supported in device info')
        self.maxApduLengthAccepted = decode_max_apdu_length_accepted(apdu.apduMaxResp)
        if self.device_info and self.device_info.maxApduLengthAccepted is not None:
            if self.device_info.maxApduLengthAccepted < self.maxApduLengthAccepted:
                if _debug:
                    ServerSSM._debug('    - apduMaxResp encoding error')
            else:
                self.maxApduLengthAccepted = self.device_info.maxApduLengthAccepted
        if _debug:
            ServerSSM._debug('    - maxApduLengthAccepted: %r', self.maxApduLengthAccepted)
        self.maxSegmentsAccepted = decode_max_segments_accepted(apdu.apduMaxSegs)
        if not apdu.apduSeg:
            self.set_state(AWAIT_RESPONSE, self.ssmSAP.applicationTimeout)
            self.request(apdu)
            return
        else:
            if self.segmentationSupported not in ('segmentedReceive', 'segmentedBoth'):
                abort = self.abort(AbortReason.segmentationNotSupported)
                self.response(abort)
                return
            self.set_segmentation_context(apdu)
            self.actualWindowSize = min(apdu.apduWin, self.ssmSAP.proposedWindowSize)
            if _debug:
                ServerSSM._debug('    - actualWindowSize? min(%r, %r) -> %r', apdu.apduWin, self.ssmSAP.proposedWindowSize, self.actualWindowSize)
            self.lastSequenceNumber = 0
            self.initialSequenceNumber = 0
            self.set_state(SEGMENTED_REQUEST, self.segmentTimeout)
            segack = SegmentAckPDU(0, 1, self.invokeID, self.initialSequenceNumber, self.actualWindowSize)
            if _debug:
                ServerSSM._debug('    - segAck: %r', segack)
            self.response(segack)
            return

    def segmented_request(self, apdu):
        if _debug:
            ServerSSM._debug('segmented_request %r', apdu)
        if apdu.apduType == AbortPDU.pduType:
            self.set_state(COMPLETED)
            self.response(apdu)
            return
        if apdu.apduType != ConfirmedRequestPDU.pduType:
            abort = self.abort(AbortReason.invalidApduInThisState)
            self.request(abort)
            self.response(abort)
            return
        if not apdu.apduSeg:
            abort = self.abort(AbortReason.invalidApduInThisState)
            self.request(abort)
            self.response(abort)
            return
        if apdu.apduSeq != (self.lastSequenceNumber + 1) % 256:
            if _debug:
                ServerSSM._debug('    - segment %d received out of order, should be %d', apdu.apduSeq, (self.lastSequenceNumber + 1) % 256)
            self.restart_timer(self.segmentTimeout)
            segack = SegmentAckPDU(1, 1, self.invokeID, self.initialSequenceNumber, self.actualWindowSize)
            self.response(segack)
            return
        self.append_segment(apdu)
        self.lastSequenceNumber = (self.lastSequenceNumber + 1) % 256
        if not apdu.apduMor:
            if _debug:
                ServerSSM._debug('    - no more follows')
            segack = SegmentAckPDU(0, 1, self.invokeID, self.lastSequenceNumber, self.actualWindowSize)
            self.response(segack)
            self.set_state(AWAIT_RESPONSE, self.ssmSAP.applicationTimeout)
            self.request(self.segmentAPDU)
        elif apdu.apduSeq == (self.initialSequenceNumber + self.actualWindowSize) % 256:
            if _debug:
                ServerSSM._debug('    - last segment in the group')
            self.initialSequenceNumber = self.lastSequenceNumber
            self.restart_timer(self.segmentTimeout)
            segack = SegmentAckPDU(0, 1, self.invokeID, self.initialSequenceNumber, self.actualWindowSize)
            self.response(segack)
        else:
            if _debug:
                ServerSSM._debug('    - wait for more segments')
            self.restart_timer(self.segmentTimeout)

    def segmented_request_timeout(self):
        if _debug:
            ServerSSM._debug('segmented_request_timeout')
        self.set_state(ABORTED)

    def await_response(self, apdu):
        if _debug:
            ServerSSM._debug('await_response %r', apdu)
        if isinstance(apdu, ConfirmedRequestPDU):
            if _debug:
                ServerSSM._debug('    - client is trying this request again')
        elif isinstance(apdu, AbortPDU):
            if _debug:
                ServerSSM._debug('    - client aborting this request')
            self.set_state(ABORTED)
            self.request(apdu)
        else:
            raise RuntimeError('invalid APDU (6)')

    def await_response_timeout(self):
        """This function is called when the application has taken too long
        to respond to a clients request.  The client has probably long since
        given up."""
        if _debug:
            ServerSSM._debug('await_response_timeout')
        abort = self.abort(AbortReason.serverTimeout)
        self.request(abort)

    def segmented_response(self, apdu):
        if _debug:
            ServerSSM._debug('segmented_response %r', apdu)
        if apdu.apduType == SegmentAckPDU.pduType:
            if _debug:
                ServerSSM._debug('    - segment ack')
            self.actualWindowSize = apdu.apduWin
            if not self.in_window(apdu.apduSeq, self.initialSequenceNumber):
                if _debug:
                    ServerSSM._debug('    - not in window')
                self.restart_timer(self.segmentTimeout)
            elif self.sentAllSegments:
                if _debug:
                    ServerSSM._debug('    - all done sending response')
                self.set_state(COMPLETED)
            else:
                if _debug:
                    ServerSSM._debug('    - more segments to send')
                self.initialSequenceNumber = (apdu.apduSeq + 1) % 256
                self.actualWindowSize = apdu.apduWin
                self.segmentRetryCount = 0
                self.fill_window(self.initialSequenceNumber)
                self.restart_timer(self.segmentTimeout)
        elif apdu.apduType == AbortPDU.pduType:
            self.set_state(COMPLETED)
            self.response(apdu)
        else:
            raise RuntimeError('invalid APDU (7)')

    def segmented_response_timeout(self):
        if _debug:
            ServerSSM._debug('segmented_response_timeout')
        if self.segmentRetryCount < self.numberOfApduRetries:
            self.segmentRetryCount += 1
            self.start_timer(self.segmentTimeout)
            self.fill_window(self.initialSequenceNumber)
        else:
            self.set_state(ABORTED)


@bacpypes_debugging
class StateMachineAccessPoint(Client, ServiceAccessPoint):

    def __init__(self, localDevice=None, deviceInfoCache=None, sap=None, cid=None):
        if _debug:
            StateMachineAccessPoint._debug('__init__ localDevice=%r deviceInfoCache=%r sap=%r cid=%r', localDevice, deviceInfoCache, sap, cid)
        Client.__init__(self, cid)
        ServiceAccessPoint.__init__(self, sap)
        self.localDevice = localDevice
        self.deviceInfoCache = deviceInfoCache
        self.nextInvokeID = 1
        self.clientTransactions = []
        self.serverTransactions = []
        self.numberOfApduRetries = 3
        self.apduTimeout = 3000
        self.maxApduLengthAccepted = 1024
        self.segmentationSupported = 'noSegmentation'
        self.segmentTimeout = 1500
        self.maxSegmentsAccepted = 2
        self.proposedWindowSize = 2
        self.dccEnableDisable = 'enable'
        self.applicationTimeout = 3000

    def get_next_invoke_id(self, addr):
        """Called by clients to get an unused invoke ID."""
        if _debug:
            StateMachineAccessPoint._debug('get_next_invoke_id')
        initialID = self.nextInvokeID
        while 1:
            invokeID = self.nextInvokeID
            self.nextInvokeID = (self.nextInvokeID + 1) % 256
            if initialID == self.nextInvokeID:
                raise RuntimeError('no available invoke ID')
            for tr in self.clientTransactions:
                if invokeID == tr.invokeID and addr == tr.pdu_address:
                    break
            else:
                break

        return invokeID

    def confirmation(self, pdu):
        """Packets coming up the stack are APDU's."""
        if _debug:
            StateMachineAccessPoint._debug('confirmation %r', pdu)
        if self.dccEnableDisable == 'enable':
            if _debug:
                StateMachineAccessPoint._debug('    - communications enabled')
        else:
            if self.dccEnableDisable == 'disable':
                if pdu.apduType == 0 and pdu.apduService == 17:
                    if _debug:
                        StateMachineAccessPoint._debug('    - continue with DCC request')
                elif pdu.apduType == 0 and pdu.apduService == 20:
                    if _debug:
                        StateMachineAccessPoint._debug('    - continue with reinitialize device')
                elif pdu.apduType == 1 and pdu.apduService == 8:
                    if _debug:
                        StateMachineAccessPoint._debug('    - continue with Who-Is')
                else:
                    if _debug:
                        StateMachineAccessPoint._debug('    - not a Who-Is, dropped')
                    return
            elif self.dccEnableDisable == 'disableInitiation':
                if _debug:
                    StateMachineAccessPoint._debug('    - initiation disabled')
            atype = apdu_types.get(pdu.apduType)
            if not atype:
                StateMachineAccessPoint._warning('    - unknown apduType: %r', pdu.apduType)
                return
        apdu = atype()
        apdu.decode(pdu)
        if _debug:
            StateMachineAccessPoint._debug('    - apdu: %r', apdu)
        if isinstance(apdu, ConfirmedRequestPDU):
            for tr in self.serverTransactions:
                if apdu.apduInvokeID == tr.invokeID and apdu.pduSource == tr.pdu_address:
                    break
            else:
                tr = ServerSSM(self, apdu.pduSource)
                self.serverTransactions.append(tr)

            tr.indication(apdu)
        elif isinstance(apdu, UnconfirmedRequestPDU):
            self.sap_request(apdu)
        elif isinstance(apdu, SimpleAckPDU) or isinstance(apdu, ComplexAckPDU) or isinstance(apdu, ErrorPDU) or isinstance(apdu, RejectPDU):
            for tr in self.clientTransactions:
                if apdu.apduInvokeID == tr.invokeID and apdu.pduSource == tr.pdu_address:
                    break
            else:
                return

            tr.confirmation(apdu)
        elif isinstance(apdu, AbortPDU):
            if apdu.apduSrv:
                for tr in self.clientTransactions:
                    if apdu.apduInvokeID == tr.invokeID and apdu.pduSource == tr.pdu_address:
                        break
                else:
                    return

                tr.confirmation(apdu)
            else:
                for tr in self.serverTransactions:
                    if apdu.apduInvokeID == tr.invokeID and apdu.pduSource == tr.pdu_address:
                        break
                else:
                    return

                tr.indication(apdu)
        elif isinstance(apdu, SegmentAckPDU):
            if apdu.apduSrv:
                for tr in self.clientTransactions:
                    if apdu.apduInvokeID == tr.invokeID and apdu.pduSource == tr.pdu_address:
                        break
                else:
                    return

                tr.confirmation(apdu)
            else:
                for tr in self.serverTransactions:
                    if apdu.apduInvokeID == tr.invokeID and apdu.pduSource == tr.pdu_address:
                        break
                else:
                    return

                tr.indication(apdu)
        else:
            raise RuntimeError('invalid APDU (8)')

    def sap_indication(self, apdu):
        """This function is called when the application is requesting
        a new transaction as a client."""
        if _debug:
            StateMachineAccessPoint._debug('sap_indication %r', apdu)
        if self.dccEnableDisable == 'enable':
            if _debug:
                StateMachineAccessPoint._debug('    - communications enabled')
        else:
            if self.dccEnableDisable == 'disable':
                if _debug:
                    StateMachineAccessPoint._debug('    - communications disabled')
                return
            if self.dccEnableDisable == 'disableInitiation':
                if _debug:
                    StateMachineAccessPoint._debug('    - initiation disabled')
                if apdu.apduType == 1 and apdu.apduService == 0:
                    if _debug:
                        StateMachineAccessPoint._debug('    - continue with I-Am')
                else:
                    if _debug:
                        StateMachineAccessPoint._debug('    - not an I-Am')
                    return
        if isinstance(apdu, UnconfirmedRequestPDU):
            self.request(apdu)
        elif isinstance(apdu, ConfirmedRequestPDU):
            if apdu.apduInvokeID is None:
                apdu.apduInvokeID = self.get_next_invoke_id(apdu.pduDestination)
            else:
                for tr in self.clientTransactions:
                    if apdu.apduInvokeID == tr.invokeID and apdu.pduDestination == tr.pdu_address:
                        raise RuntimeError('invoke ID in use')

            if apdu.pduDestination.addrType != Address.localStationAddr and apdu.pduDestination.addrType != Address.remoteStationAddr:
                StateMachineAccessPoint._warning('%s is not a local or remote station', apdu.pduDestination)
            tr = ClientSSM(self, apdu.pduDestination)
            if _debug:
                StateMachineAccessPoint._debug('    - client segmentation state machine: %r', tr)
            self.clientTransactions.append(tr)
            tr.indication(apdu)
        else:
            raise RuntimeError('invalid APDU (9)')
        return

    def sap_confirmation(self, apdu):
        """This function is called when the application is responding
        to a request, the apdu may be a simple ack, complex ack, error, reject or abort."""
        if _debug:
            StateMachineAccessPoint._debug('sap_confirmation %r', apdu)
        if isinstance(apdu, SimpleAckPDU) or isinstance(apdu, ComplexAckPDU) or isinstance(apdu, ErrorPDU) or isinstance(apdu, RejectPDU) or isinstance(apdu, AbortPDU):
            for tr in self.serverTransactions:
                if apdu.apduInvokeID == tr.invokeID and apdu.pduDestination == tr.pdu_address:
                    break
            else:
                return

            tr.confirmation(apdu)
        else:
            raise RuntimeError('invalid APDU (10)')


@bacpypes_debugging
class ApplicationServiceAccessPoint(ApplicationServiceElement, ServiceAccessPoint):

    def __init__(self, aseID=None, sapID=None):
        if _debug:
            ApplicationServiceAccessPoint._debug('__init__ aseID=%r sapID=%r', aseID, sapID)
        ApplicationServiceElement.__init__(self, aseID)
        ServiceAccessPoint.__init__(self, sapID)

    def indication(self, apdu):
        if _debug:
            ApplicationServiceAccessPoint._debug('indication %r', apdu)
        if isinstance(apdu, ConfirmedRequestPDU):
            error_found = None
            atype = confirmed_request_types.get(apdu.apduService)
            if not atype:
                if _debug:
                    ApplicationServiceAccessPoint._debug('    - no confirmed request decoder')
                error_found = UnrecognizedService()
            if not error_found:
                try:
                    xpdu = atype()
                    xpdu.decode(apdu)
                except RejectException as err:
                    ApplicationServiceAccessPoint._debug('    - decoding reject: %r', err)
                    error_found = err
                except AbortException as err:
                    ApplicationServiceAccessPoint._debug('    - decoding abort: %r', err)
                    error_found = err

            if not error_found:
                if _debug:
                    ApplicationServiceAccessPoint._debug('    - no decoding error')
                try:
                    self.sap_request(xpdu)
                except RejectException as err:
                    ApplicationServiceAccessPoint._debug('    - execution reject: %r', err)
                    error_found = err
                except AbortException as err:
                    ApplicationServiceAccessPoint._debug('    - execution abort: %r', err)
                    error_found = err

            if isinstance(error_found, RejectException):
                if _debug:
                    ApplicationServiceAccessPoint._debug('    - reject exception: %r', error_found)
                reject_pdu = RejectPDU(reason=error_found.rejectReason)
                reject_pdu.set_context(apdu)
                if _debug:
                    ApplicationServiceAccessPoint._debug('    - reject_pdu: %r', reject_pdu)
                self.response(reject_pdu)
            elif isinstance(error_found, AbortException):
                if _debug:
                    ApplicationServiceAccessPoint._debug('    - abort exception: %r', error_found)
                abort_pdu = AbortPDU(reason=error_found.abortReason)
                abort_pdu.set_context(apdu)
                if _debug:
                    ApplicationServiceAccessPoint._debug('    - abort_pdu: %r', abort_pdu)
                self.response(abort_pdu)
        elif isinstance(apdu, UnconfirmedRequestPDU):
            atype = unconfirmed_request_types.get(apdu.apduService)
            if not atype:
                if _debug:
                    ApplicationServiceAccessPoint._debug('    - no unconfirmed request decoder')
                return
            try:
                xpdu = atype()
                xpdu.decode(apdu)
            except RejectException as err:
                ApplicationServiceAccessPoint._debug('    - decoding reject: %r', err)
                return
            except AbortException as err:
                ApplicationServiceAccessPoint._debug('    - decoding abort: %r', err)
                return

            try:
                self.sap_request(xpdu)
            except RejectException as err:
                ApplicationServiceAccessPoint._debug('    - execution reject: %r', err)
            except AbortException as err:
                ApplicationServiceAccessPoint._debug('    - execution abort: %r', err)

        elif _debug:
            ApplicationServiceAccessPoint._debug('    - unknown PDU type?!')
        return

    def sap_indication(self, apdu):
        if _debug:
            ApplicationServiceAccessPoint._debug('sap_indication %r', apdu)
        if isinstance(apdu, ConfirmedRequestPDU):
            try:
                xpdu = ConfirmedRequestPDU()
                apdu.encode(xpdu)
                apdu._xpdu = xpdu
            except Exception as err:
                ApplicationServiceAccessPoint._exception('confirmed request encoding error: %r', err)
                return

        elif isinstance(apdu, UnconfirmedRequestPDU):
            try:
                xpdu = UnconfirmedRequestPDU()
                apdu.encode(xpdu)
                apdu._xpdu = xpdu
            except Exception as err:
                ApplicationServiceAccessPoint._exception('unconfirmed request encoding error: %r', err)
                return

        else:
            if _debug:
                ApplicationServiceAccessPoint._debug('    - unknown PDU type?!')
            return
        if _debug:
            ApplicationServiceAccessPoint._debug('    - xpdu %r', xpdu)
        self.request(xpdu)
        if isinstance(apdu, ConfirmedRequestPDU) and apdu.apduInvokeID is None:
            if _debug:
                ApplicationServiceAccessPoint._debug('    - pass invoke ID upstream %r', xpdu.apduInvokeID)
            apdu.apduInvokeID = xpdu.apduInvokeID
        return

    def confirmation(self, apdu):
        if _debug:
            ApplicationServiceAccessPoint._debug('confirmation %r', apdu)
        if isinstance(apdu, SimpleAckPDU):
            xpdu = apdu
        elif isinstance(apdu, ComplexAckPDU):
            atype = complex_ack_types.get(apdu.apduService)
            if not atype:
                if _debug:
                    ApplicationServiceAccessPoint._debug('    - no complex ack decoder')
                return
            try:
                xpdu = atype()
                xpdu.decode(apdu)
            except Exception as err:
                ApplicationServiceAccessPoint._exception('complex ack decoding error: %r', err)
                return

        elif isinstance(apdu, ErrorPDU):
            atype = error_types.get(apdu.apduService)
            if not atype:
                if _debug:
                    ApplicationServiceAccessPoint._debug('    - no special error decoder')
                atype = Error
            try:
                xpdu = atype()
                xpdu.decode(apdu)
            except Exception as err:
                ApplicationServiceAccessPoint._exception('error PDU decoding error: %r', err)
                xpdu = Error(errorClass=0, errorCode=0)

        elif isinstance(apdu, RejectPDU):
            xpdu = apdu
        elif isinstance(apdu, AbortPDU):
            xpdu = apdu
        else:
            if _debug:
                ApplicationServiceAccessPoint._debug('    - unknown PDU type')
            return
        if _debug:
            ApplicationServiceAccessPoint._debug('    - xpdu %r', xpdu)
        self.sap_response(xpdu)

    def sap_confirmation(self, apdu):
        if _debug:
            ApplicationServiceAccessPoint._debug('sap_confirmation %r', apdu)
        if isinstance(apdu, SimpleAckPDU):
            xpdu = apdu
        elif isinstance(apdu, ComplexAckPDU):
            xpdu = ComplexAckPDU()
            apdu.encode(xpdu)
        elif isinstance(apdu, ErrorPDU):
            xpdu = ErrorPDU()
            apdu.encode(xpdu)
        elif isinstance(apdu, RejectPDU):
            xpdu = apdu
        elif isinstance(apdu, AbortPDU):
            xpdu = apdu
        else:
            if _debug:
                ApplicationServiceAccessPoint._debug('    - unknown PDU type')
            return
        if _debug:
            ApplicationServiceAccessPoint._debug('    - xpdu %r', xpdu)
        self.response(xpdu)