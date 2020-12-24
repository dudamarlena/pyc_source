# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIC2-U\Documents\BitBucket\microsip_envia_sms\microsip_envia_sms\modules\bill_message.py
# Compiled at: 2014-12-09 11:41:12
import time, re, unidecode, threading, fdb, importlib, sys

def execute_sql(sql, **kwargs):
    user = kwargs.get('user', None)
    password = kwargs.get('password', None)
    database = kwargs.get('database', None)
    return_data = kwargs.get('return_data', True)
    db = fdb.connect(host='localhost', user=user, password=password, database=database)
    cur = db.cursor()
    cur.execute(sql)
    data = None
    if return_data:
        data = cur.fetchall()
    try:
        db.commit()
    except Exception as e:
        pass

    cur.close()
    return data


def generate_message(**kwargs):
    messages = execute_sql("Select * from SIC_MENSAJES_PENDIENTES where mensaje is null and tipo ='GRACIAS'", **kwargs)
    empresa_nombre = kwargs['empresa_nombre']
    if messages:
        for message in messages:
            message_id = message[0]
            telefono = message[1]
            cliente = message[2]
            tipo = message[3]
            folio, importe = message[4].split(',')
            message = ''
            if tipo == 'GRACIAS':
                message = empresa_nombre + ' le agradece su compra ' + folio + ' por ' + importe
                message = message.rstrip()
                sql = "update SIC_MENSAJES_PENDIENTES set mensaje='%s' where id=%s" % (message, message_id)
                kwargs['return_data'] = False
                execute_sql(sql, **kwargs)