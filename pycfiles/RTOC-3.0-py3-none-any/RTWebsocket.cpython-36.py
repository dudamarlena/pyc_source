# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\RTWebsocket.py
# Compiled at: 2019-12-26 21:59:06
# Size of source mod 2**32: 5118 bytes
import traceback, json, base64, logging as log
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)
try:
    from Cryptodome.Cipher import AES
    from Cryptodome import Random
    import hashlib
except (SystemError, ImportError):
    AES = None
    logging.warning('CryptodomeX or hashlib not installed! Install with "pip3 install pycryptodomex"')

BLOCK_SIZE = 16

class NoPasswordProtectionError(Exception):
    __doc__ = '\n    Raised when a password was provided, but server has no protectionAttributes.\n\n    Attributes:\n        expression -- input expression in which the error occurred\n        message -- explanation of the error\n    '

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class WrongPasswordError(Exception):
    __doc__ = '\n    Raised when the password is wrong.\n\n    Attributes:\n        expression -- input expression in which the error occurred\n        message -- explanation of the error\n    '

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class PasswordProtectedError(Exception):
    __doc__ = '\n    Raised when the server may be password protected.\n\n    Attributes:\n        expression -- input expression in which the error occurred\n        message -- explanation of the error\n    '

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def send(data, key=None):
    try:
        serialized = json.dumps(data)
    except (TypeError, ValueError):
        logging.debug(traceback.format_exc())
        print(traceback.format_exc())
        raise Exception('You can only send JSON-serializable data')

    if key is not None:
        if AES is not None:
            message = serialized.encode('utf-8')
            IV = Random.new().read(BLOCK_SIZE)
            aes = AES.new(key, AES.MODE_CBC, IV)
            serialized = base64.b64encode(IV + aes.encrypt(pad(message)))
    else:
        serialized = serialized.encode('utf-8')
    return serialized


def hashPassword(key, full=False):
    hash_object = hashlib.sha256(key.encode('utf-8'))
    secret_key = base64.b64encode(hash_object.digest())
    if full is False:
        secret_key = secret_key[:16]
    return secret_key


def recv(data, key=None):
    if key is not None:
        if AES is not None:
            try:
                encrypted = base64.b64decode(data)
                IV = encrypted[:BLOCK_SIZE]
                aes = AES.new(key, AES.MODE_CBC, IV)
                decrypted = aes.decrypt(encrypted[BLOCK_SIZE:])
                decrypted = unpad(decrypted)
                return json.loads(decrypted.decode('utf-8'))
            except Exception:
                tb = traceback.format_exc()
                logging.error(tb)
                raise WrongPasswordError('SOCKET PASSWORD ERROR', 'The provided password is wrong!')

        else:
            raise NoPasswordProtectionError('SOCKET ENCRYPTION ERROR', 'AES-encryption is not available!\nAborted')
    else:
        try:
            logging.warning('You are using an unencrypted websocket-connection. This is not safe! Please set a password in config.json')
            return json.loads(data)
        except (TypeError, ValueError):
            tb = traceback.format_exc()
            logging.debug(tb)
            raise PasswordProtectedError('JSON SOCKET ERROR', 'Data received was not in JSON format. Maybe the RTOC-Server is password-protected')


def pad(data):
    length = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + chr(length).encode('utf-8') * length


def unpad(data):
    return data[:-data[(-1)]]


if __name__ == '__main__':
    password = 'geheim'
    key = hashPassword(password)
    msg = {'Wow': 'true'}
    encrypted_msg = send(msg, key)
    decrypted_msg = recv(encrypted_msg, key)
    print('Password: {}, Key: {}'.format(password, key))
    print(encrypted_msg)
    if decrypted_msg == msg:
        print('LOCAL ENCRYPTION OK')
    else:
        print('LOCAL ENCRYPTION FAILED')
    msg = {'Wow': True}
    encrypted_msg = 'AqA9v8IMAWYhQ4fDc/p5IZJwel6zGhGtQGeR3rKqKSM='
    decrypted_msg = recv(encrypted_msg, key)
    print('Password: {}, Key: {}'.format(password, key))
    print(encrypted_msg)
    print(decrypted_msg)
    if decrypted_msg == msg:
        print('TYPESCRIPT ENCRYPTION OK')
    else:
        print('TYPESCRIPT ENCRYPTION FAILED')