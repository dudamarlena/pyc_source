# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/django_payworld/utils.py
# Compiled at: 2012-02-15 01:02:17
from hashlib import md5
from django.utils.encoding import smart_str

def calculate_hash(data, salt):
    u""" Считаем хэш с солью по следующему принципу:
            hash = MD5(MD5(str_to_hash) + salt)
        Строка str_to_hash формируется конкатенацией следующих параметров запроса:
            order_id + order_total + transaction_id + payer_email + seller_name + shop_id
    """
    FIELDS_ORDER = ('order_id', 'order_total', 'transaction_id', 'payer_email', 'seller_name',
                    'shop_id')
    data_as_list = [ str(data[field]) for field in FIELDS_ORDER ]
    str_to_hash = smart_str(('').join(data_as_list), 'utf-8')
    return md5(str_to_hash + salt).hexdigest()