# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_client/cfg.py
# Compiled at: 2019-09-23 08:32:07
# Size of source mod 2**32: 2043 bytes
"""
client for EKCA service -- config helper stuff
"""
import os, sys
from configparser import ConfigParser
__all__ = [
 'read_config',
 'check_ca_certs']
SSH_CMD_DIR = {'linux': '/usr/bin'}
if sys.platform == 'win32':
    EXEC_SUFFIX = '.exe'
else:
    EXEC_SUFFIX = ''

def read_config():
    """
    read client config file
    """
    cfg_filename = os.environ.get('EKCA_CFG', os.path.join(os.path.expanduser('~'), '.ekca_client'))
    if not os.path.exists(cfg_filename):
        raise SystemExit('Configuration file %r is missing!' % cfg_filename)
    cfg = ConfigParser(defaults=dict(ca_certs='',
      ssh_cmd_dir=(SSH_CMD_DIR.get(sys.platform, '/usr/bin')),
      ssh_keygen=('ssh-keygen' + EXEC_SUFFIX),
      ssh_add=('ssh-add' + EXEC_SUFFIX),
      otp_regex='^[0-9]{6}$'),
      default_section='ekca_client')
    cfg.read([cfg_filename], encoding=(sys.stdin.encoding))
    ekca_client_cfg = cfg['ekca_client']
    for cmd_key in ('ssh_add', 'ssh_keygen'):
        ekca_client_cfg[cmd_key] = os.path.join(ekca_client_cfg['ssh_cmd_dir'], ekca_client_cfg[cmd_key])
        if not os.path.exists(ekca_client_cfg[cmd_key]):
            raise SystemExit('CLI tool %r is missing!' % ekca_client_cfg[cmd_key])

    del ekca_client_cfg['ssh_cmd_dir']
    return ekca_client_cfg


def check_ca_certs(cfg):
    """
    check whether CA cert file from configuration exists and is readable
    """
    if not cfg['ca_certs']:
        return
    ca_certs_filename = cfg['ca_certs']
    if not os.path.exists(ca_certs_filename):
        raise SystemExit('Configured CA certificate file %r is missing!' % ca_certs_filename)
    try:
        open(ca_certs_filename, 'rb').read()
    except IOError as io_error:
        try:
            raise SystemExit('Error reading CA certificate file %r: %s' % (
             ca_certs_filename,
             io_error))
        finally:
            io_error = None
            del io_error