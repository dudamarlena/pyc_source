# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/tnefparse/tnef.py
# Compiled at: 2018-12-01 10:41:34
"""extracts TNEF encoded content from for example winmail.dat attachments.
"""
import logging, os
from .mapi import TNEFMAPI_Attribute, decode_mapi
from .util import typtime, bytes_to_int, checksum, uint32, uint16, uint8
logger = logging.getLogger('tnef-decode')

class TNEFObject(object):
    """a TNEF object that may contain a property and an attachment"""
    PTYPE_CLASS = 1
    PTYPE_TIME = 3
    PTYPE_STRING = 7

    def __init__(self, data, do_checksum=False):
        self.length = len(data)
        self.level = uint8(data, 0)
        self.name = uint16(data, 1)
        self.type = uint16(data, 3)
        self.length = min(self.length, uint32(data, 5) + 11)
        self.data = data[9:self.length - 2]
        att_checksum = uint16(data, self.length - 2)
        if do_checksum:
            calc_checksum = checksum(self.data)
            if calc_checksum != att_checksum:
                logger.warning('Checksum: %s != %s' % (calc_checksum, att_checksum))
        else:
            calc_checksum = att_checksum
        self.good_checksum = calc_checksum == att_checksum

    def __str__(self):
        return "<%s '%s'>" % (self.__class__.__name__, TNEF.codes.get(self.name))


class TNEFAttachment(object):
    """a TNEF attachment"""
    SZMAPI_UNSPECIFIED = 0
    SZMAPI_NULL = 1
    SZMAPI_SHORT = 2
    SZMAPI_INT = 3
    SZMAPI_FLOAT = 4
    SZMAPI_DOUBLE = 5
    SZMAPI_CURRENCY = 6
    SZMAPI_APPTIME = 7
    SZMAPI_ERROR = 10
    SZMAPI_BOOLEAN = 11
    SZMAPI_OBJECT = 13
    SZMAPI_INT8BYTE = 20
    SZMAPI_STRING = 30
    SZMAPI_UNICODE_STRING = 31
    SZMAPI_SYSTIME = 64
    SZMAPI_CLSID = 72
    SZMAPI_BINARY = 258
    SZMAPI_BEATS_THE_HELL_OUTTA_ME = 51
    codes = {SZMAPI_UNSPECIFIED: 'MAPI Unspecified', 
       SZMAPI_NULL: 'MAPI null property', 
       SZMAPI_SHORT: 'MAPI short (signed 16 bits)', 
       SZMAPI_INT: 'MAPI integer (signed 32 bits)', 
       SZMAPI_FLOAT: 'MAPI float (4 bytes)', 
       SZMAPI_DOUBLE: 'MAPI double', 
       SZMAPI_CURRENCY: 'MAPI currency (64 bits)', 
       SZMAPI_APPTIME: 'MAPI application time', 
       SZMAPI_ERROR: 'MAPI error (32 bits)', 
       SZMAPI_BOOLEAN: 'MAPI boolean (16 bits)', 
       SZMAPI_OBJECT: 'MAPI embedded object', 
       SZMAPI_INT8BYTE: 'MAPI 8 byte signed int', 
       SZMAPI_STRING: 'MAPI string', 
       SZMAPI_UNICODE_STRING: 'MAPI unicode-string (null terminated)', 
       SZMAPI_SYSTIME: 'MAPI time (64 bits)', 
       SZMAPI_CLSID: 'MAPI OLE GUID', 
       SZMAPI_BINARY: 'MAPI binary', 
       SZMAPI_BEATS_THE_HELL_OUTTA_ME: 'Unknown'}

    def __init__(self, codepage):
        self.codepage = codepage
        self.mapi_attrs = []
        self.name = ''
        self.data = ''

    def long_filename(self):
        atname = TNEFMAPI_Attribute.MAPI_ATTACH_LONG_FILENAME
        name = [ a.data for a in self.mapi_attrs if a.name == atname ]
        if name:
            return name[0]
        return self.name.decode()

    def add_attr(self, attribute):
        if attribute.name == TNEF.ATTATTACHMODIFYDATE:
            self.modification_date = typtime(attribute.data)
        elif attribute.name == TNEF.ATTATTACHCREATEDATE:
            self.creation_date = typtime(attribute.data)
        elif attribute.name == TNEF.ATTATTACHMENT:
            self.mapi_attrs += decode_mapi(attribute.data, self.codepage)
        elif attribute.name == TNEF.ATTATTACHTITLE:
            self.name = attribute.data.strip('\x00')
        elif attribute.name == TNEF.ATTATTACHDATA:
            self.data = attribute.data
        elif attribute.name == TNEF.ATTATTACHRENDDATA:
            pass
        elif attribute.name == TNEF.ATTATTACHMETAFILE:
            pass
        else:
            logger.debug('Unknown attribute name: %s' % attribute)

    def __str__(self):
        return "<ATTCH:'%s'>" % self.long_filename()


class TNEF(object):
    """main decoder class - start by using this"""
    TNEF_SIGNATURE = 574529400
    LVL_MESSAGE = 1
    LVL_ATTACHMENT = 2
    VALID_VERSION = 65536
    ATTOWNER = 0
    ATTSENTFOR = 1
    ATTDELEGATE = 2
    ATTDATESTART = 6
    ATTDATEEND = 7
    ATTAIDOWNER = 8
    ATTREQUESTRES = 9
    ATTFROM = 32768
    ATTSUBJECT = 32772
    ATTDATESENT = 32773
    ATTDATERECD = 32774
    ATTMESSAGESTATUS = 32775
    ATTMESSAGECLASS = 32776
    ATTMESSAGEID = 32777
    ATTPARENTID = 32778
    ATTCONVERSATIONID = 32779
    ATTBODY = 32780
    ATTPRIORITY = 32781
    ATTATTACHDATA = 32783
    ATTATTACHTITLE = 32784
    ATTATTACHMETAFILE = 32785
    ATTATTACHCREATEDATE = 32786
    ATTATTACHMODIFYDATE = 32787
    ATTDATEMODIFY = 32800
    ATTATTACHTRANSPORTFILENAME = 36865
    ATTATTACHRENDDATA = 36866
    ATTMAPIPROPS = 36867
    ATTRECIPTABLE = 36868
    ATTATTACHMENT = 36869
    ATTTNEFVERSION = 36870
    ATTOEMCODEPAGE = 36871
    ATTORIGNINALMESSAGECLASS = 36872
    codes = {ATTOWNER: 'Owner', 
       ATTSENTFOR: 'Sent For', 
       ATTDELEGATE: 'Delegate', 
       ATTDATESTART: 'Date Start', 
       ATTDATEEND: 'Date End', 
       ATTAIDOWNER: 'Owner Appointment ID', 
       ATTREQUESTRES: 'Response Requested', 
       ATTFROM: 'From', 
       ATTSUBJECT: 'Subject', 
       ATTDATESENT: 'Date Sent', 
       ATTDATERECD: 'Date Received', 
       ATTMESSAGESTATUS: 'Message Status', 
       ATTMESSAGECLASS: 'Message Class', 
       ATTMESSAGEID: 'Message ID', 
       ATTPARENTID: 'Parent ID', 
       ATTCONVERSATIONID: 'Conversation ID', 
       ATTBODY: 'Body', 
       ATTPRIORITY: 'Priority', 
       ATTATTACHDATA: 'Attachment Data', 
       ATTATTACHTITLE: 'Attachment File Name', 
       ATTATTACHMETAFILE: 'Attachment Meta File', 
       ATTATTACHCREATEDATE: 'Attachment Creation Date', 
       ATTATTACHMODIFYDATE: 'Attachment Modification Date', 
       ATTDATEMODIFY: 'Date Modified', 
       ATTATTACHTRANSPORTFILENAME: 'Attachment Transport Filename', 
       ATTATTACHRENDDATA: 'Attachment Rendering Data', 
       ATTMAPIPROPS: 'MAPI Properties', 
       ATTRECIPTABLE: 'Recipients', 
       ATTATTACHMENT: 'Attachment', 
       ATTTNEFVERSION: 'TNEF Version', 
       ATTOEMCODEPAGE: 'OEM Codepage', 
       ATTORIGNINALMESSAGECLASS: 'Original Message Class'}
    MIN_OBJ_SIZE = 12

    def __init__(self, data, do_checksum=True):
        self.signature = uint32(data)
        if self.signature != TNEF.TNEF_SIGNATURE:
            raise ValueError('Wrong TNEF signature: 0x%2.8x' % self.signature)
        self.key = uint16(data, 4)
        self.codepage = None
        self.objects = []
        self.attachments = []
        self.mapiprops = []
        self.msgprops = []
        self.body = None
        self.htmlbody = None
        self._rtfbody = None
        offset = 6
        if not do_checksum:
            logger.info('Skipping checksum for performance')
        while offset + self.MIN_OBJ_SIZE < len(data):
            obj = TNEFObject(data[offset:], do_checksum)
            offset += obj.length
            self.objects.append(obj)
            if obj.name == TNEF.ATTATTACHRENDDATA:
                attachment = TNEFAttachment(self.codepage)
                self.attachments.append(attachment)
            if obj.level == TNEF.LVL_ATTACHMENT:
                attachment.add_attr(obj)
            elif obj.name == TNEF.ATTMAPIPROPS:
                self.mapiprops = decode_mapi(obj.data, self.codepage)
                for p in self.mapiprops:
                    if p.name == TNEFMAPI_Attribute.MAPI_BODY:
                        self.body = p.data
                    elif p.name == TNEFMAPI_Attribute.UNCOMPRESSED_BODY:
                        self.body = p.data
                    elif p.name == TNEFMAPI_Attribute.MAPI_BODY_HTML:
                        self.htmlbody = p.data
                    elif p.name == TNEFMAPI_Attribute.MAPI_RTF_COMPRESSED:
                        self._rtfbody = p.data

            elif obj.name == TNEF.ATTBODY:
                self.body = obj.data
            elif obj.name == TNEF.ATTTNEFVERSION:
                if uint32(obj.data) != TNEF.VALID_VERSION:
                    logger.warning('Invalid TNEF Version %02x%02x%02x%02x', *obj.data)
            elif obj.name == TNEF.ATTOEMCODEPAGE:
                self.codepage = 'cp%d' % uint32(obj.data)
            elif obj.type in (TNEFObject.PTYPE_CLASS, TNEFObject.PTYPE_STRING):
                obj.data = obj.data.decode(self.codepage)
                self.msgprops.append(obj)
            elif obj.name == TNEF.ATTPRIORITY:
                obj.data = 3 - uint16(obj.data)
                self.msgprops.append(obj)
            elif obj.name == TNEF.ATTRECIPTABLE:
                rows = uint32(obj.data)
                att_offset = 4
                recipients = []
                for _ in range(rows):
                    att_offset, recipients = decode_mapi(obj.data, self.codepage, starting_offset=att_offset)
                    recipients.append(recipients)

                obj.data = recipients
                self.msgprops.append(obj)
            elif obj.name == TNEF.ATTFROM:
                obj.data = triples(obj.data)
                self.msgprops.append(obj)
            elif obj.name == TNEF.ATTREQUESTRES:
                obj.data = bool(uint16(obj.data))
                self.msgprops.append(obj)
            elif obj.name == TNEF.ATTMESSAGESTATUS:
                obj.data = bytes_to_int(obj.data)
                self.msgprops.append(obj)
            elif obj.type == TNEFObject.PTYPE_TIME and obj.name in (
             TNEF.ATTDATESTART, TNEF.ATTDATEMODIFY, TNEF.ATTDATESENT, TNEF.ATTDATERECD):
                try:
                    obj.data = typtime(obj.data)
                    self.msgprops.append(obj)
                except ValueError:
                    logger.debug('TNEF Object not a valid date: %s' % obj)

            else:
                logger.debug('Unhandled TNEF Object: %s' % obj)

        return

    def has_body(self):
        if self.body or self.htmlbody or self._rtfbody:
            return True
        return False

    @property
    def rtfbody(self):
        if self._rtfbody:
            try:
                from compressed_rtf import decompress
                return decompress(self._rtfbody + '\x00')
            except ImportError:
                logger.warning('Returning compressed RTF. Install compressed_rtf to decompress')
                return self._rtfbody

        else:
            return
        return

    def __str__(self):
        atts = ', %i attachments' % len(self.attachments) if self.attachments else ''
        return '<%s:0x%2.2x%s>' % (self.__class__.__name__, self.key, atts)


def valid_version(data):
    version = uint32(data)
    return version == 65536


def triples(data):
    assert uint16(data) == 4
    struct_length = uint16(data, 2)
    sender_length = uint16(data, 4)
    email_length = uint16(data, 6)
    sender = data[8:8 + sender_length]
    etype_email = data[8 + sender_length:8 + sender_length + email_length]
    etype, email = etype_email.split(':', 1)
    return (
     sender.rstrip('\x00'), etype, email.rstrip('\x00'))


def to_zip(data, default_name='no-name', deflate=True):
    """Convert attachments in TNEF data to zip format. Accepts and returns str type."""
    tnef = TNEF(data)
    tozip = {}
    for attachment in tnef.attachments:
        filename = attachment.name.decode() or default_name
        L = len(tozip.get(filename, []))
        if L > 0:
            root, ext = os.path.splitext(filename)
            tozip[filename].append((attachment.data, str('%s-%d%s' % (root, L + 1, ext))))
        else:
            tozip[filename] = [
             (
              attachment.data, filename)]

    from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
    from io import BytesIO
    import contextlib
    sfp = BytesIO()
    zf = ZipFile(sfp, 'w', ZIP_DEFLATED if deflate else ZIP_STORED)
    with contextlib.closing(zf) as (z):
        for filename, entries in list(tozip.items()):
            for entry in entries:
                data, name = entry
                z.writestr(name, data)

    return sfp.getvalue()