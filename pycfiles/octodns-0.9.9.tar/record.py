# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/octodns/record.py
# Compiled at: 2018-12-14 12:47:00
from __future__ import absolute_import, division, print_function, unicode_literals
from ipaddress import IPv4Address, IPv6Address
from logging import getLogger
import re

class Change(object):

    def __init__(self, existing, new):
        self.existing = existing
        self.new = new

    @property
    def record(self):
        """Returns new if we have one, existing otherwise"""
        return self.new or self.existing


class Create(Change):

    def __init__(self, new):
        super(Create, self).__init__(None, new)
        return

    def __repr__(self, leader=b''):
        source = self.new.source.id if self.new.source else b''
        return (b'Create {} ({})').format(self.new, source)


class Update(Change):

    def __repr__(self, leader=b''):
        source = self.new.source.id if self.new.source else b''
        return (b'Update\n{leader}    {existing} ->\n{leader}    {new} ({src})').format(existing=self.existing, new=self.new, leader=leader, src=source)


class Delete(Change):

    def __init__(self, existing):
        super(Delete, self).__init__(existing, None)
        return

    def __repr__(self, leader=b''):
        return (b'Delete {}').format(self.existing)


class ValidationError(Exception):

    @classmethod
    def build_message(cls, fqdn, reasons):
        return (b'Invalid record {}\n  - {}').format(fqdn, (b'\n  - ').join(reasons))

    def __init__(self, fqdn, reasons):
        super(Exception, self).__init__(self.build_message(fqdn, reasons))
        self.fqdn = fqdn
        self.reasons = reasons


class Record(object):
    log = getLogger(b'Record')

    @classmethod
    def new(cls, zone, name, data, source=None, lenient=False):
        fqdn = (b'{}.{}').format(name, zone.name) if name else zone.name
        try:
            _type = data[b'type']
        except KeyError:
            raise Exception((b'Invalid record {}, missing type').format(fqdn))

        try:
            _class = {b'A': ARecord, 
               b'AAAA': AaaaRecord, 
               b'ALIAS': AliasRecord, 
               b'CAA': CaaRecord, 
               b'CNAME': CnameRecord, 
               b'MX': MxRecord, 
               b'NAPTR': NaptrRecord, 
               b'NS': NsRecord, 
               b'PTR': PtrRecord, 
               b'SPF': SpfRecord, 
               b'SRV': SrvRecord, 
               b'SSHFP': SshfpRecord, 
               b'TXT': TxtRecord}[_type]
        except KeyError:
            raise Exception((b'Unknown record type: "{}"').format(_type))

        reasons = _class.validate(name, data)
        try:
            lenient |= data[b'octodns'][b'lenient']
        except KeyError:
            pass

        if reasons:
            if lenient:
                cls.log.warn(ValidationError.build_message(fqdn, reasons))
            else:
                raise ValidationError(fqdn, reasons)
        return _class(zone, name, data, source=source)

    @classmethod
    def validate(cls, name, data):
        reasons = []
        try:
            ttl = int(data[b'ttl'])
            if ttl < 0:
                reasons.append(b'invalid ttl')
        except KeyError:
            reasons.append(b'missing ttl')

        try:
            if data[b'octodns'][b'healthcheck'][b'protocol'] not in ('HTTP', 'HTTPS'):
                reasons.append(b'invalid healthcheck protocol')
        except KeyError:
            pass

        return reasons

    def __init__(self, zone, name, data, source=None):
        self.log.debug(b'__init__: zone.name=%s, type=%11s, name=%s', zone.name, self.__class__.__name__, name)
        self.zone = zone
        self.name = unicode(name).lower() if name else name
        self.source = source
        self.ttl = int(data[b'ttl'])
        self._octodns = data.get(b'octodns', {})

    def _data(self):
        return {b'ttl': self.ttl}

    @property
    def data(self):
        return self._data()

    @property
    def fqdn(self):
        if self.name:
            return (b'{}.{}').format(self.name, self.zone.name)
        return self.zone.name

    @property
    def ignored(self):
        return self._octodns.get(b'ignored', False)

    @property
    def excluded(self):
        return self._octodns.get(b'excluded', [])

    @property
    def included(self):
        return self._octodns.get(b'included', [])

    @property
    def healthcheck_host(self):
        try:
            return self._octodns[b'healthcheck'][b'host']
        except KeyError:
            return self.fqdn[:-1]

    @property
    def healthcheck_path(self):
        try:
            return self._octodns[b'healthcheck'][b'path']
        except KeyError:
            return b'/_dns'

    @property
    def healthcheck_protocol(self):
        try:
            return self._octodns[b'healthcheck'][b'protocol']
        except KeyError:
            return b'HTTPS'

    @property
    def healthcheck_port(self):
        try:
            return int(self._octodns[b'healthcheck'][b'port'])
        except KeyError:
            return 443

    def changes(self, other, target):
        if self.ttl != other.ttl:
            return Update(self, other)

    def __hash__(self):
        return (b'{}:{}').format(self.name, self._type).__hash__()

    def __cmp__(self, other):
        a = (b'{}:{}').format(self.name, self._type)
        b = (b'{}:{}').format(other.name, other._type)
        return cmp(a, b)

    def __repr__(self):
        raise NotImplementedError(b'Abstract base class, __repr__ required')


class GeoValue(object):
    geo_re = re.compile(b'^(?P<continent_code>\\w\\w)(-(?P<country_code>\\w\\w)(-(?P<subdivision_code>\\w\\w))?)?$')

    @classmethod
    def _validate_geo(cls, code):
        reasons = []
        match = cls.geo_re.match(code)
        if not match:
            reasons.append((b'invalid geo "{}"').format(code))
        return reasons

    def __init__(self, geo, values):
        self.code = geo
        match = self.geo_re.match(geo)
        self.continent_code = match.group(b'continent_code')
        self.country_code = match.group(b'country_code')
        self.subdivision_code = match.group(b'subdivision_code')
        self.values = sorted(values)

    @property
    def parents(self):
        bits = self.code.split(b'-')[:-1]
        while bits:
            yield (b'-').join(bits)
            bits.pop()

    def __cmp__(self, other):
        if self.continent_code == other.continent_code and self.country_code == other.country_code and self.subdivision_code == other.subdivision_code and self.values == other.values:
            return 0
        return 1

    def __repr__(self):
        return (b"'Geo {} {} {} {}'").format(self.continent_code, self.country_code, self.subdivision_code, self.values)


class _ValuesMixin(object):

    @classmethod
    def validate(cls, name, data):
        reasons = super(_ValuesMixin, cls).validate(name, data)
        values = []
        try:
            values = data[b'values']
            if not values:
                values = []
                reasons.append(b'missing value(s)')
            else:
                for value in list(values):
                    if value is None:
                        reasons.append(b'missing value(s)')
                        values.remove(value)
                    elif len(value) == 0:
                        reasons.append(b'empty value')
                        values.remove(value)

        except KeyError:
            try:
                value = data[b'value']
                if value is None:
                    reasons.append(b'missing value(s)')
                    values = []
                elif len(value) == 0:
                    reasons.append(b'empty value')
                    values = []
                else:
                    values = [
                     value]
            except KeyError:
                reasons.append(b'missing value(s)')

        for value in values:
            reasons.extend(cls._validate_value(value))

        return reasons

    def __init__(self, zone, name, data, source=None):
        super(_ValuesMixin, self).__init__(zone, name, data, source=source)
        try:
            values = data[b'values']
        except KeyError:
            values = [
             data[b'value']]

        self.values = sorted(self._process_values(values))

    def changes(self, other, target):
        if self.values != other.values:
            return Update(self, other)
        return super(_ValuesMixin, self).changes(other, target)

    def _data(self):
        ret = super(_ValuesMixin, self)._data()
        if len(self.values) > 1:
            values = [ getattr(v, b'data', v) for v in self.values if v ]
            if len(values) > 1:
                ret[b'values'] = values
            elif len(values) == 1:
                ret[b'value'] = values[0]
        elif len(self.values) == 1:
            v = self.values[0]
            if v:
                ret[b'value'] = getattr(v, b'data', v)
        return ret

    def __repr__(self):
        values = (b"['{}']").format((b"', '").join([ unicode(v) for v in self.values
                                                   ]))
        return (b'<{} {} {}, {}, {}>').format(self.__class__.__name__, self._type, self.ttl, self.fqdn, values)


class _GeoMixin(_ValuesMixin):
    """
    Adds GeoDNS support to a record.

    Must be included before `Record`.
    """

    @classmethod
    def validate(cls, name, data):
        reasons = super(_GeoMixin, cls).validate(name, data)
        try:
            geo = dict(data[b'geo'])
            for code, values in geo.items():
                reasons.extend(GeoValue._validate_geo(code))
                for value in values:
                    reasons.extend(cls._validate_value(value))

        except KeyError:
            pass

        return reasons

    def __init__(self, zone, name, data, *args, **kwargs):
        super(_GeoMixin, self).__init__(zone, name, data, *args, **kwargs)
        try:
            self.geo = dict(data[b'geo'])
        except KeyError:
            self.geo = {}

        for code, values in self.geo.items():
            self.geo[code] = GeoValue(code, values)

    def _data(self):
        ret = super(_GeoMixin, self)._data()
        if self.geo:
            geo = {}
            for code, value in self.geo.items():
                geo[code] = value.values

            ret[b'geo'] = geo
        return ret

    def changes(self, other, target):
        if target.SUPPORTS_GEO:
            if self.geo != other.geo:
                return Update(self, other)
        return super(_GeoMixin, self).changes(other, target)

    def __repr__(self):
        if self.geo:
            return (b'<{} {} {}, {}, {}, {}>').format(self.__class__.__name__, self._type, self.ttl, self.fqdn, self.values, self.geo)
        return super(_GeoMixin, self).__repr__()


class ARecord(_GeoMixin, Record):
    _type = b'A'

    @classmethod
    def _validate_value(self, value):
        reasons = []
        try:
            IPv4Address(unicode(value))
        except Exception:
            reasons.append((b'invalid ip address "{}"').format(value))

        return reasons

    def _process_values(self, values):
        return values


class AaaaRecord(_GeoMixin, Record):
    _type = b'AAAA'

    @classmethod
    def _validate_value(self, value):
        reasons = []
        try:
            IPv6Address(unicode(value))
        except Exception:
            reasons.append((b'invalid ip address "{}"').format(value))

        return reasons

    def _process_values(self, values):
        return values


class _ValueMixin(object):

    @classmethod
    def validate(cls, name, data):
        reasons = super(_ValueMixin, cls).validate(name, data)
        value = None
        try:
            value = data[b'value']
            if value is None:
                reasons.append(b'missing value')
            elif value == b'':
                reasons.append(b'empty value')
        except KeyError:
            reasons.append(b'missing value')

        if value:
            reasons.extend(cls._validate_value(value))
        return reasons

    def __init__(self, zone, name, data, source=None):
        super(_ValueMixin, self).__init__(zone, name, data, source=source)
        self.value = self._process_value(data[b'value'])

    def changes(self, other, target):
        if self.value != other.value:
            return Update(self, other)
        return super(_ValueMixin, self).changes(other, target)

    def _data(self):
        ret = super(_ValueMixin, self)._data()
        if self.value:
            ret[b'value'] = getattr(self.value, b'data', self.value)
        return ret

    def __repr__(self):
        return (b'<{} {} {}, {}, {}>').format(self.__class__.__name__, self._type, self.ttl, self.fqdn, self.value)


class AliasRecord(_ValueMixin, Record):
    _type = b'ALIAS'

    @classmethod
    def _validate_value(self, value):
        reasons = []
        if not value.endswith(b'.'):
            reasons.append(b'missing trailing .')
        return reasons

    def _process_value(self, value):
        return value


class CaaValue(object):

    @classmethod
    def _validate_value(cls, value):
        reasons = []
        try:
            flags = int(value.get(b'flags', 0))
            if flags < 0 or flags > 255:
                reasons.append((b'invalid flags "{}"').format(flags))
        except ValueError:
            reasons.append((b'invalid flags "{}"').format(value[b'flags']))

        if b'tag' not in value:
            reasons.append(b'missing tag')
        if b'value' not in value:
            reasons.append(b'missing value')
        return reasons

    def __init__(self, value):
        self.flags = int(value.get(b'flags', 0))
        self.tag = value[b'tag']
        self.value = value[b'value']

    @property
    def data(self):
        return {b'flags': self.flags, 
           b'tag': self.tag, 
           b'value': self.value}

    def __cmp__(self, other):
        if self.flags == other.flags:
            if self.tag == other.tag:
                return cmp(self.value, other.value)
            return cmp(self.tag, other.tag)
        return cmp(self.flags, other.flags)

    def __repr__(self):
        return (b'{} {} "{}"').format(self.flags, self.tag, self.value)


class CaaRecord(_ValuesMixin, Record):
    _type = b'CAA'

    @classmethod
    def _validate_value(cls, value):
        return CaaValue._validate_value(value)

    def _process_values(self, values):
        return [ CaaValue(v) for v in values ]


class CnameRecord(_ValueMixin, Record):
    _type = b'CNAME'

    @classmethod
    def validate(cls, name, data):
        reasons = []
        if name == b'':
            reasons.append(b'root CNAME not allowed')
        reasons.extend(super(CnameRecord, cls).validate(name, data))
        return reasons

    @classmethod
    def _validate_value(cls, value):
        reasons = []
        if not value.endswith(b'.'):
            reasons.append(b'missing trailing .')
        return reasons

    def _process_value(self, value):
        return value


class MxValue(object):

    @classmethod
    def _validate_value(cls, value):
        reasons = []
        try:
            try:
                int(value[b'preference'])
            except KeyError:
                int(value[b'priority'])

        except KeyError:
            reasons.append(b'missing preference')
        except ValueError:
            reasons.append((b'invalid preference "{}"').format(value[b'preference']))

        exchange = None
        try:
            exchange = value.get(b'exchange', None) or value[b'value']
            if not exchange.endswith(b'.'):
                reasons.append(b'missing trailing .')
        except KeyError:
            reasons.append(b'missing exchange')

        return reasons

    def __init__(self, value):
        try:
            preference = value[b'preference']
        except KeyError:
            preference = value[b'priority']

        self.preference = int(preference)
        try:
            exchange = value[b'exchange']
        except KeyError:
            exchange = value[b'value']

        self.exchange = exchange

    @property
    def data(self):
        return {b'preference': self.preference, 
           b'exchange': self.exchange}

    def __cmp__(self, other):
        if self.preference == other.preference:
            return cmp(self.exchange, other.exchange)
        return cmp(self.preference, other.preference)

    def __repr__(self):
        return (b"'{} {}'").format(self.preference, self.exchange)


class MxRecord(_ValuesMixin, Record):
    _type = b'MX'

    @classmethod
    def _validate_value(cls, value):
        return MxValue._validate_value(value)

    def _process_values(self, values):
        return [ MxValue(v) for v in values ]


class NaptrValue(object):
    VALID_FLAGS = ('S', 'A', 'U', 'P')

    @classmethod
    def _validate_value(cls, data):
        reasons = []
        try:
            int(data[b'order'])
        except KeyError:
            reasons.append(b'missing order')
        except ValueError:
            reasons.append((b'invalid order "{}"').format(data[b'order']))

        try:
            int(data[b'preference'])
        except KeyError:
            reasons.append(b'missing preference')
        except ValueError:
            reasons.append((b'invalid preference "{}"').format(data[b'preference']))

        try:
            flags = data[b'flags']
            if flags not in cls.VALID_FLAGS:
                reasons.append((b'unrecognized flags "{}"').format(flags))
        except KeyError:
            reasons.append(b'missing flags')

        for k in ('service', 'regexp', 'replacement'):
            if k not in data:
                reasons.append((b'missing {}').format(k))

        return reasons

    def __init__(self, value):
        self.order = int(value[b'order'])
        self.preference = int(value[b'preference'])
        self.flags = value[b'flags']
        self.service = value[b'service']
        self.regexp = value[b'regexp']
        self.replacement = value[b'replacement']

    @property
    def data(self):
        return {b'order': self.order, 
           b'preference': self.preference, 
           b'flags': self.flags, 
           b'service': self.service, 
           b'regexp': self.regexp, 
           b'replacement': self.replacement}

    def __cmp__(self, other):
        if self.order != other.order:
            return cmp(self.order, other.order)
        if self.preference != other.preference:
            return cmp(self.preference, other.preference)
        if self.flags != other.flags:
            return cmp(self.flags, other.flags)
        if self.service != other.service:
            return cmp(self.service, other.service)
        if self.regexp != other.regexp:
            return cmp(self.regexp, other.regexp)
        return cmp(self.replacement, other.replacement)

    def __repr__(self):
        flags = self.flags if self.flags is not None else b''
        service = self.service if self.service is not None else b''
        regexp = self.regexp if self.regexp is not None else b''
        return (b'\'{} {} "{}" "{}" "{}" {}\'').format(self.order, self.preference, flags, service, regexp, self.replacement)


class NaptrRecord(_ValuesMixin, Record):
    _type = b'NAPTR'

    @classmethod
    def _validate_value(cls, value):
        return NaptrValue._validate_value(value)

    def _process_values(self, values):
        return [ NaptrValue(v) for v in values ]


class NsRecord(_ValuesMixin, Record):
    _type = b'NS'

    @classmethod
    def _validate_value(cls, value):
        reasons = []
        if not value.endswith(b'.'):
            reasons.append(b'missing trailing .')
        return reasons

    def _process_values(self, values):
        return values


class PtrRecord(_ValueMixin, Record):
    _type = b'PTR'

    @classmethod
    def _validate_value(cls, value):
        reasons = []
        if not value.endswith(b'.'):
            reasons.append(b'missing trailing .')
        return reasons

    def _process_value(self, value):
        return value


class SshfpValue(object):
    VALID_ALGORITHMS = (1, 2, 3, 4)
    VALID_FINGERPRINT_TYPES = (1, 2)

    @classmethod
    def _validate_value(cls, value):
        reasons = []
        try:
            algorithm = int(value[b'algorithm'])
            if algorithm not in cls.VALID_ALGORITHMS:
                reasons.append((b'unrecognized algorithm "{}"').format(algorithm))
        except KeyError:
            reasons.append(b'missing algorithm')
        except ValueError:
            reasons.append((b'invalid algorithm "{}"').format(value[b'algorithm']))

        try:
            fingerprint_type = int(value[b'fingerprint_type'])
            if fingerprint_type not in cls.VALID_FINGERPRINT_TYPES:
                reasons.append((b'unrecognized fingerprint_type "{}"').format(fingerprint_type))
        except KeyError:
            reasons.append(b'missing fingerprint_type')
        except ValueError:
            reasons.append((b'invalid fingerprint_type "{}"').format(value[b'fingerprint_type']))

        if b'fingerprint' not in value:
            reasons.append(b'missing fingerprint')
        return reasons

    def __init__(self, value):
        self.algorithm = int(value[b'algorithm'])
        self.fingerprint_type = int(value[b'fingerprint_type'])
        self.fingerprint = value[b'fingerprint']

    @property
    def data(self):
        return {b'algorithm': self.algorithm, 
           b'fingerprint_type': self.fingerprint_type, 
           b'fingerprint': self.fingerprint}

    def __cmp__(self, other):
        if self.algorithm != other.algorithm:
            return cmp(self.algorithm, other.algorithm)
        if self.fingerprint_type != other.fingerprint_type:
            return cmp(self.fingerprint_type, other.fingerprint_type)
        return cmp(self.fingerprint, other.fingerprint)

    def __repr__(self):
        return (b"'{} {} {}'").format(self.algorithm, self.fingerprint_type, self.fingerprint)


class SshfpRecord(_ValuesMixin, Record):
    _type = b'SSHFP'

    @classmethod
    def _validate_value(cls, value):
        return SshfpValue._validate_value(value)

    def _process_values(self, values):
        return [ SshfpValue(v) for v in values ]


_unescaped_semicolon_re = re.compile(b'\\w;')

class _ChunkedValuesMixin(_ValuesMixin):
    CHUNK_SIZE = 255

    @classmethod
    def _validate_value(cls, value):
        if _unescaped_semicolon_re.search(value):
            return [b'unescaped ;']
        return []

    def _process_values(self, values):
        ret = []
        for v in values:
            if v and v[0] == b'"':
                v = v[1:-1]
            ret.append(v.replace(b'" "', b''))

        return ret

    @property
    def chunked_values(self):
        values = []
        for v in self.values:
            v = v.replace(b'"', b'\\"')
            vs = [ v[i:i + self.CHUNK_SIZE] for i in range(0, len(v), self.CHUNK_SIZE)
                 ]
            vs = (b'" "').join(vs)
            values.append((b'"{}"').format(vs))

        return values


class SpfRecord(_ChunkedValuesMixin, Record):
    _type = b'SPF'


class SrvValue(object):

    @classmethod
    def _validate_value(self, value):
        reasons = []
        try:
            int(value[b'priority'])
        except KeyError:
            reasons.append(b'missing priority')
        except ValueError:
            reasons.append((b'invalid priority "{}"').format(value[b'priority']))

        try:
            int(value[b'weight'])
        except KeyError:
            reasons.append(b'missing weight')
        except ValueError:
            reasons.append((b'invalid weight "{}"').format(value[b'weight']))

        try:
            int(value[b'port'])
        except KeyError:
            reasons.append(b'missing port')
        except ValueError:
            reasons.append((b'invalid port "{}"').format(value[b'port']))

        try:
            if not value[b'target'].endswith(b'.'):
                reasons.append(b'missing trailing .')
        except KeyError:
            reasons.append(b'missing target')

        return reasons

    def __init__(self, value):
        self.priority = int(value[b'priority'])
        self.weight = int(value[b'weight'])
        self.port = int(value[b'port'])
        self.target = value[b'target'].lower()

    @property
    def data(self):
        return {b'priority': self.priority, 
           b'weight': self.weight, 
           b'port': self.port, 
           b'target': self.target}

    def __cmp__(self, other):
        if self.priority != other.priority:
            return cmp(self.priority, other.priority)
        if self.weight != other.weight:
            return cmp(self.weight, other.weight)
        if self.port != other.port:
            return cmp(self.port, other.port)
        return cmp(self.target, other.target)

    def __repr__(self):
        return (b"'{} {} {} {}'").format(self.priority, self.weight, self.port, self.target)


class SrvRecord(_ValuesMixin, Record):
    _type = b'SRV'
    _name_re = re.compile(b'^_[^\\.]+\\.[^\\.]+')

    @classmethod
    def validate(cls, name, data):
        reasons = []
        if not cls._name_re.match(name):
            reasons.append(b'invalid name')
        reasons.extend(super(SrvRecord, cls).validate(name, data))
        return reasons

    @classmethod
    def _validate_value(cls, value):
        return SrvValue._validate_value(value)

    def _process_values(self, values):
        return [ SrvValue(v) for v in values ]


class TxtRecord(_ChunkedValuesMixin, Record):
    _type = b'TXT'