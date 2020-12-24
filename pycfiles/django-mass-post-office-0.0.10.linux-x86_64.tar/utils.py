# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/utils.py
# Compiled at: 2015-03-06 05:08:58
import zlib, pickle, hashlib, urllib, base64, settings

def encode_data(data):
    """Turn `data` into a hash and an encoded string, suitable for use with
    `decode_data`.

    """
    text = base64.b64encode(zlib.compress(pickle.dumps(data, 0))).replace('+', '.').replace('/', '-')
    m = hashlib.md5(settings.SECRET_KEY + text).hexdigest()[:12]
    return (m, text)


def decode_data(hashed, enc):
    """The inverse of `encode_data`.

    """
    text = urllib.unquote(enc)
    m = hashlib.md5(settings.SECRET_KEY + text).hexdigest()[:12]
    if m != hashed:
        raise ValueError('Bad hash!')
    text = text.replace('-', '/').replace('.', '+')
    data = pickle.loads(zlib.decompress(text.decode('base64')))
    return data