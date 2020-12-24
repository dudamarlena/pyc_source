# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/shared/models/base_session.py
# Compiled at: 2016-11-12 07:38:04
import uuid, logging, json
from datetime import datetime
import zmq.green
from gevent.lock import BoundedSemaphore
import beeswarm
from beeswarm.shared.socket_enum import SocketNames
from beeswarm.shared.message_enum import Messages
logger = logging.getLogger(__name__)

class BaseSession(object):
    socket = None
    socketLock = BoundedSemaphore(1)

    def __init__(self, protocol, source_ip=None, source_port=None, destination_ip=None, destination_port=None):
        self.id = uuid.uuid4()
        self.source_ip = source_ip
        self.source_port = source_port
        self.protocol = protocol
        self.destination_ip = destination_ip
        self.destination_port = destination_port
        self.timestamp = datetime.utcnow()
        self.login_attempts = []
        self.transcript = []
        self.session_ended = False
        with BaseSession.socketLock:
            if BaseSession.socket is None:
                context = beeswarm.shared.zmq_context
                BaseSession.socket = context.socket(zmq.PUSH)
                BaseSession.socket.connect(SocketNames.SERVER_RELAY.value)
        return

    def add_auth_attempt(self, auth_type, successful, **kwargs):
        """
        :param username:
        :param password:
        :param auth_type: possible values:
                                plain: plaintext username/password
        :return:
        """
        entry = {'timestamp': datetime.utcnow(), 'auth': auth_type, 
           'id': uuid.uuid4(), 
           'successful': successful}
        log_string = ''
        for key, value in kwargs.iteritems():
            if key == 'challenge' or key == 'response':
                entry[key] = repr(value)
            else:
                entry[key] = value
                log_string += ('{0}:{1}, ').format(key, value)

        self.login_attempts.append(entry)

    def get_number_of_login_attempts(self):
        return len(self.login_attempts)

    def _add_transcript(self, direction, data):
        self.transcript.append({'timestamp': datetime.utcnow(), 'direction': direction, 'data': data})

    def transcript_incoming(self, data):
        self._add_transcript('incoming', data)

    def transcript_outgoing(self, data):
        self._add_transcript('outgoing', data)

    @classmethod
    def send_log(cls, type, in_data):
        data = json.dumps(in_data, default=json_default, ensure_ascii=False)
        message = ('{0} {1}').format(type, data)
        with cls.socketLock:
            cls.socket.send(message)

    def to_dict(self):
        return vars(self)

    def end_session(self, session_type):
        if not self.session_ended:
            self.session_ended = True
            self.send_log(session_type, self.to_dict())
            self.connected = False


def json_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        if isinstance(obj, uuid.UUID):
            return str(obj)
        else:
            return

        return