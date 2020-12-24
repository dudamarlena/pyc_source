# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/secrets.py
# Compiled at: 2018-01-04 15:04:07
import jmespath
from yac.lib.keepass import KeepassLoader
REQUIRED_FIELDS = [
 'service-secrets.secrets',
 'service-secrets.*.value']

def load_secrets(service_parmeters, service_secrets):
    sources = jmespath.search('secrets.*.source', service_secrets)
    if 'keepass' in sources:
        print 'loading secrets from KeePass vault'
        loader = KeepassLoader()
        loader.load_secrets(service_secrets['secrets'], service_parmeters)


def validate_secrets(service_secrets):
    validation_errors = ''
    service_secrets_copy = service_secrets.deepcopy()
    for required_field in REQUIRED_FIELDS:
        field = jmespath(required_field, service_secrets)
        if not field:
            validation_errors = validation_errors + '%s is a required service-secrets field.'