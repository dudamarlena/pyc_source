# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/halicea/gaeHelpers.py
# Compiled at: 2012-01-02 15:08:01
import datetime, time
from google.appengine.ext import db
SIMPLE_TYPES = (
 int, long, float, bool, dict, basestring, list)

class ModelToDict(object):
    """Callable to convert an appengine Model to a Dictionary that can be 
       then easy represented with Json or Xml
    """

    def __call__(self, model):
        output = {}
        for key, prop in model.properties().iteritems():
            value = getattr(model, key)
            if value is None or isinstance(value, SIMPLE_TYPES):
                output[key] = value
            elif isinstance(value, datetime.date):
                ms = time.mktime(value.utctimetuple()) * 1000
                ms += getattr(value, 'microseconds', 0) / 1000
                output[key] = int(ms)
            elif isinstance(value, db.GeoPt):
                output[key] = {'lat': value.lat, 'lon': value.lon}
            elif isinstance(value, db.Model):
                output[key] = ModelToDict(value)
            else:
                raise ValueError('cannot encode ' + repr(prop))

        return output