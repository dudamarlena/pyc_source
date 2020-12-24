# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/scripts/message_response.py
# Compiled at: 2008-06-20 03:40:59
"""filter_message.py - tool to filter a given message entry

AUTHOR: Emanuel Gardaya Calso

"""
import os, urllib
from base import *

def find_response(sender, msg):
    m_args = msg.split(' ')
    print 'find_response', m_args
    for entry in model.list(model.Response).filter_by(keyword=m_args[0]):
        process_response(sender, m_args, entry)

    model.Session.commit()


def process_response(sender, m_args, response):
    print 'process_response', sender, m_args, response
    if response.action == 'show':
        response = response_show(sender, m_args, response)
    elif response.action == 'add':
        response = response_add(sender, m_args, response)
    elif response.action == 'search':
        response = response_search(sender, m_args, response)
    elif response.action == 'edit':
        response = response_edit(sender, m_args, response)
    elif response.action == 'delete':
        response = response_delete(sender, m_args, response)
    else:
        response = response
    return response


def response_add(sender, m_args, response):
    print 'response_add', sender, m_args
    r_def = response.default
    r_args = response.argument
    r_value = response.value
    table = custom_env.classes[response.table]
    cnt = 0
    s_args = {}
    entries = []
    for arg in r_args:
        cnt += 1
        col = arg.field
        try:
            m_val = m_args[cnt]
        except IndexError:
            return send_err(sender, m_args)

        s_args[str(col)] = m_val.replace(space_sub, ' ')

    entry = table(**s_args)
    model.Session.save(entry)
    model.Session.comit()
    send_msg(sender, 'Successfully saved entry')
    return response


def response_show(sender, m_args, response):
    print 'response_show', sender, m_args
    r_def = response.default
    r_args = response.argument
    r_value = response.value
    table = custom_env.classes[response.table]
    query = custom_env.session.query(table)
    cnt = 0
    s_args = {}
    entries = []
    print 'Adding default filter values;'
    for entry in r_def:
        s_args[entry.field] = entry.value

    print 'Adding filters from text mesage'
    for arg in r_args:
        cnt += 1
        col = arg.field
        try:
            m_val = m_args[cnt]
        except IndexError:
            return send_err(sender, m_args)

        s_args[str(col)] = m_val.replace(space_sub, ' ')

    print s_args
    entries = query.filter_by(**s_args)
    if len(list(entries)) == 0:
        msg = 'No entry for %s where:%s' % (
         m_args[0],
         ('\n').join(('\n%s: %s' % (k, v) for (k, v) in s_args.iteritems())))
        send_msg(sender, msg)
        return response
    for entry in entries:
        send_entry(sender, entry, r_value)

    return response


def send_entry(recipient, entry, outputs):
    print 'send_entry', recipient, entry, outputs
    msg = ''
    outs = []
    for output in outputs:
        outs.append((output.priority, output.label, output.field))

    outs.sort()
    for out in outs:
        label = out[1]
        field = out[2]
        value = getattr(entry, field)
        msg += '%s:%s\n' % (label, value)

    message = send_msg(recipient, msg)
    return message


def send_err(recipient, m_args):
    msg = 'Invalid number of arguments for %s' % m_args[0]
    message = send_msg(recipient, msg)
    return message


def send_msg(recipient, msg):
    message = model.Message(folder=OUTBOX, sender=urllib.unquote_plus(NUMBER), recipient=recipient, message=msg)
    model.Session.save(message)
    print 'Saved to Outbox'
    return message