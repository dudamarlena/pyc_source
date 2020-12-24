# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/cloudfront/origin.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6060 bytes
from boto.cloudfront.identity import OriginAccessIdentity

def get_oai_value(origin_access_identity):
    if isinstance(origin_access_identity, OriginAccessIdentity):
        return origin_access_identity.uri()
    else:
        return origin_access_identity


class S3Origin(object):
    """S3Origin"""

    def __init__(self, dns_name=None, origin_access_identity=None):
        """
        :param dns_name: The DNS name of your Amazon S3 bucket to
                         associate with the distribution.
                         For example: mybucket.s3.amazonaws.com.
        :type dns_name: str
        
        :param origin_access_identity: The CloudFront origin access
                                       identity to associate with the
                                       distribution. If you want the
                                       distribution to serve private content,
                                       include this element; if you want the
                                       distribution to serve public content,
                                       remove this element.
        :type origin_access_identity: str
        
        """
        self.dns_name = dns_name
        self.origin_access_identity = origin_access_identity

    def __repr__(self):
        return '<S3Origin: %s>' % self.dns_name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'DNSName':
            self.dns_name = value
        else:
            if name == 'OriginAccessIdentity':
                self.origin_access_identity = value
            else:
                setattr(self, name, value)

    def to_xml(self):
        s = '  <S3Origin>\n'
        s += '    <DNSName>%s</DNSName>\n' % self.dns_name
        if self.origin_access_identity:
            val = get_oai_value(self.origin_access_identity)
            s += '    <OriginAccessIdentity>%s</OriginAccessIdentity>\n' % val
        s += '  </S3Origin>\n'
        return s


class CustomOrigin(object):
    """CustomOrigin"""

    def __init__(self, dns_name=None, http_port=80, https_port=443, origin_protocol_policy=None):
        """
        :param dns_name: The DNS name of your Amazon S3 bucket to
                         associate with the distribution.
                         For example: mybucket.s3.amazonaws.com.
        :type dns_name: str
        
        :param http_port: The HTTP port the custom origin listens on.
        :type http_port: int
        
        :param https_port: The HTTPS port the custom origin listens on.
        :type http_port: int
        
        :param origin_protocol_policy: The origin protocol policy to
                                       apply to your origin. If you
                                       specify http-only, CloudFront
                                       will use HTTP only to access the origin.
                                       If you specify match-viewer, CloudFront
                                       will fetch from your origin using HTTP
                                       or HTTPS, based on the protocol of the
                                       viewer request.
        :type origin_protocol_policy: str
        
        """
        self.dns_name = dns_name
        self.http_port = http_port
        self.https_port = https_port
        self.origin_protocol_policy = origin_protocol_policy

    def __repr__(self):
        return '<CustomOrigin: %s>' % self.dns_name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'DNSName':
            self.dns_name = value
        elif name == 'HTTPPort':
            try:
                self.http_port = int(value)
            except ValueError:
                self.http_port = value

        elif name == 'HTTPSPort':
            try:
                self.https_port = int(value)
            except ValueError:
                self.https_port = value

        else:
            if name == 'OriginProtocolPolicy':
                self.origin_protocol_policy = value
            else:
                setattr(self, name, value)

    def to_xml(self):
        s = '  <CustomOrigin>\n'
        s += '    <DNSName>%s</DNSName>\n' % self.dns_name
        s += '    <HTTPPort>%d</HTTPPort>\n' % self.http_port
        s += '    <HTTPSPort>%d</HTTPSPort>\n' % self.https_port
        s += '    <OriginProtocolPolicy>%s</OriginProtocolPolicy>\n' % self.origin_protocol_policy
        s += '  </CustomOrigin>\n'
        return s