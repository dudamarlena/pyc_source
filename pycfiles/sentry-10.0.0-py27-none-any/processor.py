# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/lang/javascript/processor.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
__all__ = ['JavaScriptStacktraceProcessor']
import logging, re, sys, base64, six, zlib
from django.conf import settings
from os.path import splitext
from requests.utils import get_encoding_from_headers
from six.moves.urllib.parse import urljoin, urlsplit
from symbolic import SourceMapView
try:
    from OpenSSL.SSL import ZeroReturnError
except ImportError:

    class ZeroReturnError(Exception):
        pass


from sentry import http
from sentry.interfaces.stacktrace import Stacktrace
from sentry.models import EventError, ReleaseFile, Organization
from sentry.utils.cache import cache
from sentry.utils.files import compress_file
from sentry.utils.hashlib import md5_text
from sentry.utils.http import is_valid_origin
from sentry.utils.safe import get_path
from sentry.utils import metrics
from sentry.stacktraces.processing import StacktraceProcessor
from .cache import SourceCache, SourceMapCache
LINES_OF_CONTEXT = 5
BASE64_SOURCEMAP_PREAMBLE = 'data:application/json;base64,'
BASE64_PREAMBLE_LENGTH = len(BASE64_SOURCEMAP_PREAMBLE)
UNKNOWN_MODULE = '<unknown module>'
CLEAN_MODULE_RE = re.compile('^\n(?:/|  # Leading slashes\n(?:\n    (?:java)?scripts?|js|build|static|node_modules|bower_components|[_\\.~].*?|  # common folder prefixes\n    v?(?:\\d+\\.)*\\d+|   # version numbers, v1, 1.0.0\n    [a-f0-9]{7,8}|     # short sha\n    [a-f0-9]{32}|      # md5\n    [a-f0-9]{40}       # sha1\n)/)+|\n(?:[-\\.][a-f0-9]{7,}$)  # Ending in a commitish\n', re.X | re.I)
VERSION_RE = re.compile('^[a-f0-9]{32}|[a-f0-9]{40}$', re.I)
NODE_MODULES_RE = re.compile('\\bnode_modules/')
SOURCE_MAPPING_URL_RE = re.compile('\\/\\/# sourceMappingURL=(.*)$')
CACHE_CONTROL_RE = re.compile('max-age=(\\d+)')
CACHE_CONTROL_MAX = 7200
CACHE_CONTROL_MIN = 60
MAX_RESOURCE_FETCHES = 100
logger = logging.getLogger(__name__)

class UnparseableSourcemap(http.BadSource):
    error_type = EventError.JS_INVALID_SOURCEMAP


def trim_line(line, column=0):
    """
    Trims a line down to a goal of 140 characters, with a little
    wiggle room to be sensible and tries to trim around the given
    `column`. So it tries to extract 60 characters before and after
    the provided `column` and yield a better context.
    """
    line = line.strip('\n')
    ll = len(line)
    if ll <= 150:
        return line
    if column > ll:
        column = ll
    start = max(column - 60, 0)
    if start < 5:
        start = 0
    end = min(start + 140, ll)
    if end > ll - 5:
        end = ll
    if end == ll:
        start = max(end - 140, 0)
    line = line[start:end]
    if end < ll:
        line += ' {snip}'
    if start > 0:
        line = '{snip} ' + line
    return line


def get_source_context(source, lineno, colno, context=LINES_OF_CONTEXT):
    if not source:
        return (None, None, None)
    else:
        if lineno > 0:
            lineno -= 1
        lower_bound = max(0, lineno - context)
        upper_bound = min(lineno + 1 + context, len(source))
        try:
            pre_context = [ trim_line(x) for x in source[lower_bound:lineno] ]
        except IndexError:
            pre_context = []

        try:
            context_line = trim_line(source[lineno], colno)
        except IndexError:
            context_line = ''

        try:
            post_context = [ trim_line(x) for x in source[lineno + 1:upper_bound] ]
        except IndexError:
            post_context = []

        return (
         pre_context or None, context_line, post_context or None)


def discover_sourcemap(result):
    """
    Given a UrlResult object, attempt to discover a sourcemap.
    """
    sourcemap = result.headers.get('sourcemap', result.headers.get('x-sourcemap'))
    if not sourcemap:
        parsed_body = result.body.split('\n')
        if len(parsed_body) > 10:
            possibilities = parsed_body[:5] + parsed_body[-5:]
        else:
            possibilities = parsed_body
        for line in possibilities:
            if line[:21] in ('//# sourceMappingURL=', '//@ sourceMappingURL='):
                sourcemap = line[21:].rstrip()

        if not sourcemap:
            search_space = possibilities[(-1)][-300:].rstrip()
            match = SOURCE_MAPPING_URL_RE.search(search_space)
            if match:
                sourcemap = match.group(1)
    if sourcemap:
        if '/*' in sourcemap and sourcemap[-2:] == '*/':
            index = sourcemap.index('/*')
            if index == 0:
                raise AssertionError('react-native comment found at bad location: %d, %r' % (index, sourcemap))
            sourcemap = sourcemap[:index]
        sourcemap = urljoin(result.url, sourcemap)
    return sourcemap


def fetch_release_file(filename, release, dist=None):
    cache_key = 'releasefile:v1:%s:%s' % (release.id, md5_text(filename).hexdigest())
    logger.debug('Checking cache for release artifact %r (release_id=%s)', filename, release.id)
    result = cache.get(cache_key)
    dist_name = dist and dist.name or None
    if result is None:
        filename_choices = ReleaseFile.normalize(filename)
        filename_idents = [ ReleaseFile.get_ident(f, dist_name) for f in filename_choices ]
        logger.debug('Checking database for release artifact %r (release_id=%s)', filename, release.id)
        possible_files = list(ReleaseFile.objects.filter(release=release, dist=dist, ident__in=filename_idents).select_related('file'))
        if len(possible_files) == 0:
            logger.debug('Release artifact %r not found in database (release_id=%s)', filename, release.id)
            cache.set(cache_key, -1, 60)
            return
        if len(possible_files) == 1:
            releasefile = possible_files[0]
        else:
            releasefile = next(rf for ident in filename_idents for rf in possible_files if rf.ident == ident)
        logger.debug('Found release artifact %r (id=%s, release_id=%s)', filename, releasefile.id, release.id)
        try:
            with metrics.timer('sourcemaps.release_file_read'):
                with releasefile.file.getfile() as (fp):
                    z_body, body = compress_file(fp)
        except Exception:
            logger.error('sourcemap.compress_read_failed', exc_info=sys.exc_info())
            result = None
        else:
            headers = {k.lower():v for k, v in releasefile.file.headers.items()}
            encoding = get_encoding_from_headers(headers)
            result = http.UrlResult(filename, headers, body, 200, encoding)
            cache.set(cache_key, (headers, z_body, 200, encoding), 3600)

    elif result == -1:
        result = None
    else:
        try:
            encoding = result[3]
        except IndexError:
            encoding = None

        result = http.UrlResult(filename, result[0], zlib.decompress(result[1]), result[2], encoding)
    return result


def fetch_file(url, project=None, release=None, dist=None, allow_scraping=True):
    """
    Pull down a URL, returning a UrlResult object.

    Attempts to fetch from the cache.
    """
    if url[-3:] == '...':
        raise http.CannotFetch({'type': EventError.JS_MISSING_SOURCE, 'url': http.expose_url(url)})
    if release:
        with metrics.timer('sourcemaps.release_file'):
            result = fetch_release_file(url, release, dist)
    else:
        result = None
    cache_key = 'source:cache:v4:%s' % (md5_text(url).hexdigest(),)
    if result is None:
        if not allow_scraping or not url.startswith(('http:', 'https:')):
            error = {'type': EventError.JS_MISSING_SOURCE, 'url': http.expose_url(url)}
            raise http.CannotFetch(error)
        logger.debug('Checking cache for url %r', url)
        result = cache.get(cache_key)
        if result is not None:
            try:
                encoding = result[4]
            except IndexError:
                encoding = None

            result = http.UrlResult(result[0], result[1], zlib.decompress(result[2]), result[3], encoding)
    if result is None:
        headers = {}
        verify_ssl = False
        if project and is_valid_origin(url, project=project):
            verify_ssl = bool(project.get_option('sentry:verify_ssl', False))
            token = project.get_option('sentry:token')
            if token:
                token_header = project.get_option('sentry:token_header') or 'X-Sentry-Token'
                headers[token_header] = token
        with metrics.timer('sourcemaps.fetch'):
            result = http.fetch_file(url, headers=headers, verify_ssl=verify_ssl)
            z_body = zlib.compress(result.body)
            cache.set(cache_key, (
             url, result.headers, z_body, result.status, result.encoding), get_max_age(result.headers))
    if result.status != 200:
        raise http.CannotFetch({'type': EventError.FETCH_INVALID_HTTP_CODE, 
           'value': result.status, 
           'url': http.expose_url(url)})
    if not isinstance(result.body, six.binary_type):
        try:
            result = http.UrlResult(result.url, result.headers, result.body.encode('utf8'), result.status, result.encoding)
        except UnicodeEncodeError:
            error = {'type': EventError.FETCH_INVALID_ENCODING, 'value': 'utf8', 
               'url': http.expose_url(url)}
            raise http.CannotFetch(error)

    if url.endswith('.js'):
        body_start = result.body[:20].lstrip()
        if body_start[:1] == '<':
            error = {'type': EventError.JS_INVALID_CONTENT, 'url': url}
            raise http.CannotFetch(error)
    return result


def get_max_age(headers):
    cache_control = headers.get('cache-control')
    max_age = CACHE_CONTROL_MIN
    if cache_control:
        match = CACHE_CONTROL_RE.search(cache_control)
        if match:
            max_age = max(CACHE_CONTROL_MIN, int(match.group(1)))
    return min(max_age, CACHE_CONTROL_MAX)


def fetch_sourcemap(url, project=None, release=None, dist=None, allow_scraping=True):
    if is_data_uri(url):
        try:
            body = base64.b64decode(url[BASE64_PREAMBLE_LENGTH:] + '=' * (-(len(url) - BASE64_PREAMBLE_LENGTH) % 4))
        except TypeError as e:
            raise UnparseableSourcemap({'url': '<base64>', 'reason': e.message})

    else:
        result = fetch_file(url, project=project, release=release, dist=dist, allow_scraping=allow_scraping)
        body = result.body
    try:
        return SourceMapView.from_json_bytes(body)
    except Exception as exc:
        logger.debug(six.text_type(exc), exc_info=True)
        raise UnparseableSourcemap({'url': http.expose_url(url)})


def is_data_uri(url):
    return url[:BASE64_PREAMBLE_LENGTH] == BASE64_SOURCEMAP_PREAMBLE


def generate_module(src):
    """
    Converts a url into a made-up module name by doing the following:
     * Extract just the path name ignoring querystrings
     * Trimming off the initial /
     * Trimming off the file extension
     * Removes off useless folder prefixes

    e.g. http://google.com/js/v1.0/foo/bar/baz.js -> foo/bar/baz
    """
    if not src:
        return UNKNOWN_MODULE
    filename, ext = splitext(urlsplit(src).path)
    if filename.endswith('.min'):
        filename = filename[:-4]
    tokens = filename.split('/')
    for idx, token in enumerate(tokens):
        if VERSION_RE.match(token):
            return ('/').join(tokens[idx + 1:])

    return CLEAN_MODULE_RE.sub('', filename) or UNKNOWN_MODULE


class JavaScriptStacktraceProcessor(StacktraceProcessor):
    """
    Attempts to fetch source code for javascript frames.

    Frames must match the following requirements:

    - lineno >= 0
    - colno >= 0
    - abs_path is the HTTP URI to the source
    - context_line is empty

    Mutates the input ``data`` with expanded context if available.
    """

    def __init__(self, *args, **kwargs):
        StacktraceProcessor.__init__(self, *args, **kwargs)
        organization = getattr(self.project, '_organization_cache', None)
        if not organization:
            organization = Organization.objects.get_from_cache(id=self.project.organization_id)
        self.max_fetches = MAX_RESOURCE_FETCHES
        self.allow_scraping = organization.get_option('sentry:scrape_javascript', True) is not False and self.project.get_option('sentry:scrape_javascript', True)
        self.fetch_count = 0
        self.sourcemaps_touched = set()
        self.cache = SourceCache()
        self.sourcemaps = SourceMapCache()
        self.release = None
        self.dist = None
        return

    def get_stacktraces(self, data):
        exceptions = get_path(data, 'exception', 'values', filter=True, default=())
        stacktraces = [ e['stacktrace'] for e in exceptions if e.get('stacktrace') ]
        if 'stacktrace' in data:
            stacktraces.append(data['stacktrace'])
        return [ (s, Stacktrace.to_python(s)) for s in stacktraces ]

    def get_valid_frames(self):
        frames = []
        for info in self.stacktrace_infos:
            frames.extend([ f for f in info.stacktrace['frames'] if f.get('lineno') is not None ])

        return frames

    def preprocess_step(self, processing_task):
        frames = self.get_valid_frames()
        if not frames:
            logger.debug('Event %r has no frames with enough context to fetch remote source', self.data['event_id'])
            return False
        self.release = self.get_release(create=True)
        if self.data.get('dist') and self.release:
            self.dist = self.release.get_dist(self.data['dist'])
        self.populate_source_cache(frames)
        return True

    def handles_frame(self, frame, stacktrace_info):
        platform = frame.get('platform') or self.data.get('platform')
        return settings.SENTRY_SCRAPE_JAVASCRIPT_CONTEXT and platform in ('javascript',
                                                                          'node')

    def preprocess_frame(self, processable_frame):
        processable_frame.data = {'token': None}
        return

    def process_frame(self, processable_frame, processing_task):
        frame = processable_frame.frame
        token = None
        cache = self.cache
        sourcemaps = self.sourcemaps
        all_errors = []
        sourcemap_applied = False
        if not frame.get('abs_path') or not frame.get('lineno'):
            return
        if self.data.get('platform') == 'node' and not frame.get('abs_path').startswith(('/',
                                                                                         'app:',
                                                                                         'webpack:')):
            return
        else:
            errors = cache.get_errors(frame['abs_path'])
            if errors:
                all_errors.extend(errors)
            source = self.get_sourceview(frame['abs_path'])
            in_app = None
            new_frame = dict(frame)
            raw_frame = dict(frame)
            sourcemap_url, sourcemap_view = sourcemaps.get_link(frame['abs_path'])
            self.sourcemaps_touched.add(sourcemap_url)
            if sourcemap_view and frame.get('colno') is None:
                all_errors.append({'type': EventError.JS_NO_COLUMN, 'url': http.expose_url(frame['abs_path'])})
            else:
                if sourcemap_view:
                    if is_data_uri(sourcemap_url):
                        sourcemap_label = frame['abs_path']
                    else:
                        sourcemap_label = sourcemap_url
                    sourcemap_label = http.expose_url(sourcemap_label)
                    if frame.get('function'):
                        minified_function_name = frame['function']
                        minified_source = self.get_sourceview(frame['abs_path'])
                    else:
                        minified_function_name = minified_source = None
                    try:
                        assert frame['lineno'] > 0, 'line numbers are 1-indexed'
                        token = sourcemap_view.lookup(frame['lineno'] - 1, frame['colno'] - 1, minified_function_name, minified_source)
                    except Exception:
                        token = None
                        all_errors.append({'type': EventError.JS_INVALID_SOURCEMAP_LOCATION, 
                           'column': frame.get('colno'), 
                           'row': frame.get('lineno'), 
                           'source': frame['abs_path'], 
                           'sourcemap': sourcemap_label})

                    processable_frame.data['token'] = token
                    new_frame['data'] = dict(frame.get('data') or {}, sourcemap=sourcemap_label)
                    sourcemap_applied = True
                    if token is not None:
                        abs_path = urljoin(sourcemap_url, token.src)
                        logger.debug('Mapping compressed source %r to mapping in %r', frame['abs_path'], abs_path)
                        source = self.get_sourceview(abs_path)
                    if source is None:
                        errors = cache.get_errors(abs_path)
                        if errors:
                            all_errors.extend(errors)
                        else:
                            all_errors.append({'type': EventError.JS_MISSING_SOURCE, 'url': http.expose_url(abs_path)})
                    if token is not None:
                        new_frame['lineno'] = token.src_line + 1
                        new_frame['colno'] = token.src_col + 1
                        original_function_name = token.function_name
                        if original_function_name is None:
                            last_token = None
                            if processable_frame.previous_frame and processable_frame.previous_frame.processor is self:
                                last_token = processable_frame.previous_frame.data.get('token')
                                if last_token:
                                    original_function_name = last_token.name
                        if original_function_name is not None:
                            new_frame['function'] = original_function_name
                        filename = token.src
                        if abs_path.startswith('webpack:'):
                            filename = abs_path
                            if '/~/' in filename:
                                filename = '~/' + abs_path.split('/~/', 1)[(-1)]
                            else:
                                filename = filename.split('webpack:///', 1)[(-1)]
                            if filename.startswith('~/') or '/node_modules/' in filename or not filename.startswith('./'):
                                in_app = False
                            elif filename.startswith('./'):
                                in_app = True
                            new_frame['module'] = generate_module(filename)
                        elif '/node_modules/' in abs_path:
                            in_app = False
                        if abs_path.startswith('app:'):
                            if filename and NODE_MODULES_RE.search(filename):
                                in_app = False
                            else:
                                in_app = True
                        new_frame['abs_path'] = abs_path
                        new_frame['filename'] = filename
                        if not frame.get('module') and abs_path.startswith(('http:',
                                                                            'https:',
                                                                            'webpack:',
                                                                            'app:')):
                            new_frame['module'] = generate_module(abs_path)
                elif sourcemap_url:
                    new_frame['data'] = dict(new_frame.get('data') or {}, sourcemap=http.expose_url(sourcemap_url))
                changed_frame = self.expand_frame(new_frame, source=source)
                if not new_frame.get('context_line') and source and new_frame.get('colno') is not None:
                    all_errors.append({'type': EventError.JS_INVALID_SOURCEMAP_LOCATION, 
                       'column': new_frame['colno'], 
                       'row': new_frame['lineno'], 
                       'source': new_frame['abs_path']})
                changed_raw = sourcemap_applied and self.expand_frame(raw_frame)
                if sourcemap_applied or all_errors or changed_frame or changed_raw:
                    if in_app is not None:
                        new_frame['in_app'] = in_app
                        raw_frame['in_app'] = in_app
                    return ([new_frame], [raw_frame] if changed_raw else None, all_errors)
            return

    def expand_frame(self, frame, source=None):
        if frame.get('lineno') is not None:
            if source is None:
                source = self.get_sourceview(frame['abs_path'])
                if source is None:
                    logger.debug('No source found for %s', frame['abs_path'])
                    return False
            frame['pre_context'], frame['context_line'], frame['post_context'] = get_source_context(source=source, lineno=frame['lineno'], colno=frame.get('colno') or 0)
            return True
        else:
            return False

    def get_sourceview(self, filename):
        if filename not in self.cache:
            self.cache_source(filename)
        return self.cache.get(filename)

    def cache_source(self, filename):
        sourcemaps = self.sourcemaps
        cache = self.cache
        self.fetch_count += 1
        if self.fetch_count > self.max_fetches:
            cache.add_error(filename, {'type': EventError.JS_TOO_MANY_REMOTE_SOURCES})
            return
        else:
            logger.debug('Fetching remote source %r', filename)
            try:
                result = fetch_file(filename, project=self.project, release=self.release, dist=self.dist, allow_scraping=self.allow_scraping)
            except http.BadSource as exc:
                cache.add_error(filename, exc.data)
                return

            cache.add(filename, result.body, result.encoding)
            cache.alias(result.url, filename)
            sourcemap_url = discover_sourcemap(result)
            if not sourcemap_url:
                return
            logger.debug('Found sourcemap %r for minified script %r', sourcemap_url[:256], result.url)
            sourcemaps.link(filename, sourcemap_url)
            if sourcemap_url in sourcemaps:
                return
            try:
                sourcemap_view = fetch_sourcemap(sourcemap_url, project=self.project, release=self.release, dist=self.dist, allow_scraping=self.allow_scraping)
            except http.BadSource as exc:
                cache.add_error(filename, exc.data)
                return

            sourcemaps.add(sourcemap_url, sourcemap_view)
            for src_id, source_name in sourcemap_view.iter_sources():
                source_view = sourcemap_view.get_sourceview(src_id)
                if source_view is not None:
                    self.cache.add(urljoin(sourcemap_url, source_name), source_view)

            return

    def populate_source_cache(self, frames):
        """
        Fetch all sources that we know are required (being referenced directly
        in frames).
        """
        pending_file_list = set()
        for f in frames:
            if f.get('abs_path') is None:
                continue
            if f['abs_path'] == '<anonymous>':
                continue
            if self.data.get('platform') == 'node' and not f.get('abs_path').startswith('app:'):
                continue
            pending_file_list.add(f['abs_path'])

        for idx, filename in enumerate(pending_file_list):
            self.cache_source(filename=filename)

        return

    def close(self):
        StacktraceProcessor.close(self)
        if self.sourcemaps_touched:
            metrics.incr('sourcemaps.processed', amount=len(self.sourcemaps_touched), skip_internal=True, tags={'project_id': self.project.id})