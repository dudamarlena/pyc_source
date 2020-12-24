# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/citation.py
# Compiled at: 2017-06-20 09:14:35
import collections, datetime, json, operator, re, socket, string, sys, urllib2, utopia, utopia.extension, uuid
from utopia.log import logger
UUID_KEYSPEC = 'key'
PROVENANCE_KEYSPEC = 'provenance'
PROVENANCE_WHENCE_KEY = 'whence'
PROVENANCE_WHENCE_KEYSPEC = PROVENANCE_KEYSPEC + '/' + PROVENANCE_WHENCE_KEY
PROVENANCE_WHEN_KEY = 'when'
PROVENANCE_WHEN_KEYSPEC = PROVENANCE_KEYSPEC + '/' + PROVENANCE_WHEN_KEY
PROVENANCE_SOURCES_KEY = 'sources'
PROVENANCE_SOURCES_KEYSPEC = PROVENANCE_KEYSPEC + '/' + PROVENANCE_SOURCES_KEY
PROVENANCE_INPUT_KEY = 'input'
PROVENANCE_INPUT_KEYSPEC = PROVENANCE_KEYSPEC + '/' + PROVENANCE_INPUT_KEY
PROVENANCE_REFS_KEY = 'refs'
PROVENANCE_REFS_KEYSPEC = PROVENANCE_KEYSPEC + '/' + PROVENANCE_REFS_KEY
PROVENANCE_PLUGIN_KEY = 'plugin'
PROVENANCE_PLUGIN_KEYSPEC = PROVENANCE_KEYSPEC + '/' + PROVENANCE_PLUGIN_KEY
PROVENANCE_DELIMITER = ':'
_kwarg_sentinel = object()
mergeable_keys = ('keywords', 'links')
_keyspec_translator = string.maketrans('[.#', '//:')

def normalise_keyspec(keyspec):
    """Normalise a keyspec into path notation"""
    if isinstance(keyspec, unicode):
        return keyspec.translate({ord('['): '/', 
           ord('.'): '/', 
           ord('#'): ':', 
           ord(']'): None})
    else:
        return keyspec.translate(_keyspec_translator, ']')
        return


def split_keyspec(keyspec):
    """Normalise and split the keyspec into a list of keys."""
    return normalise_keyspec(keyspec).split('/')


def pick(obj, keyspec, default=_kwarg_sentinel):
    """Pick a value from a obj according to its keyspec"""
    curr_obj = obj
    has_default = default != _kwarg_sentinel
    try:
        seen = []
        for key in split_keyspec(keyspec):
            if isinstance(curr_obj, collections.Mapping):
                curr_obj = curr_obj[key]
            elif isinstance(curr_obj, collections.Sequence):
                curr_obj = curr_obj[int(key)]
            seen.append(key)

        if isinstance(curr_obj, collections.Sequence) and not isinstance(curr_obj, basestring):
            curr_obj = [ wrap_provenance(curr_obj[i], obj, keyspec + ('/{}').format(i)) for i in xrange(0, len(curr_obj)) ]
        return wrap_provenance(curr_obj, obj, keyspec)
    except (KeyError, IndexError, ValueError):
        if not has_default:
            if len(seen) == 0:
                raise KeyError(key)
            else:
                raise KeyError(('/').join(seen) + '/' + key)
    except:
        if not has_default:
            raise

    return default


def refspec(citation, keyspec=None):
    """Generate a refspec"""
    if UUID_KEYSPEC not in citation:
        citation[UUID_KEYSPEC] = str(uuid.uuid4())
    spec = ('@{0}').format(citation[UUID_KEYSPEC])
    if keyspec is not None:
        spec += ':' + normalise_keyspec(keyspec)
    return spec


def split_refspec(refspec):
    """Split a refspec into a UUID and a keyspec."""
    match = re.match('@(?P<uuid>[0-9a-f-]+):(?P<keyspec>.*)', refspec, re.I)
    if match is not None:
        return (match.group('uuid'), match.group('keyspec'))
    else:
        raise ValueError(('refspec expected in the form @<uuid>:<keyspec>, but received {}').format(refspec))
        return


def wrap_provenance(value, citation=None, keyspec=None):

    class sourced(type(value)):

        def __init__(self, value):
            self.citation = citation
            self.keyspec = keyspec
            super(sourced, self).__init__(value)

        @property
        def refspec(self):
            return refspec(self.citation, self.keyspec)

    return sourced(value)


def has_provenance(value):
    return hasattr(value, 'citation') and hasattr(value, 'keyspec')


def inspect_keyspecs(citation, include_provenance=False):
    """List a citation's keyspecs"""
    specs = set()
    for key, value in citation.items():
        if include_provenance or key != PROVENANCE_KEYSPEC:
            if isinstance(value, collections.Mapping):
                specs.update(set([ ('{0}/{1}').format(key, keyspec) for keyspec in inspect_keyspecs(value) ]))
            else:
                specs.add(key)

    return specs


def set_by_keyspec(citation, keyspec, value):
    """Set a value for a keyspec on a citation"""
    keys = split_keyspec(keyspec)
    for key in keys[:-1]:
        citation.setdefault(key, {})
        citation = citation[key]

    citation[keys[(-1)]] = value


def merge(citation, update):
    """Merge an update into a citation by keyspec"""
    for keyspec in inspect_keyspecs(update, include_provenance=True):
        set_by_keyspec(citation, keyspec, pick(update, keyspec))


pick_order = [
 'utopia',
 'crackle',
 'kend',
 'crossref',
 'pubmed',
 'pmc',
 'arxiv']

def pick_from(citations, keyspec, default=_kwarg_sentinel, order=pick_order, record_in=_kwarg_sentinel):
    """Pick a value from a list of objects according to its keyspec"""
    has_default = default != _kwarg_sentinel
    if isinstance(order, collections.Sequence):

        def order_fn(a, b):
            a = pick(a, PROVENANCE_WHENCE_KEYSPEC, None)
            b = pick(b, PROVENANCE_WHENCE_KEYSPEC, None)
            a = a not in order and -1 or order.index(a)
            b = b not in order and -1 or order.index(b)
            return cmp(b, a)

    else:
        if callable(order):
            order_fn = order
        else:
            raise ValueError(('Invalid ordering (expected list or function): {0}').format(repr(order)))
        citations = sorted(citations, order_fn)
        keyspec, _, whence = keyspec.partition(PROVENANCE_DELIMITER)
        if len(whence) > 0 and whence[(-1)] == '*':
            is_all = True
            whence = whence[:-1]
        else:
            is_all = False
        is_mergeable = keyspec in mergeable_keys
        all = []
        merged = []
        for citation in citations:
            try:
                if len(whence) == 0 or whence == pick(citation, PROVENANCE_WHENCE_KEYSPEC, None):
                    value = pick(citation, keyspec)
                    if is_all:
                        all.append(value)
                    elif is_mergeable:
                        blocked = is_mergeable and value in merged
                        if not blocked:
                            for i in xrange(0, len(value)):
                                item = value[i]
                                if item not in merged:
                                    if record_in != _kwarg_sentinel:
                                        refspec = value.refspec + ('/{}').format(i)
                                        inputs = pick(record_in, PROVENANCE_INPUT_KEYSPEC, [])
                                        if refspec not in inputs:
                                            inputs.append(refspec)
                                            set_by_keyspec(record_in, PROVENANCE_INPUT_KEYSPEC, inputs)
                                    merged.append(item)

                    else:
                        if record_in != _kwarg_sentinel:
                            refspec = value.refspec
                            inputs = pick(record_in, PROVENANCE_INPUT_KEYSPEC, [])
                            if refspec not in inputs:
                                inputs.append(refspec)
                                set_by_keyspec(record_in, PROVENANCE_INPUT_KEYSPEC, inputs)
                        return value
            except:
                pass

    if is_all and len(all) > 0:
        return all
    else:
        if is_mergeable and len(merged) > 0:
            return merged
        if has_default:
            return default
        key = ('/').join(split_keyspec(keyspec))
        if len(whence) > 0:
            key += (':{}').format(whence)
        raise KeyError(key)
        return


def flatten(citations):
    """Flatten a list of objects by keyspec"""
    flattened = {}
    refs = []
    set_by_keyspec(flattened, PROVENANCE_SOURCES_KEYSPEC, citations)
    set_by_keyspec(flattened, PROVENANCE_REFS_KEYSPEC, refs)
    for keyspec in reduce(operator.or_, [ inspect_keyspecs(citation) for citation in citations ]):
        is_mergeable = keyspec in mergeable_keys
        value = pick_from(citations, keyspec, None)
        if value is not None:
            if has_provenance(value):
                refs.append(value.refspec)
            elif is_mergeable and isinstance(value, collections.Sequence):
                refs.extend([ item.refspec for item in value if has_provenance(item) ])
            set_by_keyspec(flattened, keyspec, value)

    return flattened


def filter_links(citations, criteria={}, provenance={}):
    """Find all of a citation's links that match the given criteria"""
    filtered = []
    for links in pick_from(citations, 'links*', []):
        for link in links:
            link_provenance = pick(link.citation, PROVENANCE_KEYSPEC, {})
            match = True
            for key, value in criteria.iteritems():
                if value is None and key not in link or value is not None and link.get(key) != value:
                    match = False
                    break

            if match:
                for key, value in provenance.iteritems():
                    if value is None and key not in link_provenance or value is not None and link_provenance.get(key) != value:
                        match = False
                        break

            if match:
                filtered.append(link)

    return filtered


def has_link(citations, criteria={}, provenance={}):
    """Find if a citation has a link that matches the given criteria"""
    return len(filter_links(citations, criteria=criteria, provenance=provenance)) > 0


class Resolver(utopia.extension.Extension):

    def execute_resolver(self, citations, document=None):
        plugin_name = ('{0}.{1}').format(self.__module__.split('_')[(-1)], self.__class__.__name__)
        logger.debug(('Resolving from {0}: {1}').format(plugin_name, getattr(self, '__doc__', 'Unknown resolver')))
        if len([ citation for citation in citations if pick(citation, PROVENANCE_PLUGIN_KEYSPEC, None) == plugin_name ]) == 0:
            try:
                resolved = self.resolve(citations, document)
                if resolved is not None:
                    if isinstance(resolved, collections.Mapping):
                        resolved = [
                         resolved]
                    sanitised = []
                    for citation in resolved:
                        if len([ key for key in citation.keys() if key != PROVENANCE_KEYSPEC ]) > 0:
                            if hasattr(self, 'provenance') and callable(self.provenance):
                                provenance = self.provenance()
                                if not isinstance(provenance, collections.Mapping):
                                    provenance = {}
                                set_by_keyspec(provenance, PROVENANCE_PLUGIN_KEY, plugin_name)
                                existing = pick(citation, PROVENANCE_KEYSPEC, {})
                                provenance.update(existing)
                                set_by_keyspec(citation, PROVENANCE_KEYSPEC, provenance)
                                set_by_keyspec(citation, PROVENANCE_WHEN_KEYSPEC, datetime.datetime.now().isoformat())
                            sanitised.append(citation)

                    if len(sanitised) > 0:
                        return sanitised
            except Exception as exception:
                if isinstance(exception, urllib2.URLError) and hasattr(exception, 'reason') and isinstance(exception.reason, socket.timeout):
                    exception = exception.reason
                error = {}
                set_by_keyspec(error, PROVENANCE_WHEN_KEYSPEC, datetime.datetime.now().isoformat())
                set_by_keyspec(error, PROVENANCE_PLUGIN_KEYSPEC, plugin_name)
                if hasattr(self, 'provenance') and callable(self.provenance):
                    provenance = self.provenance()
                    if isinstance(provenance, collections.Mapping):
                        existing = pick(error, PROVENANCE_KEYSPEC, {})
                        existing.update(provenance)
                        set_by_keyspec(error, PROVENANCE_KEYSPEC, existing)
                if isinstance(exception, socket.timeout):
                    category = 'timeout'
                    message = 'The server did not respond'
                elif isinstance(exception, urllib2.HTTPError):
                    category = 'server'
                    message = unicode(getattr(exception, 'reason', 'The server did not respond as expected'))
                elif isinstance(exception, urllib2.URLError):
                    category = 'connection'
                    message = unicode(getattr(exception, 'reason', 'The server could not be found'))
                else:
                    category = 'unknown'
                    message = 'An unexpected error occured'
                error['error'] = {'category': category, 'message': message}
                logger.warning(('Error in resolver ({0}): {1}').format(pick(error, PROVENANCE_WHENCE_KEYSPEC, '?'), message), exc_info=True)
                return [error]

        logger.debug(' -> null result')
        return


def resolve(citation=None, citations=None, document=None, purposes=('identify', 'expand', 'dereference')):
    """Push a citation through the resolution pipeline"""
    resolvers = [ ResolverType() for ResolverType in Resolver.types() ]
    resolvers.sort(key=lambda r: r.weight())
    if citations is None:
        citations = []
    if citation is not None:
        citations.append(citation)
    for purpose in purposes:
        for resolver in resolvers:
            if hasattr(resolver, 'purposes') and resolver.purposes() == purpose:
                resolved = resolver.execute_resolver(citations, document)
                if resolved is not None:
                    citations.extend(resolved)

    return flatten(citations)


def expand(citation=None, citations=None, document=None):
    return resolve(citation=citation, citations=citations, document=document, purposes=('expand', ))


def identify(citation=None, citations=None, document=None):
    return resolve(citation=citation, citations=citations, document=document, purposes=('identify', ))


def dereference(citation=None, citations=None, document=None):
    return resolve(citation=citation, citations=citations, document=document, purposes=('dereference', ))


try:
    import utopiabridge
except ImportError:
    utopiabridge = None

if utopiabridge is not None:

    def format(citation):

        def _format(string, value):
            if value is not None and len(('{0}').format(value)) > 0:
                return unicode(string).format(value)
            else:
                return ''
                return

        def _get(map, key, default=None):
            value = map.get(('property:{0}').format(key))
            if value is None:
                value = map.get(key, default)
            if value is None:
                return default
            else:
                return value

        def _has(map, key):
            return ('property:{0}').format(key) in map or key in map

        html = None
        if _has(citation, 'unstructured'):
            if not (_has(citation, 'title') or _has(citation, 'authors') or _has(citation, 'year') or _has(citation, 'publisher') or _has(citation, 'publication-title')):
                html = _get(citation, 'unstructured')
        if html is None and hasattr(utopia.citation, '_formatCSL'):
            html = utopia.citation._formatCSL(citation)
        return html


    def render(citation, process=False, links=True):

        def jsonify(obj):
            return json.dumps(obj).replace("'", '&#39;').replace('"', '&#34;')

        if process:
            content = ''
        else:
            content = utopia.citation.format(citation)
        return ('<div class="-papyro-internal-citation" data-citation="{0}" data-process="{1}" data-links="{2}">{3}</div>').format(jsonify(citation), jsonify(process), jsonify(links), content)