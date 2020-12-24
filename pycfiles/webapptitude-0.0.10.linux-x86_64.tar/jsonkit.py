# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/webapptitude/jsonkit.py
# Compiled at: 2016-08-31 16:32:16
from webapp2_extras import json as webapp2_json
from google.appengine.ext import ndb
import datetime, time, re

class JSONDateTime(datetime.datetime):
    RE_BASE_DATE = '(?P<date>\\d{4}-\\d{2}-\\d{2})'
    RE_BASE_TIME = '(?P<time>\\d{2}:\\d{2}:\\d{2})(?P<micro>\\.\\d{1,6})?Z?'
    RE_EPOCH = re.compile('^/Date\\((?P<epoch>\\d+)(?P<micro>\\.\\d+)?\\)/$')
    RE_DATETIME = re.compile('^/Date\\(%s[ T]%s\\)/$' % (RE_BASE_DATE, RE_BASE_TIME))
    RE_DATEONLY = re.compile('^/Date\\(%s\\)/$' % RE_BASE_DATE)
    RE_TIMEONLY = re.compile('^/Time\\(%s\\)/$' % RE_BASE_TIME)

    @classmethod
    def extractJSONParts(cls, text):
        for r in (cls.RE_DATEONLY, cls.RE_TIMEONLY, cls.RE_DATETIME, cls.RE_EPOCH):
            match = r.match(text)
            if match is not None:
                return match

        return

    @classmethod
    def parsePatternMatch(cls, match):
        parts = match.groupdict()
        _micro = parts.get('micro', '.0') or '.0'
        if 'epoch' in parts:
            basetime = float(parts.get('epoch'), parts.get('micro', ''))
            basetime = cls.utcfromtimestamp(basetime)
            return basetime
        else:
            if 'date' not in parts and 'time' in parts:
                basetime = parts.get('time') + _micro + 'Z'
                return cls.strptime(basetime, '%H:%M:%S.%fZ').time()
            else:
                if 'time' not in parts and 'date' in parts:
                    return cls.strptime(parts.get('date'), '%Y-%m-%d').date()
                if 'date' in parts and 'time' in parts:
                    basetime = '%s %s%sZ' % (parts.get('date'), parts.get('time'), _micro)
                    return cls.strptime(basetime, '%Y-%m-%d %H:%M:%S.%fZ')
                return

            return

    @classmethod
    def parseJSONDate(cls, text):
        match = cls.extractJSONParts(text)
        if match is None:
            return match
        else:
            return cls.parsePatternMatch(match)
            return

    @classmethod
    def buildJSONDate(cls, basedate):
        if isinstance(basedate, (int, float)):
            basedate = cls.utcfromtimestamp(basedate)
        if isinstance(basedate, time.struct_time):
            basedate = cls.utcfromtimestamp(time.mktime(basedate))
        if isinstance(basedate, datetime.date):
            return '/Date(%s)/' % basedate.isoformat()
        if isinstance(basedate, datetime.time):
            return '/Time(%s)/' % basedate.isoformat()
        if isinstance(basedate, datetime.datetime):
            return '/Date(%s)/' % basedate.isoformat('T')
        raise TypeError('buildJSONDate requires a {datetime.datetime, datetime.time, datetime.date, struct_time, int, float}')


class JSONEncoder(webapp2_json.json.JSONEncoder):

    def default(self, o):
        if isinstance(o, unicode):
            return str(o)
        if isinstance(o, (time.struct_time, datetime.time, datetime.date, datetime.datetime)):
            return JSONDateTime.buildJSONDate(o)
        if isinstance(o, ndb.Key):
            return 'key#' + o.urlsafe()
        if isinstance(o, ndb.Model):
            return dict([ (i, self.default(v)) for i, v in o.to_dict().items() ])
        return super(JSONEncoder, self).default(o)


class JSONDecoder(webapp2_json.json.JSONDecoder):
    encodings = [
     (
      JSONDateTime.RE_TIMEONLY, JSONDateTime.parsePatternMatch),
     (
      JSONDateTime.RE_DATEONLY, JSONDateTime.parsePatternMatch),
     (
      JSONDateTime.RE_DATETIME, JSONDateTime.parsePatternMatch),
     (
      JSONDateTime.RE_EPOCH, JSONDateTime.parsePatternMatch),
     (
      re.compile('^key#(.*)$'), lambda m: ndb.Key(urlsafe=m.group(1)))]

    def __init__(self, *args, **kwargs):
        kwargs['object_hook'] = lambda a: self.convertEncodedStringTypes(a)
        super(JSONDecoder, self).__init__(*args, **kwargs)

    def convertEncodedStringTypes(self, obj):
        if isinstance(obj, basestring):
            for pattern, handler in self.encodings:
                match = pattern.match(obj)
                if match is not None:
                    return handler(match)

        if isinstance(obj, list):
            return [ self.convertEncodedStringTypes(i) for i in obj ]
        else:
            if isinstance(obj, dict):
                for k in obj.keys():
                    obj[k] = self.convertEncodedStringTypes(obj[k])

            return obj


def json_encode(data, charset='UTF-8'):
    content = webapp2_json.encode(data, separators=(',', ':'), cls=JSONEncoder)
    return content.encode(charset)


def json_decode(text):
    return webapp2_json.decode(text, cls=JSONDecoder)