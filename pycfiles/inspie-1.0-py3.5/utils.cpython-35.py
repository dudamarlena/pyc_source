# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\inspie\utils.py
# Compiled at: 2019-02-20 05:55:36
# Size of source mod 2**32: 2689 bytes
import urllib, sys, uuid, hashlib, hmac, calendar, struct, imghdr
from datetime import datetime
from .config import SIG_KEY_VERSION, IG_SIG_KEY
if sys.version_info.major == 3:
    import urllib.parse

def generate_signature(data, skip_quote=False):
    if not skip_quote:
        try:
            parsedData = urllib.parse.quote(data)
        except AttributeError:
            parsedData = urllib.quote(data)

    else:
        parsedData = data
    return 'ig_sig_key_version={}&signed_body={}.{}'.format(SIG_KEY_VERSION, hmac.new(IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest(), parsedData)


def generate_device_id(seed):
    volatile_seed = '12345'
    m = hashlib.md5()
    m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
    return 'android-' + m.hexdigest()[:16]


def generate_UUID(hyphen):
    generated_uuid = str(uuid.uuid4())
    if hyphen:
        return generated_uuid
    else:
        return generated_uuid.replace('-', '')


def generate_upload_id(self):
    return str(calendar.timegm(datetime.utcnow().utctimetuple()))


def get_image_size(fname):
    with open(fname, 'rb') as (fhandle):
        head = fhandle.read(24)
        if len(head) != 24:
            raise RuntimeError('Invalid Header')
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 218765834:
                raise RuntimeError('PNG: Invalid check')
            width, height = struct.unpack('>ii', head[16:24])
        else:
            if imghdr.what(fname) == 'gif':
                width, height = struct.unpack('<HH', head[6:10])
            else:
                if imghdr.what(fname) == 'jpeg':
                    fhandle.seek(0)
                    size = 2
                    ftype = 0
                    while not 192 <= ftype <= 207:
                        fhandle.seek(size, 1)
                        byte = fhandle.read(1)
                        while ord(byte) == 255:
                            byte = fhandle.read(1)

                        ftype = ord(byte)
                        size = struct.unpack('>H', fhandle.read(2))[0] - 2

                    fhandle.seek(1, 1)
                    height, width = struct.unpack('>HH', fhandle.read(4))
                else:
                    raise RuntimeError('Unsupported format')
        return (
         width, height)