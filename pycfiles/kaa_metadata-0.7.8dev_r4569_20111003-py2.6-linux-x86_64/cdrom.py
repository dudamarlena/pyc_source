# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/disc/cdrom.py
# Compiled at: 2009-08-30 20:12:32
import os, re, time, array, hashlib
from struct import pack, unpack
import logging
from fcntl import ioctl
CREATE_MD5_ID = 0
try:
    import _cdrom
except ImportError:
    _cdrom = None

log = logging.getLogger('metadata')

def audiocd_open(device=None, flags=None):
    if device == None:
        return _cdrom.open()
    else:
        if flags == None:
            return _cdrom.open(device)
        else:
            return _cdrom.open(device, flags)

        return


def audiocd_id(device):
    first, last = _cdrom.toc_header(device)
    track_frames = []
    checksum = 0
    for i in range(first, last + 1):
        min, sec, frame = _cdrom.toc_entry(device, i)
        n = min * 60 + sec
        while n > 0:
            checksum += n % 10
            n = n / 10

        track_frames.append(min * 60 * 75 + sec * 75 + frame)

    min, sec, frame = _cdrom.leadout(device)
    track_frames.append(min * 60 * 75 + sec * 75 + frame)
    total_time = track_frames[(-1)] / 75 - track_frames[0] / 75
    discid = checksum % 255 << 24 | total_time << 8 | last
    return [discid, last] + track_frames[:-1] + [track_frames[(-1)] / 75]


def audiocd_toc_header(device):
    return _cdrom.toc_header(device)


def audiocd_toc_entry(device, track):
    return _cdrom.toc_entry(device, track)


def audiocd_leadout(device):
    return _cdrom.leadout(device)


def _drive_status(device, handle_mix=0):
    """
    check the current disc in device
    return: no disc (0), audio cd (1), data cd (2), blank cd (3)
    """
    CDROM_DRIVE_STATUS = 21286
    CDSL_CURRENT = int(-1)
    CDROM_DISC_STATUS = 21287
    CDS_AUDIO = 100
    CDS_MIXED = 105
    CDS_DISC_OK = 4
    CDS_NO_DISC = 0
    if os.uname()[0] == 'FreeBSD':
        CDIOREADTOCENTRYS = 3221775109
        CD_MSF_FORMAT = 2
    fd = None
    try:
        fd = os.open(device, os.O_RDONLY | os.O_NONBLOCK)
        if os.uname()[0] == 'FreeBSD':
            try:
                cd_toc_entry = array.array('c', '\x00' * 4096)
                address, length = cd_toc_entry.buffer_info()
                buf = pack('BBHP', CD_MSF_FORMAT, 0, length, address)
                s = ioctl(fd, CDIOREADTOCENTRYS, buf)
                s = CDS_DISC_OK
            except (OSError, IOError):
                s = CDS_NO_DISC

        else:
            s = ioctl(fd, CDROM_DRIVE_STATUS, CDSL_CURRENT)
    except (OSError, IOError):
        log.error('ERROR: no permission to read %s' % device)
        log.error("Media detection not possible, set drive to 'empty'")
        try:
            if fd:
                os.close(fd)
        except (OSError, IOError):
            pass

        return 0

    if not s == CDS_DISC_OK:
        try:
            os.close(fd)
        except (OSError, IOError):
            pass

        return 0
    if os.uname()[0] == 'FreeBSD':
        s = 0
        for i in range(0, 4096, 8):
            control = unpack('B', cd_toc_entry[(i + 1)])[0] & 4
            track = unpack('B', cd_toc_entry[(i + 2)])[0]
            if track == 0:
                break
            if control == 0 and s != CDS_MIXED:
                s = CDS_AUDIO
            elif control != 0:
                if s == CDS_AUDIO:
                    s = CDS_MIXED
                else:
                    s = 100 + control
            elif control == 5:
                s = CDS_MIXED

    else:
        s = ioctl(fd, CDROM_DISC_STATUS)
    os.close(fd)
    if s == CDS_MIXED and handle_mix:
        return 4
    else:
        if s == CDS_AUDIO or s == CDS_MIXED:
            return 1
        try:
            fd = open(device, 'rb')
            fd.seek(32768)
            fd.read(1)
        except IOError:
            fd.close()
            return 3

        fd.close()
        return 2


_id_cache = {}

def status(device, handle_mix=0):
    """
    return the disc id of the device or None if no disc is there
    """
    global _id_cache
    if not _cdrom:
        log.debug('kaa.metadata not compiled with CDROM support')
        return (0, None)
    else:
        try:
            if _id_cache[device][0] + 0.9 > time.time():
                return _id_cache[device][1:]
        except (KeyError, IndexError):
            pass

        disc_type = _drive_status(device, handle_mix=handle_mix)
        if disc_type == 0 or disc_type == 3:
            return (0, None)
        if disc_type == 1 or disc_type == 4:
            discfd = audiocd_open(device)
            id = audiocd_id(discfd)
            id = '%08lx_%d' % (id[0], id[1])
            discfd.close()
        else:
            f = open(device, 'rb')
            if os.uname()[0] == 'FreeBSD':
                f.seek(32768)
                id = f.read(829)
                label = id[40:72]
                id = id[813:829]
            else:
                f.seek(33581)
                id = f.read(16)
                f.seek(32808, 0)
                label = f.read(32)
            if CREATE_MD5_ID:
                id = hashlib.md5(f.read(51200)).hexdigest()
            f.close()
            m = re.match('^(.*[^ ]) *$', label)
            if m:
                id = '%s%s' % (id, m.group(1))
            id = re.compile('[^a-zA-Z0-9()_-]').sub('_', id)
        _id_cache[device] = (
         time.time(), disc_type, id)
        id = id.replace('/', '_')
        return (disc_type, id)