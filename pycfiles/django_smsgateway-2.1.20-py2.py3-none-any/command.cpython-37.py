# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/smpplib/command.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 33217 bytes
"""SMPP Commands module"""
from __future__ import absolute_import
from struct import pack, unpack
from .smpp import UnknownCommandError, next_seq
from .pdu import PDU, SMPP_ESME_ROK
from .ptypes import ostr, flag
from six.moves import map
SMPP_TON_UNK = 0
SMPP_TON_INTL = 1
SMPP_TON_NATNL = 2
SMPP_TON_NWSPEC = 3
SMPP_TON_SBSCR = 4
SMPP_TON_ALNUM = 5
SMPP_TON_ABBREV = 6
SMPP_NPI_UNK = 0
SMPP_NPI_ISDN = 1
SMPP_NPI_DATA = 3
SMPP_NPI_TELEX = 4
SMPP_NPI_LNDMBL = 6
SMPP_NPI_NATNL = 8
SMPP_NPI_PRVT = 9
SMPP_NPI_ERMES = 10
SMPP_NPI_IP = 14
SMPP_NPI_WAP = 18
SMPP_ENCODING_DEFAULT = 0
SMPP_ENCODING_IA5 = 1
SMPP_ENCODING_BINARY = 2
SMPP_ENCODING_ISO88591 = 3
SMPP_ENCODING_BINARY2 = 4
SMPP_ENCODING_JIS = 5
SMPP_ENCODING_ISO88595 = 6
SMPP_ENCODING_ISO88598 = 7
SMPP_ENCODING_ISO10646 = 8
SMPP_ENCODING_PICTOGRAM = 9
SMPP_ENCODING_ISO2022JP = 10
SMPP_ENCODING_EXTJIS = 13
SMPP_ENCODING_KSC5601 = 14
SMPP_LANG_DEFAULT = 0
SMPP_LANG_EN = 1
SMPP_LANG_FR = 2
SMPP_LANG_ES = 3
SMPP_LANG_DE = 4
SMPP_MSGMODE_DEFAULT = 0
SMPP_MSGMODE_DATAGRAM = 1
SMPP_MSGMODE_FORWARD = 2
SMPP_MSGMODE_STOREFORWARD = 3
SMPP_MSGTYPE_DEFAULT = 0
SMPP_MSGTYPE_DELIVERYACK = 8
SMPP_MSGTYPE_USERACK = 16
SMPP_GSMFEAT_NONE = 0
SMPP_GSMFEAT_UDHI = 64
SMPP_GSMFEAT_REPLYPATH = 128
SMPP_GSMFEAT_UDHIREPLYPATH = 192
SMPP_PID_DEFAULT = 0
SMPP_PID_RIP = 65
SMPP_UDHIEIE_CONCATENATED = 0
SMPP_UDHIEIE_SPECIAL = 1
SMPP_UDHIEIE_RESERVED = 2
SMPP_UDHIEIE_PORT8 = 4
SMPP_UDHIEIE_PORT16 = 4
SMPP_VERSION_33 = 51
SMPP_VERSION_34 = 52
commands = {'generic_nack':2147483648, 
 'bind_receiver':1, 
 'bind_receiver_resp':2147483649, 
 'bind_transmitter':2, 
 'bind_transmitter_resp':2147483650, 
 'query_sm':3, 
 'query_sm_resp':2147483651, 
 'submit_sm':4, 
 'submit_sm_resp':2147483652, 
 'deliver_sm':5, 
 'deliver_sm_resp':2147483653, 
 'unbind':6, 
 'unbind_resp':2147483654, 
 'replace_sm':7, 
 'replace_sm_resp':2147483655, 
 'cancel_sm':8, 
 'cancel_sm_resp':2147483656, 
 'bind_transceiver':9, 
 'bind_transceiver_resp':2147483657, 
 'outbind':11, 
 'enquire_link':21, 
 'enquire_link_resp':2147483669, 
 'submit_multi':33, 
 'submit_multi_resp':2147483681, 
 'alert_notification':258, 
 'data_sm':259, 
 'data_sm_resp':2147483907}
optional_params = {'dest_addr_subunit':5, 
 'dest_network_type':6, 
 'dest_bearer_type':7, 
 'dest_telematics_id':8, 
 'source_addr_subunit':13, 
 'source_network_type':14, 
 'source_bearer_type':15, 
 'source_telematics_id':16, 
 'qos_time_to_live':23, 
 'payload_type':25, 
 'additional_status_info_text':29, 
 'receipted_message_id':30, 
 'ms_msg_wait_facilities':48, 
 'privacy_indicator':513, 
 'source_subaddress':514, 
 'dest_subaddress':515, 
 'user_message_reference':516, 
 'user_response_code':517, 
 'source_port':522, 
 'destination_port':523, 
 'sar_msg_ref_num':524, 
 'language_indicator':525, 
 'sar_total_segments':526, 
 'sar_segment_seqnum':527, 
 'sc_interface_version':528, 
 'callback_num_pres_ind':770, 
 'callback_num_atag':771, 
 'number_of_messages':772, 
 'callback_num':897, 
 'dpf_result':1056, 
 'set_dpf':1057, 
 'ms_availability_status':1058, 
 'network_error_code':1059, 
 'message_payload':1060, 
 'delivery_failure_reason':1061, 
 'more_messages_to_send':1062, 
 'message_state':1063, 
 'ussd_service_op':1281, 
 'display_time':4609, 
 'sms_signal':4611, 
 'ms_validity':4612, 
 'alert_on_message_delivery':4876, 
 'its_reply_type':4992, 
 'its_session_info':4995}

def get_command_name(code):
    """Return command name by given code. If code is unknown, raise
    UnkownCommandError exception"""
    try:
        return list(commands.keys())[list(commands.values()).index(code)]
    except ValueError:
        raise UnknownCommandError("Unknown SMPP command code '0x{}'".format(code))


def get_command_code(name):
    """Return command code by given command name. If name is unknown,
    raise UnknownCommandError exception"""
    try:
        return commands[name]
    except KeyError:
        raise UnknownCommandError("Unknown SMPP command name '{}'".format(name))


def get_optional_name(code):
    """Return optional_params name by given code. If code is unknown, raise
    UnkownCommandError exception"""
    try:
        return list(optional_params.keys())[list(optional_params.values()).index(code)]
    except ValueError:
        raise UnknownCommandError("Unknown SMPP command code '0x{}'".format(code))


def get_optional_code(name):
    """Return optional_params code by given command name. If name is unknown,
    raise UnknownCommandError exception"""
    try:
        return optional_params[name]
    except KeyError:
        raise UnknownCommandError("Unknown SMPP command name '{}'".format(name))


class Command(PDU):
    __doc__ = 'SMPP PDU Command class'
    params = {}

    def __init__(self, command, **args):
        """Initialize"""
        self.command = command
        if args.get('sequence') is None:
            self.sequence_number = next_seq()
        self.status = SMPP_ESME_ROK
        (self._set_vars)(**args)

    def _print_dict(self):
        pass

    def _set_vars(self, **args):
        for key, value in args.items():
            if not hasattr(self, key) or getattr(self, key) is None:
                setattr(self, key, value)

    def generate_params(self):
        """Generate binary data from the object"""
        if hasattr(self, 'prep'):
            if callable(self.prep):
                self.prep()
        body = ''
        for field in self.params_order:
            param = self.params[field]
            if self.field_is_optional(field):
                if param.type is int:
                    value = self._generate_int_tlv(field)
                    if value:
                        body += value
                    else:
                        if param.type is str:
                            value = self._generate_string_tlv(field)
                            if value:
                                body += value
                        elif param.type is ostr:
                            value = self._generate_ostring_tlv(field)
                            if value:
                                body += value
                elif param.type is int:
                    value = self._generate_int(field)
                    body += value
                elif param.type is str:
                    value = self._generate_string(field)
                    body += value
                elif param.type is ostr:
                    value = self._generate_ostring(field)
                    if value:
                        body += value

        return body

    def _generate_opt_header(self, field):
        """Generate a header for an optional parameter"""
        raise NotImplementedError('Vendors not supported')

    def _generate_int(self, field):
        """Generate integer value"""
        fmt = self._pack_format(field)
        data = getattr(self, field)
        if data:
            return pack(fmt, data)
        return chr(0)

    def _generate_string(self, field):
        """Generate string value"""
        field_value = getattr(self, field)
        if hasattr(self.params[field], 'size'):
            size = self.params[field].size
            value = field_value.ljust(size, chr(0))
        else:
            if hasattr(self.params[field], 'max'):
                if len(field_value or '') > self.params[field].max:
                    field_value = field_value[0:self.params[field].max - 1]
                elif field_value:
                    value = field_value + chr(0)
                else:
                    value = chr(0)
        setattr(self, field, field_value)
        return value

    def _generate_ostring(self, field):
        """Generate octet string value (no null terminator)"""
        value = getattr(self, field)
        if value:
            return value
        return

    def _generate_int_tlv(self, field):
        """Generate integer value"""
        fmt = self._pack_format(field)
        data = getattr(self, field)
        field_code = get_optional_code(field)
        field_length = self.params[field].size
        value = None
        if data:
            value = pack('>HH' + fmt, field_code, field_length, data)
        return value

    def _generate_string_tlv(self, field):
        """Generate string value"""
        field_value = getattr(self, field)
        field_code = get_optional_code(field)
        if hasattr(self.params[field], 'size'):
            size = self.params[field].size
            fvalue = field_value.ljust(size, chr(0))
            value = pack('>HH', field_code, size) + fvalue
        else:
            if hasattr(self.params[field], 'max'):
                if len(field_value or '') > self.params[field].max:
                    field_value = field_value[0:self.params[field].max - 1]
                elif field_value:
                    field_length = len(field_value)
                    fvalue = field_value + chr(0)
                    value = pack('>HH', field_code, field_length) + fvalue
                else:
                    value = None
        return value

    def _generate_ostring_tlv(self, field):
        """Generate octet string value (no null terminator)"""
        try:
            field_value = getattr(self, field)
        except:
            return
            field_code = get_optional_code(field)
            value = None
            if field_value:
                field_length = len(field_value)
                value = pack('>HH', field_code, field_length) + field_value
            return value

    def _pack_format(self, field):
        """Return format type"""
        if self.params[field].size == 1:
            return 'B'
        if self.params[field].size == 2:
            return 'H'
        if self.params[field].size == 3:
            return 'L'

    def _parse_int(self, field, data, pos):
        """Parse fixed-length chunk from a PDU.
        Return (data, pos) tuple."""
        size = self.params[field].size
        field_value = getattr(self, field)
        unpacked_data = self._unpack(self._pack_format(field), data[pos:pos + size])
        field_value = ''.join(map(str, unpacked_data))
        setattr(self, field, field_value)
        pos += size
        return (
         data, pos)

    def _parse_string(self, field, data, pos):
        """Parse variable-length string from a PDU.
        Return (data, pos) tuple."""
        end = data.find(chr(0), pos)
        length = end - pos
        field_value = data[pos:pos + length]
        setattr(self, field, field_value)
        pos += length + 1
        return (
         data, pos)

    def _parse_ostring(self, field, data, pos, length=None):
        """Parse an octet string from a PDU.
        Return (data, pos) tuple."""
        if length is None:
            length_field = self.params[field].len_field
            length = int(getattr(self, length_field))
        setattr(self, field, data[pos:pos + length])
        pos += length
        return (
         data, pos)

    def is_fixed(self, field):
        """Return True if field has fixed length, False otherwise"""
        if hasattr(self.params[field], 'size'):
            return True
        return False

    def parse_params(self, data):
        """Parse data into the object structure"""
        pos = 0
        dlen = len(data)
        for field in self.params_order:
            param = self.params[field]
            if not pos == dlen:
                if self.field_is_optional(field):
                    break
                if param.type is int:
                    data, pos = self._parse_int(field, data, pos)
                elif param.type is str:
                    data, pos = self._parse_string(field, data, pos)
                elif param.type is ostr:
                    data, pos = self._parse_ostring(field, data, pos)

        if pos < dlen:
            self.parse_optional_params(data[pos:])

    def parse_optional_params(self, data):
        """Parse optional parameters.

        Optional parameters have the following format:
            * type (2 bytes)
            * length (2 bytes)
            * value (variable, <length> bytes)
        """
        dlen = len(data)
        pos = 0
        while pos < dlen:
            unpacked_data = unpack('>H', data[pos:pos + 2])
            type_code = int(''.join(map(str, unpacked_data)))
            field = get_optional_name(type_code)
            pos += 2
            length = int(''.join(map(str, unpack('!H', data[pos:pos + 2]))))
            pos += 2
            param = self.params[field]
            if param.type is int:
                data, pos = self._parse_int(field, data, pos)
            elif param.type is str:
                data, pos = self._parse_string(field, data, pos)
            elif param.type is ostr:
                data, pos = self._parse_ostring(field, data, pos, length)

    def field_exists(self, field):
        """Return True if field exists, False otherwise"""
        return hasattr(self.params, field)

    def field_is_optional(self, field):
        """Return True if field is optional, False otherwise"""
        if field in optional_params:
            return True
        if self.is_vendor():
            return False
        return False


class Param:
    __doc__ = 'Command parameter info class'

    def __init__(self, **args):
        """Initialize"""
        if 'type' not in args:
            raise KeyError('Parameter Type not defined')
        if args.get('type') not in [int, str, ostr, flag]:
            raise ValueError('Invalid parameter type: {}'.format(args.get('type')))
        valid_keys = ['type', 'size', 'min', 'max', 'len_field']
        for k in args.keys():
            if k not in valid_keys:
                raise KeyError("Key '{}' not allowed here".format(k))

        self.type = args.get('type')
        if 'size' in args:
            self.size = args.get('size')
        if 'min' in args:
            self.min = args.get('min')
        if 'max' in args:
            self.max = args.get('max')
        if 'len_field' in args:
            self.len_field = args.get('len_field')


class BindTransmitter(Command):
    __doc__ = 'Bind as a transmitter command'
    params = {'system_id':Param(type=str, max=16), 
     'password':Param(type=str, max=9), 
     'system_type':Param(type=str, max=13), 
     'interface_version':Param(type=int, size=1), 
     'addr_ton':Param(type=int, size=1), 
     'addr_npi':Param(type=int, size=1), 
     'address_range':Param(type=str, max=41)}
    params_order = ('system_id', 'password', 'system_type', 'interface_version', 'addr_ton',
                    'addr_npi', 'address_range')

    def __init__(self, command, **args):
        """Initialize"""
        (Command.__init__)(self, command, **args)
        (self._set_vars)(**{}.fromkeys(list(self.params.keys())))
        self.interface_version = SMPP_VERSION_34


class BindReceiver(BindTransmitter):
    pass


class BindTransceiver(BindTransmitter):
    pass


class BindTransmitterResp(Command):
    __doc__ = 'Response for bind as a transmitter command'
    params = {'system_id':Param(type=str), 
     'sc_interface_version':Param(type=int, size=1)}
    params_order = ('system_id', 'sc_interface_version')

    def __init__(self, command):
        """Initialize"""
        Command.__init__(self, command)
        (self._set_vars)(**{}.fromkeys(list(self.params.keys())))


class BindReceiverResp(BindTransmitterResp):
    pass


class BindTransceiverResp(BindTransmitterResp):
    pass


class DataSM(Command):
    __doc__ = 'data_sm command is used to transfer data between SMSC and the ESME'
    params = {'service_type':Param(type=str, max=6), 
     'source_addr_ton':Param(type=int, size=1), 
     'source_addr_npi':Param(type=int, size=1), 
     'source_addr':Param(type=str, max=21), 
     'dest_addr_ton':Param(type=int, size=1), 
     'dest_addr_npi':Param(type=int, size=1), 
     'destination_addr':Param(type=str, max=21), 
     'esm_class':Param(type=int, size=1), 
     'registered_delivery':Param(type=int, size=1), 
     'data_coding':Param(type=int, size=1), 
     'source_port':Param(type=int, size=2), 
     'source_addr_subunit':Param(type=int, size=1), 
     'source_network_type':Param(type=int, size=1), 
     'source_bearer_type':Param(type=int, size=1), 
     'source_telematics_id':Param(type=int, size=2), 
     'destination_port':Param(type=int, size=2), 
     'dest_addr_subunit':Param(type=int, size=1), 
     'dest_network_type':Param(type=int, size=1), 
     'dest_bearer_type':Param(type=int, size=1), 
     'dest_telematics_id':Param(type=int, size=2), 
     'sar_msg_ref_num':Param(type=int, size=2), 
     'sar_total_segments':Param(type=int, size=1), 
     'sar_segment_seqnum':Param(type=int, size=1), 
     'more_messages_to_send':Param(type=int, size=1), 
     'qos_time_to_live':Param(type=int, size=4), 
     'payload_type':Param(type=int, size=1), 
     'message_payload':Param(type=ostr, max=260), 
     'receipted_message_id':Param(type=str, max=65), 
     'message_state':Param(type=int, size=1), 
     'network_error_code':Param(type=ostr, size=3), 
     'user_message_reference':Param(type=int, size=2), 
     'privacy_indicator':Param(type=int, size=1), 
     'callback_num':Param(type=str, min=4, max=19), 
     'callback_num_pres_ind':Param(type=int, size=1), 
     'callback_num_atag':Param(type=str, max=65), 
     'source_subaddress':Param(type=str, min=2, max=23), 
     'dest_subaddress':Param(type=str, min=2, max=23), 
     'user_response_code':Param(type=int, size=1), 
     'display_time':Param(type=int, size=1), 
     'sms_signal':Param(type=int, size=2), 
     'ms_validity':Param(type=int, size=1), 
     'ms_msg_wait_facilities':Param(type=int, size=1), 
     'number_of_messages':Param(type=int, size=1), 
     'alert_on_msg_delivery':Param(type=flag), 
     'language_indicator':Param(type=int, size=1), 
     'its_reply_type':Param(type=int, size=1), 
     'its_session_info':Param(type=int, size=2)}
    params_order = ('service_type', 'source_addr_ton', 'source_addr_npi', 'source_addr',
                    'dest_addr_ton', 'dest_addr_npi', 'destination_addr', 'esm_class',
                    'registered_delivery', 'data_codingsource_port', 'source_addr_subunit',
                    'source_network_type', 'source_bearer_type', 'source_telematics_id',
                    'destination_port', 'dest_addr_subunit', 'dest_network_type',
                    'dest_bearer_type', 'dest_telematics_id', 'sar_msg_ref_num',
                    'sar_total_segments', 'sar_segment_seqnum', 'more_messages_to_send',
                    'qos_time_to_live', 'payload_type', 'message_payload', 'receipted_message_id',
                    'message_state', 'network_error_code', 'user_message_reference',
                    'privacy_indicator', 'callback_num', 'callback_num_pres_ind',
                    'callback_num_atag', 'source_subaddress', 'dest_subaddress',
                    'user_response_code', 'display_time', 'sms_signal', 'ms_validity',
                    'ms_msg_wait_facilities', 'number_of_messages', 'alert_on_message_delivery',
                    'language_indicator', 'its_reply_type', 'its_session_info')

    def __init__(self, command):
        """Initialize"""
        Command.__init__(self, command)
        (self._set_vars)(**{}.fromkeys(list(self.params.keys())))


class DataSMResp(Command):
    __doc__ = 'Reponse command for data_sm'
    message_id = None
    delivery_failure_reason = None
    network_error_code = None
    additional_status_info_text = None
    dpf_result = None


class GenericNAck(Command):
    __doc__ = 'General Negative Acknowledgement class'
    _defs = []


class SubmitSM(Command):
    __doc__ = 'submit_sm command class\n\n    This command is used by an ESME to submit short message to the SMSC.\n    submit_sm PDU does not support the transaction mode.'
    service_type = None
    source_addr_ton = None
    source_addr_npi = None
    source_addr = None
    dest_addr_ton = None
    dest_addr_npi = None
    destination_addr = None
    esm_class = None
    protocol_id = None
    priority_flag = None
    schedule_delivery_time = None
    validity_period = None
    registered_delivery = None
    replace_if_present_flag = None
    data_coding = None
    sm_default_msg_id = None
    sm_length = 0
    short_message = None
    params = {'service_type':Param(type=str, max=6), 
     'source_addr_ton':Param(type=int, size=1), 
     'source_addr_npi':Param(type=int, size=1), 
     'source_addr':Param(type=str, max=21), 
     'dest_addr_ton':Param(type=int, size=1), 
     'dest_addr_npi':Param(type=int, size=1), 
     'destination_addr':Param(type=str, max=21), 
     'esm_class':Param(type=int, size=1), 
     'protocol_id':Param(type=int, size=1), 
     'priority_flag':Param(type=int, size=1), 
     'schedule_delivery_time':Param(type=str, max=17), 
     'validity_period':Param(type=str, max=17), 
     'registered_delivery':Param(type=int, size=1), 
     'replace_if_present_flag':Param(type=int, size=1), 
     'data_coding':Param(type=int, size=1), 
     'sm_default_msg_id':Param(type=int, size=1), 
     'sm_length':Param(type=int, size=1), 
     'short_message':Param(type=ostr, max=254, len_field='sm_length'), 
     'user_message_reference':Param(type=int, size=2), 
     'source_port':Param(type=int, size=2), 
     'source_addr_subunit':Param(type=int, size=2), 
     'destination_port':Param(type=int, size=2), 
     'dest_addr_subunit':Param(type=int, size=1), 
     'sar_msg_ref_num':Param(type=int, size=2), 
     'sar_total_segments':Param(type=int, size=1), 
     'sar_segment_seqnum':Param(type=int, size=1), 
     'more_messages_to_send':Param(type=int, size=1), 
     'payload_type':Param(type=int, size=1), 
     'message_payload':Param(type=ostr, max=260), 
     'privacy_indicator':Param(type=int, size=1), 
     'callback_num':Param(type=str, min=4, max=19), 
     'callback_num_pres_ind':Param(type=int, size=1), 
     'source_subaddress':Param(type=str, min=2, max=23), 
     'dest_subaddress':Param(type=str, min=2, max=23), 
     'user_response_code':Param(type=int, size=1), 
     'display_time':Param(type=int, size=1), 
     'sms_signal':Param(type=int, size=2), 
     'ms_validity':Param(type=int, size=1), 
     'ms_msg_wait_facilities':Param(type=int, size=1), 
     'number_of_messages':Param(type=int, size=1), 
     'alert_on_message_delivery':Param(type=flag), 
     'language_indicator':Param(type=int, size=1), 
     'its_reply_type':Param(type=int, size=1), 
     'its_session_info':Param(type=int, size=2), 
     'ussd_service_op':Param(type=int, size=1)}
    params_order = ('service_type', 'source_addr_ton', 'source_addr_npi', 'source_addr',
                    'dest_addr_ton', 'dest_addr_npi', 'destination_addr', 'esm_class',
                    'protocol_id', 'priority_flag', 'schedule_delivery_time', 'validity_period',
                    'registered_delivery', 'replace_if_present_flag', 'data_coding',
                    'sm_default_msg_id', 'sm_length', 'short_message', 'user_message_reference',
                    'source_port', 'source_addr_subunit', 'destination_port', 'dest_addr_subunit',
                    'sar_msg_ref_num', 'sar_total_segments', 'sar_segment_seqnum',
                    'more_messages_to_send', 'payload_type', 'message_payload', 'privacy_indicator',
                    'callback_num', 'callback_num_pres_ind', 'source_subaddress',
                    'dest_subaddress', 'user_response_code', 'display_time', 'sms_signal',
                    'ms_validity', 'ms_msg_wait_facilities', 'number_of_messages',
                    'alert_on_message_delivery', 'language_indicator', 'its_reply_type',
                    'its_session_info', 'ussd_service_op')

    def __init__(self, command, **args):
        """Initialize"""
        (Command.__init__)(self, command, **args)
        (self._set_vars)(**{}.fromkeys(list(self.params.keys())))

    def prep(self):
        """Prepare to generate binary data"""
        if self.short_message:
            self.sm_length = len(self.short_message)
            delattr(self, 'message_payload')
        else:
            self.sm_length = 0


class SubmitSMResp(Command):
    __doc__ = 'Response command for submit_sm'
    params = {'message_id': Param(type=str, max=65)}
    params_order = ('message_id', )

    def __init__(self, command):
        """Initialize"""
        Command.__init__(self, command)
        (self._set_vars)(**{}.fromkeys(list(self.params.keys())))


class DeliverSM(SubmitSM):
    __doc__ = 'deliver_sm command class, similar to submit_sm but has different optional params'
    params = {'service_type':Param(type=str, max=6), 
     'source_addr_ton':Param(type=int, size=1), 
     'source_addr_npi':Param(type=int, size=1), 
     'source_addr':Param(type=str, max=21), 
     'dest_addr_ton':Param(type=int, size=1), 
     'dest_addr_npi':Param(type=int, size=1), 
     'destination_addr':Param(type=str, max=21), 
     'esm_class':Param(type=int, size=1), 
     'protocol_id':Param(type=int, size=1), 
     'priority_flag':Param(type=int, size=1), 
     'schedule_delivery_time':Param(type=str, max=17), 
     'validity_period':Param(type=str, max=17), 
     'registered_delivery':Param(type=int, size=1), 
     'replace_if_present_flag':Param(type=int, size=1), 
     'data_coding':Param(type=int, size=1), 
     'sm_default_msg_id':Param(type=int, size=1), 
     'sm_length':Param(type=int, size=1), 
     'short_message':Param(type=ostr, max=254, len_field='sm_length'), 
     'user_message_reference':Param(type=int, size=2), 
     'source_port':Param(type=int, size=2), 
     'destination_port':Param(type=int, size=2), 
     'sar_msg_ref_num':Param(type=int, size=2), 
     'sar_total_segments':Param(type=int, size=1), 
     'sar_segment_seqnum':Param(type=int, size=1), 
     'user_response_code':Param(type=int, size=1), 
     'privacy_indicator':Param(type=int, size=1), 
     'payload_type':Param(type=int, size=1), 
     'message_payload':Param(type=ostr, max=260), 
     'callback_num':Param(type=str, min=4, max=19), 
     'source_subaddress':Param(type=str, min=2, max=23), 
     'dest_subaddress':Param(type=str, min=2, max=23), 
     'language_indicator':Param(type=int, size=1), 
     'its_session_info':Param(type=int, size=2), 
     'network_error_code':Param(type=ostr, size=3), 
     'message_state':Param(type=int, size=1), 
     'receipted_message_id':Param(type=str, max=65)}
    params_order = ('service_type', 'source_addr_ton', 'source_addr_npi', 'source_addr',
                    'dest_addr_ton', 'dest_addr_npi', 'destination_addr', 'esm_class',
                    'protocol_id', 'priority_flag', 'schedule_delivery_time', 'validity_period',
                    'registered_delivery', 'replace_if_present_flag', 'data_coding',
                    'sm_default_msg_id', 'sm_length', 'short_message', 'user_message_reference',
                    'source_port', 'destination_port', 'sar_msg_ref_num', 'sar_total_segments',
                    'sar_segment_seqnum', 'user_response_code', 'privacy_indicator',
                    'payload_type', 'message_payload', 'callback_num', 'source_subaddress',
                    'dest_subaddress', 'language_indicator', 'its_session_info',
                    'network_error_code', 'message_state', 'receipted_message_id')


class DeliverSMResp(SubmitSMResp):
    __doc__ = 'deliver_sm_response response class, same as submit_sm'
    message_id = None


class Unbind(Command):
    __doc__ = 'Unbind command'
    params = {}
    params_order = ()


class UnbindResp(Command):
    __doc__ = 'Unbind response command'
    params = {}
    params_order = ()


class EnquireLink(Command):
    params = {}
    params_order = ()


class EnquireLinkResp(Command):
    params = {}
    params_order = ()