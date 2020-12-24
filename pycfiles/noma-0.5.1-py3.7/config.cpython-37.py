# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noma/config.py
# Compiled at: 2019-09-25 06:48:41
# Size of source mod 2**32: 1543 bytes
"""
config.py defines configuration of filesystem structure

These constants are not to be changed during runtime

Pathlib objects represent PosixPaths
"""
from pathlib import Path
LND_MODE = 'neutrino'
LND_NET = 'mainnet'
MEDIA_PATH = Path('/media')
NOMA_SOURCE = MEDIA_PATH / 'noma'
SSH_PORT = '22'
SSH_IDENTITY = '~/.ssh/id_ed25519'
SSH_TARGET = 'user@ssh-hostname:/path/to/backup/dir/'
HOME_PATH = Path.home()
COMPOSE_MODE_PATH = NOMA_SOURCE / 'compose' / LND_MODE
LND_PATH = NOMA_SOURCE / 'lnd' / LND_MODE
LND_CONF = LND_PATH / 'lnd.conf'
CHAIN_PATH = LND_PATH / 'data' / 'chain' / 'bitcoin'
WALLET_PATH = CHAIN_PATH / LND_NET / 'wallet.db'
TLS_CERT_PATH = LND_PATH / 'tls.cert'
MACAROON_PATH = CHAIN_PATH / LND_NET / 'admin.macaroon'
SEED_FILENAME = LND_PATH / 'seed.txt'
CHANNEL_BACKUP = CHAIN_PATH / LND_NET / 'channel.backup'
SAVE_PASSWORD_CONTROL_FILE = LND_PATH / 'save_password'
PASSWORD_FILE_PATH = LND_PATH / 'password.txt'
URL_GRPC = '192.168.83.33:10009'
URL_GENSEED = 'https://127.0.0.1:8080/v1/genseed'
URL_INITWALLET = 'https://127.0.0.1:8080/v1/initwallet'
URL_UNLOCKWALLET = 'https://127.0.0.1:8080/v1/unlockwallet'