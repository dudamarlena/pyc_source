# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/drmartiner/projects/django-paymecash/paymecash/common.py
# Compiled at: 2013-09-16 10:40:06
import uuid, conf, hashlib

def get_sign(data):
    parts = [
     str(int(data['wallet_id']))]
    if data.get('product_price') is not None and data.get('product_currency') is not None:
        parts.append(str(data['product_price']))
        parts.append(data['product_currency'])
    if data.get('order_id'):
        parts.append(data['order_id'])
    parts.append(conf.PAYMECASH_SECRET_KEY)
    string = ('-').join(parts)
    sign = hashlib.md5(string).hexdigest()
    return sign


def get_order_id():
    return str(uuid.uuid4()).replace('-', '')[:16]