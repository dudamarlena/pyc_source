# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/trytond/modules/twilio_messages/routes.py
# Compiled at: 2018-04-30 01:33:52
from werkzeug.exceptions import abort
from werkzeug.wrappers import Response
from trytond.wsgi import app
from trytond.protocols.wrappers import with_pool, with_transaction

@app.route('/<database_name>/twiliomessages/<uuid>', methods=['POST'])
@with_pool
@with_transaction()
def callback(request, pool, uuid):
    Message = pool.get('twilio.message')
    try:
        message, = Message.search([
         (
          'uuid', '=', uuid)])
    except ValueError:
        abort(404)

    message.sid = request.values.get('MessageSid', None)
    message.status = request.values.get('MessageStatus', None)
    if message.status in {'failed', 'undelivered'}:
        message.error_code = request.values.get('MessageErrorCode', None)
        message.error_message = request.values.get('MessageErrorMessage', None)
    message.save()
    return Response(None, 204)