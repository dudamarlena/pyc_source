# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/util/cert.py
# Compiled at: 2019-03-03 16:57:38
import base64

def chunks(l, n):
    return (l[i:i + n] for i in range(0, len(l), n))


def RSA_KEY_DER_to_PEM(data):
    a = [
     '-----BEGIN RSA PRIVATE KEY-----']
    a.extend(chunks(base64.b64encode(data), 64))
    a.append('-----END RSA PRIVATE KEY-----')
    return ('\n').join(a)