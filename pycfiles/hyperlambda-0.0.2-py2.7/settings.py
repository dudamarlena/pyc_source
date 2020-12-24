# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hyperlambda/settings.py
# Compiled at: 2018-02-13 05:00:49
import configparser, ast, base64, os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, 'data', 'config.ini'))
try:
    aws_access_key_id = config['aws_credentials']['aws_access_key_id']
    aws_secret_access_key = config['aws_credentials']['aws_secret_access_key']
    region = config['aws_credentials']['region']
except KeyError as e:
    error_info = ('configure {} in config.ini. Refer config_sample.ini at {} for more info').format(e, BASE_DIR)
    sys.exit(error_info)

try:
    image_id = 'ami-73f4a61c'
    security_group_ids = ast.literal_eval(config['instance_settings']['security_group_ids'])
    key_name = config['instance_settings']['key_name']
    volume_size = int(config['instance_settings']['volume_size'])
    instance_type = config['instance_settings']['instance_type']
    spot_price = config['instance_settings']['spot_price']
except KeyError as e:
    error_info = ('configure {} in config.ini. Refer config_sample.ini at {} for more info').format(e, BASE_DIR)
    sys.exit(error_info)

file = open(os.path.join(BASE_DIR, 'data', 'boot.sh'), 'r')
user_data = file.read().strip()
file.close()