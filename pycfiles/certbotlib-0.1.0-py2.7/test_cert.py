# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/certbotlib/test_cert.py
# Compiled at: 2017-10-06 08:57:37
from certbotlib import Certbot
from awslib import Acm
import logging
logger = logging.getLogger('certbotlib')
logging.basicConfig(level=logging.INFO)
directory = '/Users/oriolfb/Desktop/certbotlib'
lets_encrypt_certs = []
acm = Acm(region='eu-central-1')
certificates = acm.get_expiring_certs_by_days(40)
for certificate in certificates:
    if 'Encrypt' in certificate.issuer:
        lets_encrypt_certs.append(certificate)

certbot = Certbot(email='devops@payconiq.com', logs_dir=directory, work_dir=directory, config_dir=directory, domain='test4.payconiq.io', region='eu-central-1', profile='oriol-prod')