# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/cromulent/model.py
# Compiled at: 2019-11-22 16:06:13
from __future__ import unicode_literals
import os, sys, re, codecs, inspect, uuid, datetime
KEY_ORDER_DEFAULT = 10000
LINKED_ART_CONTEXT_URI = b'https://linked.art/ns/v1/linked-art.json'
import json
from collections import OrderedDict, namedtuple
try:
    STR_TYPES = [
     str, unicode]
    FILE_STREAM_CLASS = file
except:
    import io
    STR_TYPES = [
     bytes, str]
    FILE_STREAM_CLASS = io.TextIOBase

PropInfo = namedtuple(b'PropInfo', [
 b'property',
 b'predicate',
 b'range',
 b'inverse_property',
 b'inverse_predicate',
 b'multiple_okay',
 b'profile_okay'])

class CromulentError(Exception):
    """Base exception class"""
    resource = None

    def __init__(self, msg, resource=None):
        """Initialize CidocError."""
        self.args = [
         msg]
        self.resource = resource


class ConfigurationError(CromulentError):
    """Raised when an object (likely the factory) isn't configured properly for the current operation."""
    pass


class MetadataError(CromulentError):
    """Base metadata exception."""
    pass


class RequirementError(MetadataError):
    """Raised when schema/profile/metadata requirements not met."""
    pass


class DataError(MetadataError):
    """Raised when data is not valid/allowed."""
    pass


class ProfileError(MetadataError):
    """Raised when a class or property not in the configured profile is used"""
    pass


class CromulentFactory(object):

    def __init__(self, base_url=b'', base_dir=b'', lang=b'', full_names=False, context=b'', context_file={}, load_context=True):
        self.base_url = base_url
        self.base_dir = base_dir
        self.debug_level = b'warn'
        self.log_stream = sys.stderr
        self.materialize_inverses = False
        self.full_names = False
        self.pipe_scoped_contexts = False
        self.validate_properties = True
        self.validate_profile = True
        self.validate_range = True
        self.validate_multiplicity = True
        self.auto_assign_id = True
        self.process_multiplicity = True
        self.multiple_instances_per_property = b'drop'
        self.auto_id_type = b'int-per-segment'
        self.filename_extension = b'.json'
        self.context_uri = context
        self.context_json = {}
        self.prefixes = {}
        self.prefixes_rev = {}
        self.context_rev = {}
        if load_context:
            context_filemap = {LINKED_ART_CONTEXT_URI: os.path.join(os.path.dirname(__file__), b'data', b'linked-art.json')}
            context_filemap.update(context_file)
            self.load_context(context, context_filemap)
        self.elasticsearch_compatible = False
        self.linked_art_boundaries = False
        self.id_type_label = True
        self.json_indent = 2
        self.order_json = True
        self.key_order_hash = {b'@context': 0, b'id': 1, b'type': 2, b'_label': 5, 
           b'value': 6}
        self.full_key_order_hash = {b'@context': 0, b'@id': 1, b'rdf:type': 2, b'@type': 2, b'rdfs:label': 5, 
           b'rdf:value': 6}
        self.key_order_default = 10000
        self.underscore_properties = [
         b'_label']
        self._auto_id_types = {}
        self._auto_id_segments = {}
        self._auto_id_int = -1
        self._all_classes = {}

    def load_context(self, context, context_filemap):
        if not context or not context_filemap:
            raise ConfigurationError(b'No context provided, and load_context not False')
        if type(context) is not list:
            context = [
             context]
        js = {b'@context': {}}
        for ct in context:
            fn = context_filemap.get(ct, b'')
            if fn:
                try:
                    fh = open(fn)
                    data = fh.read()
                    fh.close()
                except IOError:
                    raise ConfigurationError(b'Provided context file does not exist')

            else:
                data = b'{}'
            try:
                ctx = json.loads(data)
                js[b'@context'].update(ctx[b'@context'])
            except:
                raise ConfigurationError(b'Provided context does not have valid JSON')

        self.context_json = js
        self.process_context()

    def process_context(self):
        for k, v in self.context_json[b'@context'].items():
            if type(v) in STR_TYPES and v[(-1)] in ('/', '#'):
                self.prefixes[k] = v
                self.prefixes_rev[v] = k
            elif k == b'@version':
                continue
            else:
                if type(v) in STR_TYPES:
                    rdf = v
                else:
                    rdf = v[b'@id']
                self.context_rev[rdf] = k

    def __getstate__(self):
        d = self.__dict__.copy()
        try:
            self.log_stream.flush()
        except:
            pass

        strm = d[b'log_stream']
        if strm is sys.stdout:
            d[b'log_stream'] = ('sys.stdout', 'stream')
        elif strm is sys.stderr:
            d[b'log_stream'] = ('sys.stderr', 'stream')
        elif isinstance(strm, FILE_STREAM_CLASS):
            d[b'log_stream'] = (
             strm.name, b'file')
        else:
            d[b'log_stream'] = None
        return d

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.log_stream:
            if self.log_stream[1] == b'stream':
                if self.log_stream[0] == b'sys.stdout':
                    self.log_stream = sys.stdout
                elif self.log_stream[0] == b'sys.stderr':
                    self.log_stream = sys.stderr
            elif self.log_stream[1] == b'file':
                try:
                    self.log_stream = open(self.log_stream[0], b'a')
                except:
                    self.log_stream = None

        return

    def set_debug_stream(self, strm):
        """Set debug level."""
        self.log_stream = strm

    def set_debug(self, typ):
        """Set behavior on errors and warnings.

                error = squash warnings
                warn = display warnings
                error_on_warning = raise exception for a warning rather than continuing
                """
        if typ in ('error', 'warn', 'error_on_warning'):
            self.debug_level = typ
        else:
            raise ConfigurationError(b"Only levels are 'error', 'warn' and 'error_on_warning'")

    def maybe_warn(self, msg):
        """warn method that respects debug_level property."""
        if self.debug_level == b'warn':
            self.log_stream.write(msg + b'\n')
            try:
                self.log_stream.flush()
            except:
                pass

        elif self.debug_level == b'error_on_warning':
            raise MetadataError(msg)

    def generate_id(self, what):
        if self.auto_id_type == b'int':
            self._auto_id_int += 1
            slug = self._auto_id_int
        elif self.auto_id_type == b'int-per-segment':
            curr = self._auto_id_segments.get(what._uri_segment, -1)
            curr += 1
            self._auto_id_segments[what._uri_segment] = curr
            slug = self._auto_id_segments[what._uri_segment]
        elif self.auto_id_type == b'int-per-type':
            t = type(what).__name__
            curr = self._auto_id_types.get(t, -1)
            curr += 1
            self._auto_id_types[t] = curr
            slug = self._auto_id_types[t]
        else:
            if self.auto_id_type == b'uuid':
                return b'urn:uuid:%s' % uuid.uuid4()
            raise ConfigurationError(b'Unknown auto-id type')
        return self.base_url + what.__class__._uri_segment + b'/' + str(slug)

    def toJSON(self, what, done=None):
        """ Serialize what, making sure of no infinite loops """
        if not done:
            done = {}
        out = what._toJSON(top=what, done=done)
        return out

    def _collapse_json(self, text, collapse):
        js_indent = self.json_indent
        lines = text.splitlines()
        out = [lines[0]]
        while lines:
            l = lines.pop(0)
            indent = len(re.split(b'\\S', l, 1)[0])
            if indent and l.rstrip()[(-1)] in ('[', '{'):
                curr = indent
                temp = []
                stemp = []
                while lines and curr <= indent:
                    if temp and curr == indent:
                        break
                    temp.append(l[curr:])
                    stemp.append(l.strip())
                    l = lines.pop(0)
                    indent = len(re.split(b'\\S', l, 1)[0])

                temp.append(l[curr:])
                stemp.append(l.lstrip())
                short = b' ' * curr + (b'').join(stemp)
                if len(short) < collapse:
                    out.append(short)
                else:
                    ntext = (b'\n').join(temp)
                    nout = self._collapse_json(ntext, collapse)
                    for no in nout:
                        out.append(b' ' * curr + no)

            elif indent:
                out.append(l)

        out.append(l)
        return out

    def collapse_json(self, text, collapse):
        return (b'\n').join(self._collapse_json(text, collapse))

    def _buildString(self, js, compact=True, collapse=0):
        """Build string from JSON."""
        try:
            if compact:
                out = json.dumps(js, separators=(',', ':'), ensure_ascii=False)
            else:
                out = json.dumps(js, indent=self.json_indent, ensure_ascii=False)
        except:
            out = b''
            self.maybe_warn(b"Can't decode %r" % js)
            raise

        if collapse:
            out = self.collapse_json(out, collapse)
        return out

    def toString(self, what, compact=True, collapse=0, done=None):
        """Return JSON setialization as string."""
        if not done:
            done = {}
        js = self.toJSON(what, done=done)
        return self._buildString(js, compact, collapse)

    def toFile(self, what, compact=True, filename=b'', done=None):
        """Write to local file.

                Creates directories as necessary
                """
        if not done:
            done = {}
        js = self.toJSON(what, done=done)
        if not filename:
            myid = js[b'id']
            mdb = self.base_url
            if not myid.startswith(mdb):
                raise ConfigurationError(b'The id of that object is not the base URI in the Factory')
            mdd = self.base_dir
            if not mdd:
                raise ConfigurationError(b'Directory on Factory must be set to write to file')
            fp = myid[len(mdb):]
            bits = fp.split(b'/')
            if len(bits) > 1:
                mydir = os.path.join(mdd, (b'/').join(bits[:-1]))
                try:
                    os.makedirs(mydir)
                except OSError:
                    pass

            if self.filename_extension:
                fp = fp + self.filename_extension
            filename = os.path.join(mdd, fp)
        fh = open(filename, b'w')
        out = self._buildString(js, compact)
        fh.write(out)
        fh.close()
        return out

    def production_mode(self):
        self.cache_hierarchy()
        self.validate_profile = False
        self.validate_properties = False
        self.validate_range = False
        self.validate_multiplicity = False
        return True

    def cache_hierarchy(self):
        """ For each class, walk up the hierarchy and cache the terms """
        for c in self._all_classes.values():
            new_hash = c._all_properties.copy()
            if len(c._classhier) > 1:
                for p in c._classhier[1:]:
                    for prop, info in p._all_properties.items():
                        if prop not in new_hash:
                            new_hash[prop] = info

            c._all_properties = new_hash


class ExternalResource(object):
    """Base class for all resources, including external references"""
    _factory = None
    _uri_segment = b''
    id = b''
    _full_id = b''
    _all_properties = {}
    _type = b''
    _embed = True

    def _is_uri(self, what):
        uri_schemes = [
         b'urn:uuid:', b'tag:', b'data:', b'mailto:', b'info:', b'ftp:/', b'sftp:/']
        for u in uri_schemes:
            if what.startswith(u):
                return True

        return False

    def __init__(self, ident=None):
        self._factory = factory
        if ident is not None:
            if self._is_uri(ident):
                self.id = ident
            elif ident.startswith(b'http'):
                hashed = ident.rsplit(b'#', 1)
                if len(hashed) == 1:
                    pref, rest = ident.rsplit(b'/', 1)
                    pref += b'/'
                else:
                    pref, rest = hashed
                    pref += b'#'
                if pref in self._factory.prefixes_rev:
                    self._full_id = ident
                    ident = b'%s:%s' % (self._factory.prefixes_rev[pref], rest)
                self.id = ident
            elif ident == b'':
                self.id = b''
            else:
                curied = ident.split(b':', 1)
                if len(curied) == 2 and curied[0] in self._factory.prefixes:
                    self.id = ident
                    self._full_id = self._factory.prefixes[curied[0]] + curied[1]
                else:
                    self.id = factory.base_url + self.__class__._uri_segment + b'/' + ident
        elif factory.auto_assign_id:
            self.id = factory.generate_id(self)
        else:
            self.id = b''
        return

    def _toJSON(self, done, top=None):
        if self._factory.elasticsearch_compatible:
            return {b'id': self.id}
        else:
            return self.id


class BaseResource(ExternalResource):
    """Base class for all resources with classes"""
    _integer_properties = []
    _object_properties = []
    _required_properties = []
    _warn_properties = []
    _classification = b''
    _classhier = []

    def __init__(self, ident=None, label=b'', value=b'', content=b'', **kw):
        """Initialize BaseObject."""
        super(BaseResource, self).__init__(ident)
        if content and not value:
            value = content
        if self._factory.validate_profile and hasattr(self, b'_okayToUse'):
            if not self._okayToUse:
                raise ProfileError(b"Class '%s' is configured to not be used" % self.__class__._type)
            elif self._okayToUse == 2:
                self._factory.maybe_warn(b"Class '%s' is configured to warn on use" % self.__class__._type)
        if label:
            self._label = label
        if value:
            try:
                self.value = value
            except:
                try:
                    self.content = value
                except:
                    raise ProfileError(b"Class '%s' does not hold values" % self.__class__._type)

        self._post_init(**kw)

    def __dir__(self):
        d = dir(self.__class__)
        d.extend(self.list_all_props())
        return sorted(d)

    def __eq__(a, b):
        if id(a) == id(b):
            return True
        ap = a.list_my_props()
        bp = b.list_my_props()
        if ap != bp:
            return False
        for p in ap:
            av = getattr(a, p)
            bv = getattr(b, p)
            if av != bv:
                return False

        return True

    @property
    def type(self):
        for c in self._classhier:
            if c._type:
                return c.__name__

    @type.setter
    def type(self, value):
        raise AttributeError(b"Must not set 'type' on resources directly")

    def set_context(self, value):
        raise DataError(b'Must not set the JSON LD context directly', self)

    def _post_init(self, **kw):
        pass

    def __setattr__(self, which, value):
        """Attribute setting magic for error checking and resource/literal handling."""
        if which[0] == b'_' or not value:
            object.__setattr__(self, which, value)
        else:
            if hasattr(self, b'set_%s' % which):
                fn = getattr(self, b'set_%s' % which)
                return fn(value)
            if self._factory.validate_properties or self._factory.validate_profile or self._factory.validate_range:
                ok = self._check_prop(which, value)
            elif isinstance(value, ExternalResource):
                ok = 2
            else:
                ok = 1
            if ok == 2:
                self._set_magic_resource(which, value)
            else:
                object.__setattr__(self, which, value)

    def _check_prop(self, which, value):
        val_props = self._factory.validate_properties
        val_profile = self._factory.validate_profile
        val_range = self._factory.validate_range
        for c in self._classhier:
            if which in c._all_properties:
                pinfo = c._all_properties[which]
                if val_profile:
                    okay = pinfo.profile_okay
                    rdf = pinfo.predicate
                    if not okay:
                        raise ProfileError(b"Property '%s' / '%s' is configured to not be used" % (which, rdf), self)
                    elif okay == 2:
                        self._factory.maybe_warn(b"Property '%s' / '%s' is configured to warn on use" % (which, rdf))
                if val_range:
                    rng = pinfo.range
                    if rng is str:
                        return 1
                    if type(value) is BaseResource:
                        return 2
                    if isinstance(value, rng):
                        return 2
                    raise DataError(b"Can't set '%s' on resource of type '%s' to '%r'" % (which, self._type, value), self)
                return 1

        if val_props:
            raise DataError(b"Can't set unknown field '%s' on resource of type '%s'" % (which, self._type), self)
        else:
            return 1

    def _check_reference(self, data):
        """True if data is a resource or reference to a resource"""
        if type(data) in STR_TYPES:
            return data.startswith(b'http')
        else:
            if type(data) is dict:
                return b'id' in data
            if isinstance(data, BaseResource):
                return True
            if type(data) is list:
                for d in data:
                    if type(d) in STR_TYPES and not d.startswith(b'http'):
                        return False
                    if type(d) is dict and b'id' not in d:
                        return False

                return True
            self._factory.maybe_warn(b'expecing a resource, got: %r' % data)
            return True

    def _set_magic_resource(self, which, value, inversed=False):
        """Set resource property.
                allow: string/object/dict, and magically generate list thereof
                """
        if self._factory.materialize_inverses or self._factory.process_multiplicity or self._factory.validate_multiplicity:
            inverse = None
            multiple = 1
            for c in self._classhier:
                if which in c._all_properties:
                    v = c._all_properties[which]
                    multiple = v.multiple_okay
                    if v.inverse_property:
                        inverse = v.inverse_property
                    break

        try:
            current = getattr(self, which)
        except:
            current = None

        if not current:
            object.__setattr__(self, which, value)
        elif type(current) is list:
            if self._factory.multiple_instances_per_property == b'error' and isinstance(value, BaseResource) and value in current:
                raise DataError(b"Cannot add the same resource in the same property more than once:\nchange factory.multiple_instances_per_property to 'drop' or 'allow'")
            current.append(value)
        else:
            if self._factory.validate_multiplicity and not multiple:
                raise ProfileError(b'Cannot append to %s on %s as multiplicity is 1' % (which, self._type))
            nvalue = [
             current, value]
            object.__setattr__(self, which, nvalue)
        if self._factory.materialize_inverses and not inversed and inverse:
            value._set_magic_resource(inverse, self, True)
        if self._factory.process_multiplicity and type(current) is not list and multiple:
            object.__setattr__(self, which, [getattr(self, which)])
        return

    def _toJSON(self, done, top=None):
        """Serialize as JSON."""
        d = self.__dict__.copy()
        del d[b'_factory']
        if top is None:
            top = self
        if not factory.id_type_label and id(self) in done:
            if self._factory.elasticsearch_compatible:
                return {b'id': self.id}
            else:
                return self.id

        if b'context' in d:
            d[b'@context'] = d[b'context']
            del d[b'context']
        for e in self._required_properties:
            if e not in d:
                raise RequirementError(b"Resource type '%s' requires '%s' to be set" % (self._type, e), self)

        debug = self._factory.debug_level
        if debug.find(b'warn') > -1:
            for e in self._warn_properties:
                if e not in d:
                    msg = b"Resource type '%s' should have '%s' set" % (self._type, e)
                    self._factory.maybe_warn(msg)

        if top is self and self._factory.context_uri:
            d[b'@context'] = self._factory.context_uri
        if self._factory.id_type_label and id(self) in done or top is not self and not self._embed:
            nd = {}
            nd[b'id'] = d[b'id']
            if self.type:
                nd[b'type'] = self.type
            try:
                nd[b'_label'] = d[b'_label']
            except:
                pass

            d = nd
        else:
            done[id(self)] = 1
        KOH = self._factory.key_order_hash
        kodflt = self._factory.key_order_default
        kvs = sorted(d.items(), key=lambda x: KOH.get(x[0], kodflt))
        tbd = []
        for k, v in kvs:
            if not v or k[0] == b'_' and k not in self._factory.underscore_properties:
                del d[k]
            elif isinstance(v, ExternalResource):
                if self._factory.linked_art_boundaries and not self._linked_art_boundary_okay(top, k, v):
                    done[id(v)] = 1
                else:
                    tbd.append(id(v))
            elif type(v) is list:
                for ni in v:
                    if isinstance(ni, ExternalResource):
                        if self._factory.linked_art_boundaries and not self._linked_art_boundary_okay(top, k, ni):
                            done[id(ni)] = 1
                        else:
                            tbd.append(id(ni))

            elif isinstance(v, datetime.datetime):
                kvs[k] = v.strftime(b'%Y-%m-%dT%H:%M:%SZ')

        for t in tbd:
            if t not in done:
                done[t] = id(self)

        for k, v in kvs:
            if v and k[0] != b'_' and k not in self._factory.underscore_properties:
                if isinstance(v, ExternalResource):
                    if done[id(v)] == id(self):
                        del done[id(v)]
                    d[k] = v._toJSON(done=done, top=top)
                elif type(v) is list:
                    newl = []
                    uniq = set()
                    for ni in v:
                        if self._factory.multiple_instances_per_property == b'drop':
                            if id(ni) in uniq:
                                continue
                            else:
                                uniq.add(id(ni))
                        if isinstance(ni, ExternalResource):
                            if done[id(ni)] == id(self):
                                del done[id(ni)]
                            newl.append(ni._toJSON(done=done, top=top))
                        else:
                            newl.append(ni)

                    d[k] = newl

        if self._factory.full_names:
            nd = {}
            if top is self:
                nd[b'@context'] = self._factory.context_uri
            for k, v in d.items():
                for c in reversed(self._classhier):
                    if k in c._all_properties:
                        nk = c._all_properties[k].predicate
                        nd[nk] = v
                        break

            if b'rdf:type' in nd:
                nd[b'@type'] = nd[b'rdf:type']
                del nd[b'rdf:type']
            if b'@type' not in nd or not nd[b'@type']:
                for c in reversed(self._classhier):
                    if c._type:
                        nd[b'@type'] = c._type

            d = nd
            KOH = self._factory.full_key_order_hash
        else:
            if self.type:
                d[b'type'] = self.type
            if self._factory.pipe_scoped_contexts:
                if b'part' in d:
                    for c in reversed(self._classhier):
                        if b'part' in c._all_properties:
                            nk = c._all_properties[b'part'].predicate
                            d[b'part|%s' % nk] = d[b'part']
                            del d[b'part']
                            break

                if b'part_of' in d:
                    for c in reversed(self._classhier):
                        if b'part_of' in c._all_properties:
                            nk = c._all_properties[b'part_of'].predicate
                            d[b'part_of|%s' % nk] = d[b'part_of']
                            del d[b'part_of']
                            break

        if self._factory.order_json:
            return OrderedDict(sorted(d.items(), key=lambda x: KOH.get(x[0], 1000)))
        else:
            return d
            return

    def _linked_art_boundary_okay(self, top, prop, value):
        return True

    def list_all_props(self, filter=None, okay=None):
        props = []
        for c in self._classhier:
            for k, v in c._all_properties.items():
                if k not in props and (not okay or okay and v.profile_okay) and (filter is None or isinstance(filter, v.range) or filter is v.range):
                    props.append(k)

        props.sort()
        return props

    def list_my_props(self, filter=None):
        d = self.__dict__.copy()
        props = []
        for k, v in d.items():
            if k[0] != b'_' or k in self._factory.underscore_properties:
                if filter:
                    if isinstance(v, filter):
                        props.append(k)
                    elif isinstance(v, list):
                        for i in v:
                            if isinstance(i, filter):
                                props.append(k)
                                break

                else:
                    props.append(k)

        return props

    def allows_multiple(self, propName):
        """ Does propName allow multiple values on this class """
        for c in self._classhier:
            if propName in c._all_properties:
                v = c._all_properties[propName]
                return bool(v.multiple_okay)

        raise DataError(b"Cannot set '%s' on '%s'" % (propName, self.__class__.__name__))


def override_okay(clss, propName):
    """ set particular property on the class to be okay to use """
    pinfo = clss._all_properties.get(propName, None)
    if pinfo:
        npinfo = PropInfo(pinfo.property, pinfo.predicate, pinfo.range, pinfo.inverse_property, pinfo.inverse_predicate, pinfo.multiple_okay, 1)
        clss._all_properties[propName] = npinfo
    else:
        raise DataError(b'%s does not have a %s property to allow' % (
         clss.__name__, propName))
    return


BaseResource._properties = {b'id': {b'rdf': b'@id', b'range': str, b'okayToUse': 1}, b'type': {b'rdf': b'rdf:type', b'range': str, b'rangeStr': b'rdfs:Class', b'okayToUse': 1}, b'_label': {b'rdf': b'rdfs:label', b'range': str, b'rangeStr': b'xsd:string', b'okayToUse': 1}}
BaseResource._all_properties = {b'id': PropInfo(b'id', b'@id', str, None, None, 0, 1), 
   b'type': PropInfo(b'type', b'rdf:type', str, None, None, 0, 1), 
   b'_label': PropInfo(b'_label', b'rdfs:label', str, None, None, 0, 1)}
BaseResource._classhier = (
 BaseResource, ExternalResource)

def process_tsv(fn):
    fh = codecs.open(fn, b'r', b'utf-8')
    lines = fh.readlines()[1:]
    fh.close()
    vocabData = {b'rdf:Resource': {b'props': [], b'label': b'Resource', b'className': b'Resource', b'subs': [], b'desc': b'', b'class': BaseResource, b'okay': 1}}
    for l in lines:
        l = l[:-1]
        info = l.split(b'\t')
        name = info[0]
        if info[1] == b'class':
            data = {b'subOf': info[5], b'label': info[3], b'className': info[2], b'desc': info[4], b'class': None, b'props': [], b'subs': [], b'okay': info[6]}
            vocabData[name] = data
        else:
            data = {b'name': name, b'subOf': info[5], b'label': info[3], b'propName': info[2], b'desc': info[4], b'range': info[7], b'inverse': info[8], b'okay': info[10], b'multiple': info[11]}
            try:
                what = vocabData[info[6]]
            except:
                what = vocabData[b'rdf:Resource']

            what[b'props'].append(data)
            koh = int(info[9])
            if koh != KEY_ORDER_DEFAULT:
                factory.full_key_order_hash[data[b'propName']] = koh
                factory.key_order_hash[data[b'name']] = koh

    for k, v in vocabData.items():
        if k != b'rdf:Resource':
            sub = v[b'subOf']
            for s in sub.split(b'|'):
                if s:
                    try:
                        vocabData[s][b'subs'].append(k)
                    except:
                        pass

    return vocabData


def build_class(crmName, parent, vocabData):
    data = vocabData[crmName]
    name = str(data[b'className'])
    if name in globals():
        c = globals()[name]
        try:
            c.__bases__ += (parent,)
        except:
            print b'MRO FAILURE: %r --> %r + %r' % (c, c.__bases__, parent)
            raise

        return
    c = type(name, (parent,), {b'__doc__': data[b'desc']})
    globals()[name] = c
    data[b'class'] = c
    c._type = b'crm:%s' % crmName
    c._uri_segment = name
    c._properties = {}
    c._all_properties = {}
    c._okayToUse = int(data[b'okay'])
    factory._all_classes[name] = c
    for p in data[b'props']:
        name = p[b'name']
        rng = p[b'range']
        ccname = p[b'propName']
        if p[b'inverse']:
            i = p[b'inverse']
            if i[0] == b'P':
                invRdf = b'crm:%s' % i
            else:
                invRdf = i
        else:
            invRdf = b''
        okay = p[b'okay']
        if not okay:
            okay = b'1'
        okay = int(okay)
        mult = p[b'multiple']
        if not mult:
            mult = b'0'
        mult = int(mult)
        c._properties[ccname] = {b'rdf': b'crm:%s' % name, b'rangeStr': rng, 
           b'inverseRdf': invRdf, 
           b'okayToUse': okay, 
           b'multiple': mult}

    for s in data[b'subs']:
        build_class(s, c, vocabData)


def build_classes(fn=None, topClass=None):
    if not fn:
        dd = os.path.join(os.path.dirname(__file__), b'data')
        fn = os.path.join(dd, b'crm_vocab.tsv')
        topClass = b'E1_CRM_Entity'
    vocabData = process_tsv(fn)
    build_class(topClass, BaseResource, vocabData)
    for v in vocabData.values():
        c = v[b'class']
        if c is BaseResource:
            continue
        for name, value in c._properties.items():
            rngs = value.get(b'rangeStr', None)
            if not rngs:
                continue
            inverse = None
            rngd = vocabData.get(value[b'rangeStr'], None)
            if rngs in ('rdfs:Literal', 'xsd:dateTime', 'xsd:string', 'rdfs:Class'):
                rng = str
            elif not rngd:
                raise ConfigurationError(b'Failed to get range for %s property %s - %s' % (c, name, rngs))
            else:
                rng = rngd[b'class']
                for ik, iv in rng._properties.items():
                    if iv[b'inverseRdf'] == value[b'rdf']:
                        inverse = ik
                        break

            c._all_properties[name] = PropInfo(name, value[b'rdf'], rng, inverse, value.get(b'inverseRdf', None), value.get(b'multiple', 1), value.get(b'okayToUse', 0))

    for v in vocabData.values():
        c = v[b'class']
        c._classhier = inspect.getmro(c)[:-1]
        try:
            del c._properties
        except:
            pass

    return


factory = CromulentFactory(b'http://lod.example.org/museum/', context=b'https://linked.art/ns/v1/linked-art.json')
build_classes()