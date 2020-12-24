# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sqall/syncfolder/projekte/alertR/push_service/lightweight-push-pip/lightweightpush/lightweightpush.py
# Compiled at: 2019-04-16 13:19:29
import time, socket, ssl, os, base64, json, hashlib, re, requests
from Crypto.Cipher import AES

class ErrorCodes(object):
    """
    Lightweight Push error codes.
    """
    NO_ERROR = 0
    DATABASE_ERROR = 1
    AUTH_ERROR = 2
    ILLEGAL_MSG_ERROR = 3
    GOOGLE_MSG_TOO_LARGE = 4
    GOOGLE_CONNECTION = 5
    GOOGLE_UNKNOWN = 6
    GOOGLE_AUTH = 7
    VERSION_MISSMATCH = 8
    NO_NOTIFICATION_PERMISSION = 9
    WEB_BRIDGE_ERROR = 10
    CLIENT_CONNECTION_ERROR = 4096


class LightweightPush(object):

    def __init__(self, username, password, shared_secret):
        self.host = 'https://push.alertr.de/push/send.php'
        sha256 = hashlib.sha256()
        sha256.update(shared_secret.encode('utf-8'))
        self.key = sha256.digest()
        self.username = username
        self.password = password

    def _generate_prefixed_channel(self, channel):
        """
        Create the channel name linked to the username.
        NOTE: This function is not collision free but will improve collision
        resistance if multiple parties choose the same channel.

        :param channel: to send the message to.
        :return: channel with a prefix based on the user to send the message to.
        """
        sha256 = hashlib.sha256()
        sha256.update(self.username.encode('utf-8'))
        prefix = sha256.hexdigest()[0:8]
        return prefix.lower() + '_' + channel

    def _trunc_to_size(self, subject, message):
        """
        Truncates the message and subject to fit in a notification message.

        :param subject: subject of the message to send.
        :param message: message body of the message.
        :return: (subject, message) in a truncated form to fit the limitations.
        """
        len_json_sbj = len(json.dumps(subject))
        len_sbj = len(subject)
        len_json_msg = len(json.dumps(message))
        len_msg = len(message)
        if len_json_sbj + len_json_msg > 1400:
            number_to_remove = len_json_sbj + len_json_msg + 7 - 1400
            if len_msg > number_to_remove:
                message = message[0:len_msg - number_to_remove]
                message += '*TRUNC*'
            elif len_sbj > number_to_remove:
                subject = subject[0:len_sbj - number_to_remove]
                subject += '*TRUNC*'
            else:
                message = '*TRUNC*'
                number_to_remove = number_to_remove - len_msg + 7
                subject = subject[0:len_sbj - number_to_remove]
                subject += '*TRUNC*'
        return (
         subject, message)

    def _check_channel(self, channel):
        """
        Checks if the given channel is valid.

        :param channel: channel to check.
        :return: True if the channel is valid.
        """
        return bool(re.match('^[a-zA-Z0-9-_.~%]+$', channel))

    def _send_msg(self, data_frame, payload, max_retries):
        """
        Internal function to send data to the push server.

        :param data_frame: data frame to send.
        :param payload: payload of the data to send.
        :param max_retries: maximum number of retries (if -1 we try forever).
        :return: returns error code.
        """
        max_retries_ctr = max_retries
        times_sleep = 5
        iv = os.urandom(16)
        internal_iv = os.urandom(4)
        while True:
            ts = int(time.time())
            payload['ts'] = ts
            padded_payload = internal_iv + json.dumps(payload).encode('utf-8')
            padding = len(padded_payload) % 16
            if padding != 0:
                for i in range(16 - padding):
                    padded_payload += ' '

            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            encrypted_payload = cipher.encrypt(padded_payload)
            temp = iv + encrypted_payload
            data_payload = base64.b64encode(temp)
            data_frame['data'] = data_payload.decode('utf-8')
            try:
                requests_payload = {'data': json.dumps(data_frame)}
                r = requests.post(self.host, verify=True, data=requests_payload)
                if r.status_code != 200:
                    error_code = ErrorCodes.WEB_BRIDGE_ERROR
                else:
                    data_recv = r.text
                    json_data = json.loads(data_recv)
                    if 'code' in json_data.keys():
                        error_code = json_data['code']
                    elif 'Code' in json_data.keys():
                        error_code = json_data['Code']
                    else:
                        raise ValueError('Received data does not contain status code.')
            except Exception as e:
                print e
                error_code = ErrorCodes.CLIENT_CONNECTION_ERROR

            if error_code is None:
                pass
            elif error_code == ErrorCodes.NO_ERROR:
                break
            elif error_code == ErrorCodes.DATABASE_ERROR:
                pass
            elif error_code == ErrorCodes.AUTH_ERROR:
                break
            elif error_code == ErrorCodes.ILLEGAL_MSG_ERROR:
                break
            elif error_code == ErrorCodes.GOOGLE_MSG_TOO_LARGE:
                break
            elif error_code == ErrorCodes.GOOGLE_CONNECTION:
                pass
            elif error_code == ErrorCodes.GOOGLE_AUTH:
                pass
            elif error_code == ErrorCodes.VERSION_MISSMATCH:
                break
            elif error_code == ErrorCodes.NO_NOTIFICATION_PERMISSION:
                break
            elif error_code == ErrorCodes.WEB_BRIDGE_ERROR:
                pass
            else:
                break
            if max_retries_ctr == 0:
                break
            elif max_retries_ctr < 0:
                pass
            else:
                max_retries_ctr -= 1
            time.sleep(times_sleep)
            times_sleep *= 2
            if times_sleep > 86400:
                times_sleep = 86400

        return error_code

    def send_msg(self, subject, message, channel, state=None, time_triggered=None, max_retries=16):
        """
        Send push notification message to the push server.

        :param subject: subject of the message to send.
        :param message: the text body of the message to send.
        :param channel: the channel the message is sent to.
        :param state: state of the message send (1 for "triggered", 0 for "normal", None for no state) (optional).
        :param time_triggered: time the alarm message was triggered (if not given the current time is used) (optional).
        :param max_retries: maximum number of retries (if -1 we try forever) (optional).
        :return: returns error code (described by class ErrorCodes).
        """
        subject, message = self._trunc_to_size(subject, message)
        if not self._check_channel(channel):
            raise ValueError('Channel contains illegal characters.')
        is_sa = False
        if state is not None:
            is_sa = True
            if state != 0 and state != 1:
                raise ValueError('State has to be either 0 or 1 when given.')
        if time_triggered is None:
            tt = int(time.time())
        else:
            tt = int(time_triggered)
        payload = {'sbj': subject, 
           'msg': message, 
           'tt': tt, 
           'is_sa': is_sa}
        if is_sa:
            payload['st'] = state
        prefixed_channel = self._generate_prefixed_channel(channel)
        data_frame = {'username': self.username, 'password': self.password, 
           'channel': prefixed_channel, 
           'version': 0.1}
        return self._send_msg(data_frame, payload, max_retries)