# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dame/configuration.py
# Compiled at: 2020-05-04 13:31:17
# Size of source mod 2**32: 1417 bytes
import configparser, os, pathlib
__DEFAULT_MINT_API_CREDENTIALS_FILE__ = '~/.mint/credentials'
import click
DEFAULT_PROFILE = 'default'

def get_credentials(profile):
    credentials_file = pathlib.Path(os.getenv('MINT_CREDENTIALS_FILE', __DEFAULT_MINT_API_CREDENTIALS_FILE__)).expanduser()
    credentials = configparser.ConfigParser()
    if credentials_file.exists():
        credentials.read(credentials_file)
        return credentials[profile]
    if credentials is not None:
        if profile not in credentials:
            if profile != '%s' % DEFAULT_PROFILE:
                click.secho(("WARNING: The profile doesn't exists. To configure it, run:\ndame configure -p {}".format(profile)), fg='yellow')


def configure_credentials(server, username, profile):
    credentials_file = pathlib.Path(os.getenv('MINT_CREDENTIALS_FILE', __DEFAULT_MINT_API_CREDENTIALS_FILE__)).expanduser()
    os.makedirs((str(credentials_file.parent)), exist_ok=True)
    credentials = configparser.ConfigParser()
    credentials.optionxform = str
    if credentials_file.exists():
        credentials.read(credentials_file)
    credentials[profile] = {'server':server, 
     'username':username}
    with credentials_file.open('w') as (fh):
        credentials_file.parent.chmod(448)
        credentials_file.chmod(384)
        credentials.write(fh)