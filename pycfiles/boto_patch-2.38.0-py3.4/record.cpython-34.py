# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/route53/record.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 14689 bytes
RECORD_TYPES = [
 'A', 'AAAA', 'TXT', 'CNAME', 'MX', 'PTR', 'SRV', 'SPF']
from boto.resultset import ResultSet

class ResourceRecordSets(ResultSet):
    __doc__ = '\n    A list of resource records.\n\n    :ivar hosted_zone_id: The ID of the hosted zone.\n    :ivar comment: A comment that will be stored with the change.\n    :ivar changes: A list of changes.\n    '
    ChangeResourceRecordSetsBody = '<?xml version="1.0" encoding="UTF-8"?>\n    <ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2013-04-01/">\n            <ChangeBatch>\n                <Comment>%(comment)s</Comment>\n                <Changes>%(changes)s</Changes>\n            </ChangeBatch>\n        </ChangeResourceRecordSetsRequest>'
    ChangeXML = '<Change>\n        <Action>%(action)s</Action>\n        %(record)s\n    </Change>'

    def __init__(self, connection=None, hosted_zone_id=None, comment=None):
        self.connection = connection
        self.hosted_zone_id = hosted_zone_id
        self.comment = comment
        self.changes = []
        self.next_record_name = None
        self.next_record_type = None
        self.next_record_identifier = None
        super(ResourceRecordSets, self).__init__([('ResourceRecordSet', Record)])

    def __repr__(self):
        if self.changes:
            record_list = ','.join([c.__repr__() for c in self.changes])
        else:
            record_list = ','.join([record.__repr__() for record in self])
        return '<ResourceRecordSets:%s [%s]' % (self.hosted_zone_id,
         record_list)

    def add_change(self, action, name, type, ttl=600, alias_hosted_zone_id=None, alias_dns_name=None, identifier=None, weight=None, region=None, alias_evaluate_target_health=None, health_check=None, failover=None):
        """
        Add a change request to the set.

        :type action: str
        :param action: The action to perform ('CREATE'|'DELETE'|'UPSERT')

        :type name: str
        :param name: The name of the domain you want to perform the action on.

        :type type: str
        :param type: The DNS record type.  Valid values are:

            * A
            * AAAA
            * CNAME
            * MX
            * NS
            * PTR
            * SOA
            * SPF
            * SRV
            * TXT

        :type ttl: int
        :param ttl: The resource record cache time to live (TTL), in seconds.

        :type alias_hosted_zone_id: str
        :param alias_dns_name: *Alias resource record sets only* The value
            of the hosted zone ID, CanonicalHostedZoneNameId, for
            the LoadBalancer.

        :type alias_dns_name: str
        :param alias_hosted_zone_id: *Alias resource record sets only*
            Information about the domain to which you are redirecting traffic.

        :type identifier: str
        :param identifier: *Weighted and latency-based resource record sets
            only* An identifier that differentiates among multiple resource
            record sets that have the same combination of DNS name and type.

        :type weight: int
        :param weight: *Weighted resource record sets only* Among resource
            record sets that have the same combination of DNS name and type,
            a value that determines what portion of traffic for the current
            resource record set is routed to the associated location

        :type region: str
        :param region: *Latency-based resource record sets only* Among resource
            record sets that have the same combination of DNS name and type,
            a value that determines which region this should be associated with
            for the latency-based routing

        :type alias_evaluate_target_health: bool
        :param alias_evaluate_target_health: *Required for alias resource record
            sets* Indicates whether this Resource Record Set should respect the
            health status of any health checks associated with the ALIAS target
            record which it is linked to.

        :type health_check: str
        :param health_check: Health check to associate with this record

        :type failover: str
        :param failover: *Failover resource record sets only* Whether this is the
            primary or secondary resource record set.
        """
        change = Record(name, type, ttl, alias_hosted_zone_id=alias_hosted_zone_id, alias_dns_name=alias_dns_name, identifier=identifier, weight=weight, region=region, alias_evaluate_target_health=alias_evaluate_target_health, health_check=health_check, failover=failover)
        self.changes.append([action, change])
        return change

    def add_change_record(self, action, change):
        """Add an existing record to a change set with the specified action"""
        self.changes.append([action, change])

    def to_xml(self):
        """Convert this ResourceRecordSet into XML
        to be saved via the ChangeResourceRecordSetsRequest"""
        changesXML = ''
        for change in self.changes:
            changeParams = {'action': change[0],  'record': change[1].to_xml()}
            changesXML += self.ChangeXML % changeParams

        params = {'comment': self.comment,  'changes': changesXML}
        return self.ChangeResourceRecordSetsBody % params

    def commit(self):
        """Commit this change"""
        if not self.connection:
            import boto
            self.connection = boto.connect_route53()
        return self.connection.change_rrsets(self.hosted_zone_id, self.to_xml())

    def endElement(self, name, value, connection):
        """Overwritten to also add the NextRecordName,
        NextRecordType and NextRecordIdentifier to the base object"""
        if name == 'NextRecordName':
            self.next_record_name = value
        else:
            if name == 'NextRecordType':
                self.next_record_type = value
            else:
                if name == 'NextRecordIdentifier':
                    self.next_record_identifier = value
                else:
                    return super(ResourceRecordSets, self).endElement(name, value, connection)

    def __iter__(self):
        """Override the next function to support paging"""
        results = super(ResourceRecordSets, self).__iter__()
        truncated = self.is_truncated
        while results:
            for obj in results:
                yield obj

            if self.is_truncated:
                self.is_truncated = False
                results = self.connection.get_all_rrsets(self.hosted_zone_id, name=self.next_record_name, type=self.next_record_type, identifier=self.next_record_identifier)
            else:
                results = None
                self.is_truncated = truncated


class Record(object):
    __doc__ = 'An individual ResourceRecordSet'
    HealthCheckBody = '<HealthCheckId>%s</HealthCheckId>'
    XMLBody = '<ResourceRecordSet>\n        <Name>%(name)s</Name>\n        <Type>%(type)s</Type>\n        %(weight)s\n        %(body)s\n        %(health_check)s\n    </ResourceRecordSet>'
    WRRBody = '\n        <SetIdentifier>%(identifier)s</SetIdentifier>\n        <Weight>%(weight)s</Weight>\n    '
    RRRBody = '\n        <SetIdentifier>%(identifier)s</SetIdentifier>\n        <Region>%(region)s</Region>\n    '
    FailoverBody = '\n        <SetIdentifier>%(identifier)s</SetIdentifier>\n        <Failover>%(failover)s</Failover>\n    '
    ResourceRecordsBody = '\n        <TTL>%(ttl)s</TTL>\n        <ResourceRecords>\n            %(records)s\n        </ResourceRecords>'
    ResourceRecordBody = '<ResourceRecord>\n        <Value>%s</Value>\n    </ResourceRecord>'
    AliasBody = '<AliasTarget>\n        <HostedZoneId>%(hosted_zone_id)s</HostedZoneId>\n        <DNSName>%(dns_name)s</DNSName>\n        %(eval_target_health)s\n    </AliasTarget>'
    EvaluateTargetHealth = '<EvaluateTargetHealth>%s</EvaluateTargetHealth>'

    def __init__(self, name=None, type=None, ttl=600, resource_records=None, alias_hosted_zone_id=None, alias_dns_name=None, identifier=None, weight=None, region=None, alias_evaluate_target_health=None, health_check=None, failover=None):
        self.name = name
        self.type = type
        self.ttl = ttl
        if resource_records is None:
            resource_records = []
        self.resource_records = resource_records
        self.alias_hosted_zone_id = alias_hosted_zone_id
        self.alias_dns_name = alias_dns_name
        self.identifier = identifier
        self.weight = weight
        self.region = region
        self.alias_evaluate_target_health = alias_evaluate_target_health
        self.health_check = health_check
        self.failover = failover

    def __repr__(self):
        return '<Record:%s:%s:%s>' % (self.name, self.type, self.to_print())

    def add_value(self, value):
        """Add a resource record value"""
        self.resource_records.append(value)

    def set_alias(self, alias_hosted_zone_id, alias_dns_name, alias_evaluate_target_health=False):
        """Make this an alias resource record set"""
        self.alias_hosted_zone_id = alias_hosted_zone_id
        self.alias_dns_name = alias_dns_name
        self.alias_evaluate_target_health = alias_evaluate_target_health

    def to_xml(self):
        """Spit this resource record set out as XML"""
        if self.alias_hosted_zone_id is not None and self.alias_dns_name is not None:
            if self.alias_evaluate_target_health is not None:
                eval_target_health = self.EvaluateTargetHealth % ('true' if self.alias_evaluate_target_health else 'false')
            else:
                eval_target_health = ''
            body = self.AliasBody % {'hosted_zone_id': self.alias_hosted_zone_id,  'dns_name': self.alias_dns_name, 
             'eval_target_health': eval_target_health}
        else:
            records = ''
            for r in self.resource_records:
                records += self.ResourceRecordBody % r

            body = self.ResourceRecordsBody % {'ttl': self.ttl, 
             'records': records}
        weight = ''
        if self.identifier is not None and self.weight is not None:
            weight = self.WRRBody % {'identifier': self.identifier,  'weight': self.weight}
        else:
            if self.identifier is not None and self.region is not None:
                weight = self.RRRBody % {'identifier': self.identifier,  'region': self.region}
            elif self.identifier is not None:
                if self.failover is not None:
                    weight = self.FailoverBody % {'identifier': self.identifier,  'failover': self.failover}
        health_check = ''
        if self.health_check is not None:
            health_check = self.HealthCheckBody % self.health_check
        params = {'name': self.name, 
         'type': self.type, 
         'weight': weight, 
         'body': body, 
         'health_check': health_check}
        return self.XMLBody % params

    def to_print(self):
        rr = ''
        if self.alias_hosted_zone_id is not None and self.alias_dns_name is not None:
            rr = 'ALIAS ' + self.alias_hosted_zone_id + ' ' + self.alias_dns_name
            if self.alias_evaluate_target_health is not None:
                rr += ' (EvalTarget %s)' % self.alias_evaluate_target_health
        else:
            rr = ','.join(self.resource_records)
        if self.identifier is not None and self.weight is not None:
            rr += ' (WRR id=%s, w=%s)' % (self.identifier, self.weight)
        else:
            if self.identifier is not None and self.region is not None:
                rr += ' (LBR id=%s, region=%s)' % (self.identifier, self.region)
            elif self.identifier is not None:
                if self.failover is not None:
                    rr += ' (FAILOVER id=%s, failover=%s)' % (self.identifier, self.failover)
        return rr

    def endElement(self, name, value, connection):
        if name == 'Name':
            self.name = value
        else:
            if name == 'Type':
                self.type = value
            else:
                if name == 'TTL':
                    self.ttl = value
                else:
                    if name == 'Value':
                        self.resource_records.append(value)
                    else:
                        if name == 'HostedZoneId':
                            self.alias_hosted_zone_id = value
                        else:
                            if name == 'DNSName':
                                self.alias_dns_name = value
                            else:
                                if name == 'SetIdentifier':
                                    self.identifier = value
                                else:
                                    if name == 'EvaluateTargetHealth':
                                        self.alias_evaluate_target_health = value.lower() == 'true'
                                    else:
                                        if name == 'Weight':
                                            self.weight = value
                                        else:
                                            if name == 'Region':
                                                self.region = value
                                            else:
                                                if name == 'Failover':
                                                    self.failover = value
                                                elif name == 'HealthCheckId':
                                                    self.health_check = value

    def startElement(self, name, attrs, connection):
        pass