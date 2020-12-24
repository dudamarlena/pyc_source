# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/smpplib/pdu.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 9987 bytes
"""PDU module"""
from __future__ import absolute_import
from struct import pack, unpack
SMPP_ESME_ROK = 0
SMPP_ESME_RINVMSGLEN = 1
SMPP_ESME_RINVCMDLEN = 2
SMPP_ESME_RINVCMDID = 3
SMPP_ESME_RINVBNDSTS = 4
SMPP_ESME_RALYBND = 5
SMPP_ESME_RINVPRTFLG = 6
SMPP_ESME_RINVREGDLVFLG = 7
SMPP_ESME_RSYSERR = 8
SMPP_ESME_RINVSRCADR = 10
SMPP_ESME_RINVDSTADR = 11
SMPP_ESME_RINVMSGID = 12
SMPP_ESME_RBINDFAIL = 13
SMPP_ESME_RINVPASWD = 14
SMPP_ESME_RINVSYSID = 15
SMPP_ESME_RCANCELFAIL = 17
SMPP_ESME_RREPLACEFAIL = 19
SMPP_ESME_RMSGQFUL = 20
SMPP_ESME_RINVSERTYP = 21
SMPP_ESME_RINVNUMDESTS = 51
SMPP_ESME_RINVDLNAME = 52
SMPP_ESME_RINVDESTFLAG = 64
SMPP_ESME_RINVSUBREP = 66
SMPP_ESME_RINVESMCLASS = 67
SMPP_ESME_RCNTSUBDL = 68
SMPP_ESME_RSUBMITFAIL = 69
SMPP_ESME_RINVSRCTON = 72
SMPP_ESME_RINVSRCNPI = 73
SMPP_ESME_RINVDSTTON = 80
SMPP_ESME_RINVDSTNPI = 81
SMPP_ESME_RINVSYSTYP = 83
SMPP_ESME_RINVREPFLAG = 84
SMPP_ESME_RINVNUMMSGS = 85
SMPP_ESME_RTHROTTLED = 88
SMPP_ESME_RINVSCHED = 97
SMPP_ESME_RINVEXPIRY = 98
SMPP_ESME_RINVDFTMSGID = 99
SMPP_ESME_RX_T_APPN = 100
SMPP_ESME_RX_P_APPN = 101
SMPP_ESME_RX_R_APPN = 102
SMPP_ESME_RQUERYFAIL = 103
SMPP_ESME_RINVOPTPARSTREAM = 192
SMPP_ESME_ROPTPARNOTALLWD = 193
SMPP_ESME_RINVPARLEN = 194
SMPP_ESME_RMISSINGOPTPARAM = 195
SMPP_ESME_RINVOPTPARAMVAL = 196
SMPP_ESME_RDELIVERYFAILURE = 254
SMPP_ESME_RUNKNOWNERR = 255
descs = {SMPP_ESME_ROK: 'No Error', 
 SMPP_ESME_RINVMSGLEN: 'Message Length is invalid', 
 SMPP_ESME_RINVCMDLEN: 'Command Length is invalid', 
 SMPP_ESME_RINVCMDID: 'Invalid Command ID', 
 SMPP_ESME_RINVBNDSTS: 'Incorrect BIND Status for given command', 
 SMPP_ESME_RALYBND: 'ESME Already in Bound State', 
 SMPP_ESME_RINVPRTFLG: 'Invalid Priority Flag', 
 SMPP_ESME_RINVREGDLVFLG: '<Desc Not Set>', 
 SMPP_ESME_RSYSERR: 'System Error', 
 SMPP_ESME_RINVSRCADR: 'Invalid Source Address', 
 SMPP_ESME_RINVDSTADR: 'Invalid Destination Address', 
 SMPP_ESME_RINVMSGID: 'Invalid Message ID', 
 SMPP_ESME_RBINDFAIL: 'Bind Failed', 
 SMPP_ESME_RINVPASWD: 'Invalid Password', 
 SMPP_ESME_RINVSYSID: 'Invalid System ID', 
 SMPP_ESME_RCANCELFAIL: 'Cancel SM Failed', 
 SMPP_ESME_RREPLACEFAIL: 'Replace SM Failed', 
 SMPP_ESME_RMSGQFUL: 'Message Queue is full', 
 SMPP_ESME_RINVSERTYP: 'Invalid Service Type', 
 SMPP_ESME_RINVNUMDESTS: 'Invalid number of destinations', 
 SMPP_ESME_RINVDLNAME: 'Invalid Distribution List name', 
 SMPP_ESME_RINVDESTFLAG: 'Invalid Destination Flag (submit_multi)', 
 SMPP_ESME_RINVSUBREP: 'Invalid Submit With Replace request (replace_if_present_flag set)', 
 SMPP_ESME_RINVESMCLASS: 'Invalid esm_class field data', 
 SMPP_ESME_RCNTSUBDL: 'Cannot submit to Distribution List', 
 SMPP_ESME_RSUBMITFAIL: 'submit_sm or submit_multi failed', 
 SMPP_ESME_RINVSRCTON: 'Invalid Source address TON', 
 SMPP_ESME_RINVSRCNPI: 'Invalid Source address NPI', 
 SMPP_ESME_RINVDSTTON: 'Invalid Destination address TON', 
 SMPP_ESME_RINVDSTNPI: 'Invalid Destination address NPI', 
 SMPP_ESME_RINVSYSTYP: 'Invalid system_type field', 
 SMPP_ESME_RINVREPFLAG: 'Invalid replace_if_present flag', 
 SMPP_ESME_RINVNUMMSGS: 'Invalid number of messages', 
 SMPP_ESME_RTHROTTLED: 'Throttling error (ESME has exceeded allowed message limits)', 
 SMPP_ESME_RINVSCHED: 'Invalid Scheduled Delivery Time', 
 SMPP_ESME_RINVEXPIRY: 'Invalid message validity period (Expiry Time)', 
 SMPP_ESME_RINVDFTMSGID: 'Predefined Message is invalid or not found', 
 SMPP_ESME_RX_T_APPN: 'ESME received Temporary App Error Code', 
 SMPP_ESME_RX_P_APPN: 'ESME received Permanent App Error Code', 
 SMPP_ESME_RX_R_APPN: 'ESME received Reject Message Error Code', 
 SMPP_ESME_RQUERYFAIL: 'query_sm request failed', 
 SMPP_ESME_RINVOPTPARSTREAM: 'Error in the optional part of the PDU body', 
 SMPP_ESME_ROPTPARNOTALLWD: 'Optional Parameter not allowed', 
 SMPP_ESME_RINVPARLEN: 'Invalid Parameter Length', 
 SMPP_ESME_RMISSINGOPTPARAM: 'Expected Optional Parameter missing', 
 SMPP_ESME_RINVOPTPARAMVAL: 'Invalid Optional Parameter Value', 
 SMPP_ESME_RDELIVERYFAILURE: 'Delivery Failure (used data_sm_resp)', 
 SMPP_ESME_RUNKNOWNERR: 'Unknown Error'}
sequence = 0

def factory(command_name, **args):
    """Return instance of a specific command class"""
    from .command import BindTransmitter, BindTransmitterResp, BindReceiver, BindReceiverResp, BindTransceiver, BindTransceiverResp, DataSM, DataSMResp, GenericNAck, SubmitSM, SubmitSMResp, DeliverSM, DeliverSMResp, Unbind, UnbindResp, EnquireLink, EnquireLinkResp
    cc = None
    if command_name == 'bind_transmitter':
        cc = BindTransmitter
    else:
        if command_name == 'bind_transmitter_resp':
            cc = BindTransmitterResp
        elif command_name == 'bind_receiver':
            cc = BindReceiver
        else:
            if command_name == 'bind_receiver_resp':
                cc = BindReceiverResp
    if command_name == 'bind_transceiver':
        cc = BindTransceiver
    else:
        if command_name == 'bind_transceiver_resp':
            cc = BindTransceiverResp
        else:
            if command_name == 'data_sm':
                cc = DataSM
            else:
                if command_name == 'data_sm_resp':
                    cc = DataSMResp
                else:
                    if command_name == 'generic_nack':
                        cc = GenericNAck
                    else:
                        if command_name == 'submit_sm':
                            cc = SubmitSM
                        else:
                            if command_name == 'submit_sm_resp':
                                cc = SubmitSMResp
                            else:
                                if command_name == 'deliver_sm':
                                    cc = DeliverSM
                                else:
                                    if command_name == 'deliver_sm_resp':
                                        cc = DeliverSMResp
                                    else:
                                        if command_name == 'unbind':
                                            cc = Unbind
                                        else:
                                            if command_name == 'unbind_resp':
                                                cc = UnbindResp
                                            else:
                                                if command_name == 'enquire_link':
                                                    cc = EnquireLink
                                                else:
                                                    if command_name == 'enquire_link_resp':
                                                        cc = EnquireLinkResp
                                                    if not cc:
                                                        raise ValueError("Command '{}' is not supported".format(command_name))
                                                    return cc(command_name, **args)


class PDU:
    __doc__ = 'PDU class'
    length = 0
    command = None
    status = None

    def __init__(self, **args):
        (self.__dict__.update)(**args)

    def get_sequence(self):
        """Return global sequence number"""
        global sequence
        return sequence

    sequence = property(get_sequence)

    def is_vendor(self):
        """Return True if this is a vendor PDU, False otherwise"""
        return hasattr(self, 'vendor')

    def is_request(self):
        """Return True if this is a request PDU, False otherwise"""
        return not self.is_response()

    def is_response(self):
        """Return True if this is a response PDU, False otherwise"""
        from .command import get_command_code
        if get_command_code(self.command) & 2147483648:
            return True
        return False

    def is_error(self):
        """Return True if this is an error response, False otherwise"""
        if self.status != SMPP_ESME_ROK:
            return True
        return False

    def get_status_desc(self, status=None):
        """Return status description"""
        if status is None:
            status = self.status
        try:
            desc = descs[status]
        except KeyError:
            return 'Description for status 0x{} not found!'.format(status)
        else:
            return desc

    def parse(self, data):
        """Parse raw PDU"""
        header = data[0:16]
        chunks = unpack('>LLLL', header)
        self.length = chunks[0]
        self.command = self.extract_command(data)
        self.status = chunks[2]
        self.sequence = chunks[3]
        if len(data) > 16:
            self.parse_params(data[16:])

    @staticmethod
    def extract_command(pdu):
        """Extract command from a PDU"""
        code = unpack('>L', pdu[4:8])[0]
        from .command import get_command_name
        return get_command_name(code)

    def _unpack(self, format, data):
        """Unpack values. Uses unpack."""
        return unpack(format, data)

    def generate(self):
        """Generate raw PDU"""
        body = self.generate_params()
        self._length = len(body) + 16
        from .command import get_command_code
        command_code = get_command_code(self.command)
        header = pack('>LLLL', self._length, command_code, self.status, self.sequence)
        return header + body