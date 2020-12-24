# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/certificates_enddate.py
# Compiled at: 2019-05-16 13:41:33
"""
CertificatesEnddate - command ``/usr/bin/openssl x509 -noout -enddate -in path/to/cert/file``
=============================================================================================

This command gets the enddates of certificate files.

Typical output of this command is::

    /usr/bin/find: '/etc/origin/node': No such file or directory
    /usr/bin/find: '/etc/origin/master': No such file or directory
    notAfter=May 25 16:39:40 2019 GMT
    FileName= /etc/origin/node/cert.pem
    unable to load certificate
    139881193203616:error:0906D066:PEM routines:PEM_read_bio:bad end line:pem_lib.c:802:
    unable to load certificate
    140695459370912:error:0906D06C:PEM routines:PEM_read_bio:no start line:pem_lib.c:703:Expecting: TRUSTED CERTIFICATE
    notAfter=May 25 16:39:40 2019 GMT
    FileName= /etc/pki/ca-trust/extracted/pem/email-ca-bundle.pem
    notAfter=Dec  9 10:55:38 2017 GMT
    FileName= /etc/pki/consumer/cert.pem
    notAfter=Jan  1 04:59:59 2022 GMT
    FileName= /etc/pki/entitlement/3343502840335059594.pem
    notAfter=Aug 31 02:19:59 2017 GMT
    FileName= /etc/pki/consumer/cert.pem
    notAfter=Jan  1 04:59:59 2022 GMT
    FileName= /etc/pki/entitlement/2387590574974617178.pem

Examples:
    >>> cert_enddate = shared[CertificatesEnddate]
    >>> paths = cert_enddate.get_certificates_path
    >>> paths[0]
    '/etc/origin/node/cert.pem'
    >>> cert_enddate.expiration_date(paths[0]).datetime
    datetime(2019, 05, 25, 16, 39, 40)
    >>> cert_enddate.expiration_date(paths[0]).str
    'May 25 16:39:40 2019'
"""
from datetime import datetime
from collections import namedtuple
from .. import parser, LegacyItemAccess, CommandParser
from insights.specs import Specs

@parser(Specs.certificates_enddate)
class CertificatesEnddate(LegacyItemAccess, CommandParser):
    """Class to parse the expiration dates."""
    ExpirationDate = namedtuple('ExpirationDate', ['str', 'datetime'])

    def parse_content(self, content):
        """Parse the content of crt files."""
        self.data = {}
        datestamp = None
        for l in content:
            if datestamp and l.startswith('FileName='):
                self.data[l.split('=')[(-1)].strip()] = datestamp
                datestamp = None
            elif l.startswith('notAfter='):
                datestamp = l.split('=')[(-1)].rsplit(' ', 1)[0]
            else:
                datestamp = None

        return

    @property
    def certificates_path(self):
        """list: Return filepaths in list or []."""
        if self.data:
            return self.data.keys()
        return []

    def expiration_date(self, path):
        """This will return a namedtuple(['str', 'datetime']) contains the
        expiration date in string and datetime format. If the expiration date
        is unparsable, the ExpirationDate.datetime should be None.

        Args:
            path(str): The certificate file path.

        Returns:
            A ExpirationDate for available path. None otherwise.
        """
        path_date = self.data.get(path)
        if path_date:
            try:
                path_datetime = datetime.strptime(path_date, '%b %d %H:%M:%S %Y')
                return self.ExpirationDate(path_date, path_datetime)
            except:
                return self.ExpirationDate(path_date, None)

        return