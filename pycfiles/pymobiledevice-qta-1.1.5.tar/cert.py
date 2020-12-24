# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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