# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/buttersink/send.py
# Compiled at: 2018-06-26 18:43:29
""" Utilities for sending and receiving btrfs snapshots. """
from ioctl import Structure, t
import btrfs, ioctl, crcmod.predefined
crc32c = crcmod.predefined.mkPredefinedCrcFun('crc-32c')
import logging, struct
logger = logging.getLogger(__name__)
BTRFS_SEND_STREAM_MAGIC = 'btrfs-stream\x00'
BTRFS_SEND_STREAM_VERSION = 1
btrfs_stream_header = Structure((
 t.char, 'magic', len(BTRFS_SEND_STREAM_MAGIC)), (
 t.le32, 'version'), packed=True)
btrfs_cmd_header = Structure((
 t.le32, 'len'), (
 t.le16, 'cmd'), (
 t.le32, 'crc'), packed=True)
btrfs_tlv_header = Structure((
 t.le16, 'tlv_type'), (
 t.le16, 'tlv_len'), packed=True)
BTRFS_SEND_C_UNSPEC, BTRFS_SEND_C_SUBVOL, BTRFS_SEND_C_SNAPSHOT, BTRFS_SEND_C_MKFILE, BTRFS_SEND_C_MKDIR, BTRFS_SEND_C_MKNOD, BTRFS_SEND_C_MKFIFO, BTRFS_SEND_C_MKSOCK, BTRFS_SEND_C_SYMLINK, BTRFS_SEND_C_RENAME, BTRFS_SEND_C_LINK, BTRFS_SEND_C_UNLINK, BTRFS_SEND_C_RMDIR, BTRFS_SEND_C_SET_XATTR, BTRFS_SEND_C_REMOVE_XATTR, BTRFS_SEND_C_WRITE, BTRFS_SEND_C_CLONE, BTRFS_SEND_C_TRUNCATE, BTRFS_SEND_C_CHMOD, BTRFS_SEND_C_CHOWN, BTRFS_SEND_C_UTIMES, BTRFS_SEND_C_END, BTRFS_SEND_C_UPDATE_EXTENT, __BTRFS_SEND_C_MAX = range(24)
BTRFS_SEND_C_MAX = __BTRFS_SEND_C_MAX - 1
BTRFS_SEND_A_UNSPEC, BTRFS_SEND_A_UUID, BTRFS_SEND_A_CTRANSID, BTRFS_SEND_A_INO, BTRFS_SEND_A_SIZE, BTRFS_SEND_A_MODE, BTRFS_SEND_A_UID, BTRFS_SEND_A_GID, BTRFS_SEND_A_RDEV, BTRFS_SEND_A_CTIME, BTRFS_SEND_A_MTIME, BTRFS_SEND_A_ATIME, BTRFS_SEND_A_OTIME, BTRFS_SEND_A_XATTR_NAME, BTRFS_SEND_A_XATTR_DATA, BTRFS_SEND_A_PATH, BTRFS_SEND_A_PATH_TO, BTRFS_SEND_A_PATH_LINK, BTRFS_SEND_A_FILE_OFFSET, BTRFS_SEND_A_DATA, BTRFS_SEND_A_CLONE_UUID, BTRFS_SEND_A_CLONE_CTRANSID, BTRFS_SEND_A_CLONE_PATH, BTRFS_SEND_A_CLONE_OFFSET, BTRFS_SEND_A_CLONE_LEN, __BTRFS_SEND_A_MAX = range(26)
BTRFS_SEND_A_MAX = __BTRFS_SEND_A_MAX - 1

class ParseException(Exception):
    """ Dedicated Exception class. """
    pass


def TLV_GET(attrs, attrNum, format):
    """ Get a tag-length-value encoded attribute. """
    attrView = attrs[attrNum]
    if format == 's':
        format = str(attrView.len) + format
    try:
        result, = struct.unpack_from(format, attrView.buf, attrView.offset)
    except TypeError:
        result, = struct.unpack_from(format, str(bytearray(attrView.buf)), attrView.offset)

    return result


def TLV_PUT(attrs, attrNum, format, value):
    """ Put a tag-length-value encoded attribute. """
    attrView = attrs[attrNum]
    if format == 's':
        format = str(attrView.len) + format
    struct.pack_into(format, attrView.buf, attrView.offset, value)


def TLV_GET_BYTES(attrs, attrNum):
    """ Get a tag-length-value encoded attribute as bytes. """
    return TLV_GET(attrs, attrNum, 's')


def TLV_PUT_BYTES(attrs, attrNum, value):
    """ Put a tag-length-value encoded attribute as bytes. """
    TLV_PUT(attrs, attrNum, 's', value)


def TLV_GET_STRING(attrs, attrNum):
    """ Get a tag-length-value encoded attribute as a string. """
    return t.readString(TLV_GET_BYTES(attrs, attrNum))


def TLV_GET_UUID(attrs, attrNum):
    """ Get a tag-length-value encoded attribute as a UUID. """
    return btrfs.bytes2uuid(TLV_GET_BYTES(attrs, attrNum))


def TLV_GET_U64(attrs, attrNum):
    """ Get a tag-length-value encoded attribute as a U64. """
    return TLV_GET(attrs, attrNum, t.u64)


def replaceIDs(data, receivedUUID, receivedGen, parentUUID, parentGen):
    """ Parse and replace UUID and transid info in data stream. """
    if len(data) < 20:
        return data
    else:
        logger.debug('Setting received %s/%d and parent %s/%d', receivedUUID, receivedGen or 0, parentUUID, parentGen or 0.0)
        data = bytearray(data)
        buf = ioctl.Buffer(data)
        header = buf.read(btrfs_stream_header)
        if header.magic != BTRFS_SEND_STREAM_MAGIC:
            raise ParseException("Didn't find '%s'" % BTRFS_SEND_STREAM_MAGIC)
        logger.debug('Version: %d', header.version)
        if header.version > BTRFS_SEND_STREAM_VERSION:
            logger.warn('Unknown stream version: %d', header.version)
        cmdHeaderView = buf.peekView(btrfs_cmd_header.size)
        cmdHeader = buf.read(btrfs_cmd_header)
        logger.debug('Command: %d', cmdHeader.cmd)
        attrs = {}
        attrDataView = buf.peekView(cmdHeader.len)
        attrData = buf.readBuffer(cmdHeader.len)
        while attrData.len > 0:
            attrHeader = attrData.read(btrfs_tlv_header)
            attrs[attrHeader.tlv_type] = attrData.readBuffer(attrHeader.tlv_len)

        def calcCRC():
            header = cmdHeader._asdict()
            header['crc'] = 0
            crc = 4294967295
            crc = crc32c(btrfs_cmd_header.write(header).tostring(), crc)
            crc = crc32c(attrDataView.tobytes(), crc)
            crc &= 4294967295
            crc = crc ^ 4294967295
            return crc

        crc = calcCRC()
        if cmdHeader.crc != crc:
            logger.warn("Stored crc (%d) doesn't match calculated crc (%d)", cmdHeader.crc, crc)
        s = attrs

        def correct(attr, format, name, old, new, encode=None):
            if new is not None and new != old:
                logger.debug('Correcting %s from %s to %s', name, str(old), str(new))
                if encode is not None:
                    new = encode(new)
                TLV_PUT(attrs, attr, format, new)
            return

        def correctCRC():
            crc = calcCRC()
            if cmdHeader.crc != crc:
                logger.debug('Correcting CRC from %d to %d', cmdHeader.crc, crc)
                header = cmdHeader._asdict()
                header['crc'] = crc
                cmdHeaderView[:] = btrfs_cmd_header.write(header).tostring()

        if cmdHeader.cmd == BTRFS_SEND_C_SUBVOL:
            path = TLV_GET_STRING(s, BTRFS_SEND_A_PATH)
            uuid = TLV_GET_UUID(s, BTRFS_SEND_A_UUID)
            ctransid = TLV_GET_U64(s, BTRFS_SEND_A_CTRANSID)
            logger.debug('Subvol: %s/%d %s', uuid, ctransid, path)
            correct(BTRFS_SEND_A_UUID, 's', 'received UUID', uuid, receivedUUID, btrfs.uuid2bytes)
            correct(BTRFS_SEND_A_CTRANSID, t.u64, 'received gen', ctransid, receivedGen)
        elif cmdHeader.cmd == BTRFS_SEND_C_SNAPSHOT:
            path = TLV_GET_STRING(s, BTRFS_SEND_A_PATH)
            uuid = TLV_GET_UUID(s, BTRFS_SEND_A_UUID)
            ctransid = TLV_GET_U64(s, BTRFS_SEND_A_CTRANSID)
            clone_uuid = TLV_GET_UUID(s, BTRFS_SEND_A_CLONE_UUID)
            clone_ctransid = TLV_GET_U64(s, BTRFS_SEND_A_CLONE_CTRANSID)
            logger.debug('Snapshot: %s/%d -> %s/%d %s', clone_uuid, clone_ctransid, uuid, ctransid, path)
            correct(BTRFS_SEND_A_UUID, 's', 'received UUID', uuid, receivedUUID, btrfs.uuid2bytes)
            correct(BTRFS_SEND_A_CTRANSID, t.u64, 'received gen', ctransid, receivedGen)
            correct(BTRFS_SEND_A_CLONE_UUID, 's', 'parent UUID', clone_uuid, parentUUID, btrfs.uuid2bytes)
            correct(BTRFS_SEND_A_CLONE_CTRANSID, t.u64, 'parent gen', clone_ctransid, parentGen)
        else:
            logger.warn("Didn't find volume UUID command")
        correctCRC()
        return data