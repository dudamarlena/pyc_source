# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /root/Documents/ros-cli/ros/apps/config.py
# Compiled at: 2017-08-16 04:51:54
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
import NewConfigParser, os, sys, re
reload(sys)
sys.setdefaultencoding('utf-8')
ACCESS_KEY_ID = None
ACCESS_KEY_SECRET = None
REGION_ID = None
client = None
JSON_FORM = False
JSON_INDENT = 2
ROS_DEBUG = False

def current_conf():
    """
    Print current client configuration
    :return: None
    """
    global ACCESS_KEY_ID
    global ACCESS_KEY_SECRET
    global REGION_ID
    print '[DEBUG] Current Config:\nACCESS_KEY_ID: %s\nACCESS_KEY_SECRET: %s\nREGION_ID: %s\n' % (
     ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)


def set_client(cfg_file, region_id, top_dir=None):
    """
    Configure client
    :param cfg_file: specify the configuration file
    :param region_id: specify region id
    :param top_dir: working path
    :return: None
    """
    global ACCESS_KEY_ID
    global ACCESS_KEY_SECRET
    global JSON_INDENT
    global REGION_ID
    global ROS_DEBUG
    global client
    if top_dir is None:
        default_file = 'ros/ros.conf'
    else:
        default_file = os.path.normpath(top_dir + '/ros/ros.conf')
    cf = NewConfigParser.NewConfigParser()
    if cfg_file is None:
        if ROS_DEBUG:
            print 'Use default config file: %s\n' % default_file
        cfg_file = default_file
    if os.path.isfile(cfg_file):
        pass
    else:
        if os.path.isdir(top_dir + '/ros'):
            pass
        else:
            os.mkdir(top_dir + '/ros')
        print 'Please set Aliyun access info first.'
        access_key_id = raw_input('Enter your access key id:')
        while check_access_info(access_key_id) is False:
            access_key_id = raw_input('Enter your access key id, only characters and numbers:')

        access_key_secret = raw_input('Enter your access key secret, without quote:')
        while check_access_info(access_key_secret) is False:
            access_key_secret = raw_input('Enter your access key secret, only characters and numbers:')

        default_region_id = raw_input('Enter default region id, without quote:')
        cf.add_section('ACCESS')
        cf.set('ACCESS', 'ACCESS_KEY_ID', access_key_id)
        cf.set('ACCESS', 'ACCESS_KEY_SECRET', access_key_secret)
        cf.set('ACCESS', 'REGION_ID', default_region_id)
        cf.add_section('OTHER')
        cf.set('OTHER', 'JSON_INDENT', 2)
        cf.set('OTHER', 'DEBUG', False)
        with open(cfg_file, 'w') as (configfile):
            cf.write(configfile)
    try:
        cf.read(cfg_file)
    except BaseException:
        print 'Config file (%s) error, please write it like:\n\n        [ACCESS]\n        ACCESS_KEY_ID = YOUR_KEY_ID\n        ACCESS_KEY_SECRET = YOUR_KEY_SECRET\n        REGION_ID = cn-beijing\n\n        [OTHER]\n        JSON_INDENT = 2\n        DEBUG = False\n        ' % cfg_file
        sys.exit(1)

    ACCESS_KEY_ID = cf.get('ACCESS', 'ACCESS_KEY_ID')
    ACCESS_KEY_SECRET = cf.get('ACCESS', 'ACCESS_KEY_SECRET')
    if region_id is None:
        REGION_ID = cf.get('ACCESS', 'REGION_ID')
    else:
        REGION_ID = region_id
    JSON_INDENT = int(cf.get('OTHER', 'JSON_INDENT'))
    ROS_DEBUG = bool(cf.get('OTHER', 'DEBUG') == 'True')
    client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION_ID)
    if ROS_DEBUG:
        current_conf()
    return


def check_access_info(info):
    """
    Check if access info only has characters and numbers
    """
    match = re.search('^[A-Za-z0-9]+$', info)
    if match:
        return True
    else:
        return False