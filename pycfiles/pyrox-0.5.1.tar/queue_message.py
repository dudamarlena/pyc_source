# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /private/tmp/test/lib/python2.7/site-packages/pyrowire/routes/queue_message.py
# Compiled at: 2014-11-25 17:55:11
from datetime import datetime
import json
from multiprocessing import Process
import time
from flask import Blueprint, request, current_app
from redis import Redis
from redis.exceptions import ConnectionError, TimeoutError
import twilio.twiml as twiml, pyrowire.config.configuration as config
from pyrowire.messaging.message import message_from_request
from pyrowire.messaging.send import sms
queue_message = Blueprint('message_queue', __name__)

@queue_message.route('/<topic>', methods=['GET', 'POST'])
def queue(topic):
    """
    takes inbound request from Twilio API and parses out:
      - From (mobile number of sender)
      - Body (message sent via SMS)
    ensures body passes through all defined filters for the topic
    if filters pass, mobile number and message are queued in Redis for processing by worker(s).
    response is sent back using twiml based on outcome
    :return: string form of twiml response
    """
    message = message_from_request(request=request)
    redis = Redis(config.redis('host'), int(config.redis('port')), int(config.redis('db')), config.redis('password'))
    response = twiml.Response()
    try:
        for name, func in [ k for k in config.validators().items() if k[0] in config.validators(topic).keys() ]:
            message_invalid = func(message)
            if message_invalid:
                message['validator_error'] = config.validators(topic)[name]
                Process(target=sms, kwargs={'data': message, 'key': 'validator_error'}).start()
                response.message(config.validators(topic)[name])
                return str(response)

        redis.rpush('%s.%s' % (topic, 'submitted'), json.dumps(message))
        message['response'] = config.accept_response(topic)
        if config.send_on_accept(topic):
            Process(target=sms, kwargs={'data': message, 'key': 'response'}).start()
        response.message(config.accept_response(topic))
        return str(response)
    except (ConnectionError, TimeoutError, KeyError, TypeError) as e:
        if type(e) in [KeyError, TypeError]:
            try:
                timestamp = time.time()
                date_timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                error = {'message': message, 'error': str(e)}
                redis.hset('%s.error' % topic, date_timestamp, error)
            except:
                pass

        current_app.logger.log(e)
        response.message(config.error_response(topic))
        return str(response)