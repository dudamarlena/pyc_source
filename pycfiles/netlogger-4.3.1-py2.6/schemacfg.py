# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/schemacfg.py
# Compiled at: 2010-10-18 10:11:18
"""
Read and handle simple event "schemas" encoded
in a Python configuration file.

Format::

  [<event-name>]
  <field> = <type-name> [{default-value}]
  ..

The <type-name> is the target type for the field value.
Accepted values for <type-name> are:
  int(eger) - int/long-int number
  float - FP number
  date - datetime object
  str - doesn't do anything, but good for documentation and also
        used in 'drop not mentioned' mode.
        
The "default-value" is optional.

Sample schema::

  [enter.stage.left]
  ts = date
  name = str
  height = float
  weight = float
  age = int
  gender = str {female}

# event:
# ts=1602-02-23T12:22:34 event=enter.stage.left name=Hamlet height=70 # weight=160 age=20 gender=male

Sample usage::

  from <thismodule> import SchemaParser, Schema
  parser = SchemaParser(files=("myschemafile.cfg",))
  schema = parser.get_schema()
  for e in event_list:
      print "before: %s" % e
      schema.event(e)
      print "after: %s" % e

"""
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
__rcsid__ = '$Id: schemacfg.py 26624 2010-10-18 14:05:03Z dang $'
from datetime import datetime
import ConfigParser, re
from netlogger import nldate
from netlogger import nlapi
from netlogger import nllog
from netlogger import util
from netlogger.parsers.base import parseDate

def convert_to_date(x):
    """Convert value to date.

    Exceptions:
      - ValueError: if string date is invalid.
    """
    result = x
    if isinstance(x, float):
        result = datetime.utcfromtimestamp(x)
    elif isinstance(x, str):
        sec = parseDate(x)
        result = datetime.utcfromtimestamp(sec)
    return result


def drop(x):
    return


def identity(x):
    return x


class SchemaParser(nllog.DoesLogging):
    _TYPEFN = {'int': int, 
       'integer': int, 
       'float': float, 
       'date': convert_to_date, 
       'str': str, 
       'string': str, 
       '@drop': drop}
    _SCHEMAVAL = re.compile('      \n    (?P<type>\\w+)                    # Type of the named item     \n    (?:\\s+(?P<default>\\{.*\\}))?\\s*   # Optional default value, only WS after\n    ', flags=re.VERBOSE)

    def __init__(self, files=[], **read_kw):
        """Constructor.

        Args:
          - files (str[]): File objects or names
              passed to read(), if present.
              
        Kwargs:
          - **read_kw: Keywords passed through to read() function

        Exceptions:
          If `files` is non-empty, then will raise exceptions
          just like read().
          
        """
        nllog.DoesLogging.__init__(self)
        self._parser = ConfigParser.RawConfigParser()
        self._mapping, self._defaults, self._drop = {}, {}, {}
        for f in files:
            self.read(f, **read_kw)

    def read(self, str_or_file):
        """Read and parse the data.

        Args:
          - str_or_file (str|file): A string or file-like
              object, which must implement readline(). If it is a
              string attempt to open the file with that name.

        Exceptions:
          - IOError: If a file is specified but can't be opened
          - ValueError: Bad type specification
        """
        if hasattr(str_or_file, 'readline'):
            fileobj = str_or_file
        else:
            fileobj = open(str(str_or_file), 'r')
        self._parser.readfp(fileobj)
        name_expr = re.compile('^[0-9a-zA-Z._-]+$')
        msg = 'must be 1 or more of alphanumeric, dash, underline or dot'
        for sect in self._parser.sections():
            m = name_expr.match(sect)
            if m is None:
                raise ValueError('Event name [%s]: %s' % (sect, msg))
            type_map, defaults = {}, {}
            try:
                drop_opt = self._parser.get(sect, '@drop')
                drop = util.as_bool(drop_opt)
            except ConfigParser.NoOptionError:
                drop = False

            for (name, value) in self._parser.items(sect):
                if name[0] == '@':
                    continue
                m = name_expr.match(name)
                if m is None:
                    raise ValueError("Field name '%s': %s" % (name, msg))
                m = self._SCHEMAVAL.match(value)
                if m is None:
                    raise ValueError("Bad value '%s' for field '%s'" % (
                     value, name))
                mgd = m.groupdict()
                value_type, value_default = mgd['type'], mgd['default']
                try:
                    fn = self._TYPEFN[value_type]
                    if not drop and fn is str:
                        pass
                    else:
                        type_map[name] = fn
                except KeyError:
                    raise ValueError("Unknown type '%s' in '%s=%s' in section [%s]" % (
                     value_type, name, value, sect))

                if value_default is not None:
                    s = value_default[1:-1]
                    defaults[name] = s

            self._mapping[sect] = type_map
            self._defaults[sect] = defaults
            self._drop[sect] = drop

        return

    def get_schema(self):
        """Get the schema so far.

        Returns:
          - Schema: The schema as an object.
        """
        return Schema(self._mapping, self._defaults, drop_unknown=self._drop)


class Schema(nllog.DoesLogging):
    """Thin wrapper around a mapping that specifies functions
    for converting field values for a given event type.

    Attributes:
       - mapping: the original mapping
    """

    def __init__(self, mapping, defaults, drop_unknown={}):
        """Constructor.

        Args:
          - mapping (dict): Type mapping. Layout of dictionary is
             { event-name : { field-name : function, .. }, .. }             
          - defaults (dict): Default values. Layout of dictionary is
             { event-name : { field-name : value, .. }, .. }
          - drop_unknown (dict): When processing events, if this is True
             then drop all event attributes not named in the schema.
             Key is event-name, value is boolean.
        """
        nllog.DoesLogging.__init__(self)
        self.mapping = mapping
        self.defaults = defaults
        self.drop_unknown = drop_unknown

    def event(self, event):
        """Modify input event dictionary, in place,
        parsing types as specified by the schema.

        Args:
          - event (dict): NetLogger event dictionary

        Exceptions:
          - ValueError: If the event doesn't have required fields,
              or there is an error parsing one of the values.
        """
        try:
            event_name = event[nlapi.EVENT_FIELD]
        except KeyError:
            raise ValueError("Bad event, missing required field '%s'" % nlapi.EVENT_FIELD)

        if self.mapping.has_key(event_name):
            type_map = self.mapping[event_name]
            for key in type_map:
                value = None
                if key not in event:
                    if key in self.defaults[event_name]:
                        value = self.defaults[event_name][key]
                else:
                    value = event[key]
                if value is not None:
                    if self._trace:
                        self.log.trace('convert.start', key=key)
                    fn = type_map[key]
                    if fn is not None:
                        try:
                            result = fn(value)
                        except ValueError, err:
                            if self._trace:
                                self.log.trace('convert.end', key=key, status=-1, msg=err)
                            raise ValueError("parsing '%s': %s" % (key, err))

                    if result is not None:
                        event[key] = result
                    if self._trace:
                        self.log.trace('convert.end', key=key, status=0)

            if self.drop_unknown.get(event_name, False):
                for ekey in event.keys():
                    if ekey != 'event' and ekey != 'ts' and ekey not in type_map:
                        del event[ekey]

        return