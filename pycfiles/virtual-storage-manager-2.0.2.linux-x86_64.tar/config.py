# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/manifest/config.py
# Compiled at: 2016-06-13 14:11:03
"""
Agent Service
"""
import os, json, re, time
from vsm import exception
from vsm import flags
from vsm.openstack.common import log as logging
from vsm import utils
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

def set_keyring_admin(keyring_admin):
    """Set keyring admin file."""
    if not os.path.exists(FLAGS.keyring_admin):
        utils.write_file_as_root(FLAGS.keyring_admin, keyring_admin, 'w')
    else:
        LOG.info('Error keyring file exists')
        LOG.info('Back up & cover the old version')
        old_content = open(FLAGS.keyring_admin, 'r').read()
        if cmp(keyring_admin.strip(), old_content.strip()):
            bfx = time.asctime().replace(' ', '_').replace(':', '_')
            old_fname = FLAGS.keyring_admin + bfx
            utils.write_file_as_root(old_fname, old_content, 'w')
            utils.write_file_as_root(FLAGS.keyring_admin, keyring_admin, 'w')
        else:
            LOG.info('Have the same content, pass')


def is_vsm_ok():
    """Check vsm.conf is configured."""
    vcf = file(FLAGS.vsm_config).read()
    apf = file(FLAGS.api_paste_config).read()
    if re.search('MYSQL_VSM_PASSWORD', vcf) or re.search('MYSQL_VSM_USER', vcf) or re.search('RABBITMQ_HOST', vcf) or re.search('RABBITMQ_PASSWORD', vcf) or re.search('RABBITMQ_PORT', vcf) or re.search('SERVICE_TENANT_NAME', apf) or re.search('SERVICE_USER', apf) or re.search('SERVICE_PASSWORD', apf):
        return False
    return True


def set_vsm_conf(recv):
    """Write vsm conf files."""
    if recv is None:
        return False
    else:
        old_recv = recv
        try:
            recv = json.loads(recv)
        except TypeError:
            recv = old_recv
            LOG.info('Maybe recv is not json.')

        if not recv.get('api-paste.ini', None):
            LOG.error('Can not find content of api-paste.ini')
            raise exception.NotFound()
        if not recv.get('vsm.conf', None):
            LOG.error('Can not find content of vsm.conf')
            raise exception.NotFound()
        files = ['api-paste.ini', 'vsm.conf']
        for conf in files:
            conf_path = FLAGS.vsm_config_path + conf
            utils.write_file_as_root(conf_path, recv[conf], 'w')

        return True