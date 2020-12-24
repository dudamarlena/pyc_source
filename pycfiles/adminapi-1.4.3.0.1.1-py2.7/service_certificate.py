# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/services/service_certificate.py
# Compiled at: 2018-01-31 14:44:08
from cloud_admin.services import EucaBaseObj

class ServiceCertificate(EucaBaseObj):
    """
    Used to parse and objectify the DescribeServiceCertificate response.
    """

    def __init__(self, connection=None):
        self.certificate = None
        self.certificatefingerprint = None
        self.certificatefingerprintdigest = None
        self.certificateformat = None
        self.certificateusage = None
        self.connection = None
        super(ServiceCertificate, self).__init__(connection)
        return

    def endElement(self, name, value, connection):
        ename = name.lower().replace('euca:', '')
        if ename:
            if ename == 'certificateusage':
                self.certificateusage = value
                if self.name is None:
                    self.name = value
            else:
                setattr(self, ename.lower(), value)
        return