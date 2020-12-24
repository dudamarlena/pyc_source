# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synapseclient/core/utils.py
# Compiled at: 2020-03-23 17:17:03
# Size of source mod 2**32: 29139 bytes
"""
*****************
Utility Functions
*****************

Utility functions useful in the implementation and testing of the Synapse client.

"""
import os, sys, hashlib, re, cgi, datetime, errno, inspect, random, requests, collections, tempfile, platform, functools, threading, uuid, importlib, numbers, urllib.parse as urllib_parse
UNIX_EPOCH = datetime.datetime(1970, 1, 1, 0, 0)
ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'
ISO_FORMAT_MICROS = '%Y-%m-%dT%H:%M:%S.%fZ'
GB = 1073741824
MB = 1048576
KB = 1024
BUFFER_SIZE = 8 * KB

def md5_for_file(filename, block_size=2 * MB):
    """
    Calculates the MD5 of the given file.
    See `source <http://stackoverflow.com/questions/1131220/get-md5-hash-of-a-files-without-open-it-in-python>`_.

    :param filename:   The file to read in
    :param block_size: How much of the file to read in at once (bytes).
                       Defaults to 2 MB
    :returns: The MD5
    """
    md5 = hashlib.md5()
    with open(filename, 'rb') as (f):
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)

    return md5


def download_file(url, localFilepath=None):
    """
    Downloads a remote file.

    :param localFilePath: May be None, in which case a temporary file is created

    :returns: localFilePath
    """
    f = None
    try:
        if localFilepath:
            dir = os.path.dirname(localFilepath)
            if not os.path.exists(dir):
                os.makedirs(dir)
            f = open(localFilepath, 'wb')
        else:
            f = tempfile.NamedTemporaryFile(delete=False)
            localFilepath = f.name
        r = requests.get(url, stream=True)
        toBeTransferred = float(r.headers['content-length'])
        for nChunks, chunk in enumerate(r.iter_content(chunk_size=10240)):
            if chunk:
                f.write(chunk)
                printTransferProgress(nChunks * 1024 * 10, toBeTransferred)

    finally:
        if f:
            f.close()
            printTransferProgress(toBeTransferred, toBeTransferred)

    return localFilepath


def extract_filename(content_disposition_header, default_filename=None):
    """
    Extract a filename from an HTTP content-disposition header field.

    See `this memo <http://tools.ietf.org/html/rfc6266>`_ and `this package <http://pypi.python.org/pypi/rfc6266>`_
    for cryptic details.
    """
    if not content_disposition_header:
        return default_filename
    else:
        value, params = cgi.parse_header(content_disposition_header)
        return params.get('filename', default_filename)


def extract_user_name(profile):
    """
    Extract a displayable user name from a user's profile
    """
    if 'userName' in profile:
        if profile['userName']:
            return profile['userName']
        else:
            if 'displayName' in profile:
                if profile['displayName']:
                    return profile['displayName']
            if 'firstName' in profile:
                if profile['firstName']:
                    if 'lastName' in profile:
                        if profile['lastName']:
                            return profile['firstName'] + ' ' + profile['lastName']
            if 'lastName' in profile:
                if profile['lastName']:
                    return profile['lastName']
    else:
        if 'firstName' in profile:
            if profile['firstName']:
                return profile['firstName']
    return str(profile.get('id', 'Unknown-user'))


def _get_from_members_items_or_properties(obj, key):
    if hasattr(obj, key):
        return getattr(obj, key)
    try:
        if hasattr(obj, 'properties'):
            if key in obj.properties:
                return obj.properties[key]
        if key in obj:
            return obj[key]
        else:
            return obj['properties'][key]
    except (KeyError, TypeError):
        pass


def id_of(obj):
    """
    Try to figure out the Synapse ID of the given object.

    :param obj: May be a string, Entity object, or dictionary

    :returns: The ID or throws an exception
    """
    if isinstance(obj, str):
        return str(obj)
    if isinstance(obj, numbers.Number):
        return str(obj)
    id_attr_names = ['id', 'ownerId', 'tableId']
    for attribute_name in id_attr_names:
        syn_id = _get_from_members_items_or_properties(obj, attribute_name)
        if syn_id is not None:
            return str(syn_id)

    raise ValueError("Invalid parameters: couldn't find id of " + str(obj))


def is_in_path(id, path):
    """Determines whether id is in the path as returned from /entity/{id}/path

    :param id:      synapse id string
    :param path:    object as returned from '/entity/{id}/path'

    :returns: True or False
    """
    return id in [item['id'] for item in path['path']]


def get_properties(entity):
    """Returns the dictionary of properties of the given Entity."""
    if hasattr(entity, 'properties'):
        return entity.properties
    else:
        return entity


def is_url(s):
    """Return True if the string appears to be a valid URL."""
    if isinstance(s, str):
        try:
            url_parts = urllib_parse.urlsplit(s)
            if len(url_parts.scheme) == 1:
                if url_parts.scheme.isalpha():
                    return False
            if url_parts.scheme == 'file':
                if bool(url_parts.path):
                    return True
            return bool(url_parts.scheme) and bool(url_parts.netloc)
        except Exception:
            return False

    return False


def as_url(s):
    """Tries to convert the input into a proper URL."""
    url_parts = urllib_parse.urlsplit(s)
    if len(url_parts.scheme) == 1:
        if url_parts.scheme.isalpha():
            return 'file:///%s' % str(s).replace('\\', '/')
    if url_parts.scheme:
        return url_parts.geturl()
    else:
        return 'file://%s' % str(s)


def guess_file_name(string):
    """Tries to derive a filename from an arbitrary string."""
    path = normalize_path(urllib_parse.urlparse(string).path)
    tokens = [x for x in path.split('/') if x != '']
    if len(tokens) > 0:
        return tokens[(-1)]
    if len(path) > 0:
        path = re.sub('[^a-zA-Z0-9_.+() -]', '', path)
    if len(path) > 0:
        return path
    raise ValueError('Could not derive a name from %s' % string)


def normalize_path(path):
    """Transforms a path into an absolute path with forward slashes only."""
    if path is None:
        return
    else:
        return re.sub('\\\\', '/', os.path.normcase(os.path.abspath(path)))


def equal_paths(path1, path2):
    """
    Compare file paths in a platform neutral way
    """
    return normalize_path(path1) == normalize_path(path2)


def file_url_to_path(url, verify_exists=False):
    """
    Convert a file URL to a path, handling some odd cases around Windows paths.

    :param url:             a file URL
    :param verify_exists:   If true, return an populated dict only if the resulting file path exists on the local file
                            system.

    :returns: a path or None if the URL is not a file URL.
    """
    parts = urllib_parse.urlsplit(url)
    if parts.scheme == 'file' or parts.scheme == '':
        path = parts.path
        if re.match('\\/[A-Za-z]:', path):
            path = path[1:]
        if os.path.exists(path) or not verify_exists:
            return path


def is_same_base_url(url1, url2):
    """Compares two urls to see if they are the same excluding up to the base path

    :param url1: a URL
    :param url2: a second URL

    :returns: Boolean
    """
    url1 = urllib_parse.urlsplit(url1)
    url2 = urllib_parse.urlsplit(url2)
    return url1.scheme == url2.scheme and url1.hostname == url2.hostname


def is_synapse_id(obj):
    """If the input is a Synapse ID return it, otherwise return None"""
    if isinstance(obj, str):
        m = re.match('(syn\\d+)', obj)
        if m:
            return m.group(1)


def is_date(dt):
    """Objects of class datetime.date and datetime.datetime will be recognized as dates"""
    return isinstance(dt, datetime.date) or isinstance(dt, datetime.datetime)


def to_list(value):
    """Convert the value (an iterable or a scalar value) to a list."""
    if isinstance(value, collections.Iterable):
        if not isinstance(value, str):
            return list(value)
    return [
     value]


def _to_iterable(value):
    """Convert the value (an iterable or a scalar value) to an iterable."""
    if isinstance(value, collections.Iterable):
        return value
    else:
        return (
         value,)


def make_bogus_data_file(n=100, seed=None):
    """
    Makes a bogus data file for testing. It is the caller's responsibility to clean up the file when finished.

    :param n:    How many random floating point numbers to be written into the file, separated by commas
    :param seed: Random seed for the random numbers

    :returns: The name of the file
    """
    if seed is not None:
        random.seed(seed)
    data = [random.gauss(mu=0.0, sigma=1.0) for i in range(n)]
    f = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    try:
        f.write(', '.join(str(n) for n in data))
        f.write('\n')
    finally:
        f.close()

    return normalize_path(f.name)


def make_bogus_binary_file(n=1 * MB, filepath=None, printprogress=False):
    """
    Makes a bogus binary data file for testing. It is the caller's responsibility to clean up the file when finished.

    :param n:       How many bytes to write

    :returns: The name of the file
    """
    with open(filepath, 'wb') if filepath else tempfile.NamedTemporaryFile(mode='wb', suffix='.dat', delete=False) as (f):
        if not filepath:
            filepath = f.name
        progress = 0
        remaining = n
        while remaining > 0:
            buff_size = int(min(remaining, 1 * MB))
            f.write(os.urandom(buff_size))
            remaining -= buff_size
            if printprogress:
                progress += buff_size
                printTransferProgress(progress, n, 'Generated ', filepath)

        return normalize_path(filepath)


def to_unix_epoch_time(dt):
    """
    Convert either `datetime.date or datetime.datetime objects <http://docs.python.org/2/library/datetime.html>`_
    to UNIX time.
    """
    if type(dt) == datetime.date:
        return (dt - UNIX_EPOCH.date()).total_seconds() * 1000
    else:
        return int((dt - UNIX_EPOCH).total_seconds() * 1000)


def to_unix_epoch_time_secs(dt):
    """
    Convert either `datetime.date or datetime.datetime objects <http://docs.python.org/2/library/datetime.html>`_
    to UNIX time.
    """
    if type(dt) == datetime.date:
        return (dt - UNIX_EPOCH.date()).total_seconds()
    else:
        return (dt - UNIX_EPOCH).total_seconds()


def from_unix_epoch_time_secs(secs):
    """Returns a Datetime object given milliseconds since midnight Jan 1, 1970."""
    if isinstance(secs, str):
        secs = float(secs)
    if platform.system() == 'Windows' and secs < 0:
        mirror_date = datetime.datetime.utcfromtimestamp(abs(secs))
        return UNIX_EPOCH - (mirror_date - UNIX_EPOCH)
    else:
        return datetime.datetime.utcfromtimestamp(secs)


def from_unix_epoch_time(ms):
    """Returns a Datetime object given milliseconds since midnight Jan 1, 1970."""
    if isinstance(ms, str):
        ms = float(ms)
    return from_unix_epoch_time_secs(ms / 1000.0)


def datetime_to_iso(dt, sep='T'):
    fmt = '{time.year:04}-{time.month:02}-{time.day:02}{sep}{time.hour:02}:{time.minute:02}:{time.second:02}.{millisecond:03}{tz}'
    if dt.microsecond >= 999500:
        dt -= datetime.timedelta(microseconds=(dt.microsecond))
        dt += datetime.timedelta(seconds=1)
    return fmt.format(time=dt, millisecond=(int(round(dt.microsecond / 1000.0))), tz='Z', sep=sep)


def iso_to_datetime(iso_time):
    return datetime.datetime.strptime(iso_time, ISO_FORMAT_MICROS)


def format_time_interval(seconds):
    """Format a time interval given in seconds to a readable value, e.g. "5 minutes, 37 seconds"."""
    periods = (('year', 31536000), ('month', 2592000), ('day', 86400), ('hour', 3600),
               ('minute', 60), ('second', 1))
    result = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds or period_name == 'second':
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value > 0 or period_name == 'second':
                if period_value == 1:
                    result.append('%d %s' % (period_value, period_name))
                else:
                    result.append('%d %ss' % (period_value, period_name))

    return ', '.join(result)


def _find_used(activity, predicate):
    """Finds a particular used resource in an activity that matches a predicate."""
    for resource in activity['used']:
        if predicate(resource):
            return resource


def itersubclasses(cls, _seen=None):
    """
    http://code.activestate.com/recipes/576949/ (r3)

    itersubclasses(cls)

    Generator over all subclasses of a given class, in depth first order.

    >>> list(itersubclasses(int)) == [bool]
    True
    >>> class A(object): pass
    >>> class B(A): pass
    >>> class C(A): pass
    >>> class D(B,C): pass
    >>> class E(D): pass
    >>>
    >>> for cls in itersubclasses(A):
    ...     print(cls.__name__)
    B
    D
    E
    C
    >>> # get ALL (new-style) classes currently defined
    >>> [cls.__name__ for cls in itersubclasses(object)] #doctest: +ELLIPSIS
    ['type', ...'tuple', ...]
    """
    if not isinstance(cls, type):
        raise TypeError('itersubclasses must be called with new-style classes, not %.100r' % cls)
    else:
        if _seen is None:
            _seen = set()
        try:
            subs = cls.__subclasses__()
        except TypeError:
            subs = cls.__subclasses__(cls)

    for sub in subs:
        if sub not in _seen:
            _seen.add(sub)
            yield sub
            for inner_sub in itersubclasses(sub, _seen):
                yield inner_sub


def normalize_whitespace(s):
    """
    Strips the string and replace all whitespace sequences and other non-printable characters with a single space.
    """
    assert isinstance(s, str)
    return re.sub('[\\x00-\\x20\\s]+', ' ', s.strip())


def normalize_lines(s):
    assert isinstance(s, str)
    s2 = re.sub('[\\t ]*\\n[\\t ]*', '\n', s.strip())
    return re.sub('[\\t ]+', ' ', s2)


def _synapse_error_msg(ex):
    """
    Format a human readable error message
    """
    if isinstance(ex, str):
        return ex
    else:
        return '\n' + ex.__class__.__name__ + ': ' + str(ex) + '\n\n'


def _limit_and_offset(uri, limit=None, offset=None):
    """
    Set limit and/or offset query parameters of the given URI.
    """
    parts = urllib_parse.urlparse(uri)
    query = urllib_parse.parse_qs(parts.query)
    if limit is None:
        query.pop('limit', None)
    else:
        query['limit'] = limit
    if offset is None:
        query.pop('offset', None)
    else:
        query['offset'] = offset
    new_query_string = urllib_parse.urlencode(query, doseq=True)
    return urllib_parse.urlunparse(urllib_parse.ParseResult(scheme=(parts.scheme),
      netloc=(parts.netloc),
      path=(parts.path),
      params=(parts.params),
      query=new_query_string,
      fragment=(parts.fragment)))


def query_limit_and_offset(query, hard_limit=1000):
    """
    Extract limit and offset from the end of a query string.

    :returns:   A triple containing the query with limit and offset removed, the limit at most equal to the hard_limit,
                and the offset which
                defaults to 1
    """
    tempQueryStr = query.lower()
    regex = '\\A(.*\\s)(offset|limit)\\s*(\\d*\\s*)\\Z'
    match = re.search(regex, tempQueryStr)
    options = {}
    while match is not None:
        options[match.group(2)] = int(match.group(3))
        tempQueryStr = match.group(1)
        match = re.search(regex, tempQueryStr)

    query = query[:len(tempQueryStr)].strip()
    limit = min(options.get('limit', hard_limit), hard_limit)
    offset = options.get('offset', 1)
    return (
     query, limit, offset)


def extract_synapse_id_from_query(query):
    """
    An unfortunate hack to pull the synapse ID out of a table query of the form "select column1, column2 from syn12345
    where...." needed to build URLs for table services.
    """
    m = re.search('from\\s+(syn\\d+)', query, re.IGNORECASE)
    if m:
        return m.group(1)
    raise ValueError('Couldn\'t extract synapse ID from query: "%s"' % query)


def memoize(obj):
    cache = obj._memoize_cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        refresh = kwargs.pop('refresh', False)
        key = str(args) + str(kwargs)
        if refresh or key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


def printTransferProgress(transferred, toBeTransferred, prefix='', postfix='', isBytes=True, dt=None, previouslyTransferred=0):
    """Prints a progress bar

    :param transferred:             a number of items/bytes completed
    :param toBeTransferred:         total number of items/bytes when completed
    :param prefix:                  String printed before progress bar
    :param postfix:                 String printed after progress bar
    :param isBytes:                 A boolean indicating whether to convert bytes to kB, MB, GB etc.
    :param dt:                      The time in seconds that has passed since transfer started is used to calculate rate
    :param previouslyTransferred:   the number of bytes that were already transferred before this transfer began
                                    (e.g. someone ctrl+c'd out of an upload and restarted it later)

    """
    if not sys.stdout.isatty():
        return
    else:
        barLength = 20
        status = ''
        rate = ''
        if dt is not None:
            if dt != 0:
                rate = (transferred - previouslyTransferred) / float(dt)
                rate = '(%s/s)' % humanizeBytes(rate) if isBytes else rate
        if toBeTransferred < 0:
            defaultToBeTransferred = barLength * 1 * MB
            if transferred > defaultToBeTransferred:
                progress = float(transferred % defaultToBeTransferred) / defaultToBeTransferred
            else:
                progress = float(transferred) / defaultToBeTransferred
        else:
            if toBeTransferred == 0:
                progress = 1
                status = 'Done...\n'
            else:
                progress = float(transferred) / toBeTransferred
        if progress >= 1:
            progress = 1
            status = 'Done...\n'
        block = int(round(barLength * progress))
        nbytes = humanizeBytes(transferred) if isBytes else transferred
        if toBeTransferred > 0:
            outOf = '/%s' % (humanizeBytes(toBeTransferred) if isBytes else toBeTransferred)
            percentage = '%4.2f%%' % (progress * 100)
        else:
            outOf = ''
        percentage = ''
    text = '\r%s [%s]%s   %s%s %s %s %s    ' % (prefix,
     '#' * block + '-' * (barLength - block),
     percentage,
     nbytes, outOf, rate,
     postfix, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def humanizeBytes(bytes):
    bytes = float(bytes)
    units = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB', 'EB']
    for i, unit in enumerate(units):
        if bytes < 1024:
            return '%3.1f%s' % (bytes, units[i])
        bytes /= 1024

    return 'Oops larger than Exabytes'


def touch(path, times=None):
    """
    Make sure a file exists. Update its access and modified times.
    """
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        try:
            os.makedirs(basedir)
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise

    with open(path, 'a'):
        os.utime(path, times)
    return path


def is_json(content_type):
    """detect if a content-type is JSON"""
    if content_type:
        return content_type.lower().strip().startswith('application/json')
    else:
        return False


def find_data_file_handle(bundle):
    """Return the fileHandle whose ID matches the dataFileHandleId in an entity bundle"""
    for fileHandle in bundle['fileHandles']:
        if fileHandle['id'] == bundle['entity']['dataFileHandleId']:
            return fileHandle


def unique_filename(path):
    """Returns a unique path by appending (n) for some number n to the end of the filename."""
    base, ext = os.path.splitext(path)
    counter = 0
    while os.path.exists(path):
        counter += 1
        path = base + '(%d)' % counter + ext

    return path


class threadsafe_iter:
    __doc__ = 'Takes an iterator/generator and makes it thread-safe by serializing call to the `next` method of given\n    iterator/generator.\n    See: http://anandology.com/blog/using-iterators-and-generators/\n    '

    def __init__(self, it):
        self.it = it
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return next(self.it)


def threadsafe_generator(f):
    """A decorator that takes a generator function and makes it thread-safe.
    See: http://anandology.com/blog/using-iterators-and-generators/
    """

    def g(*a, **kw):
        return threadsafe_iter(f(*a, **kw))

    return g


def extract_prefix(keys):
    """
    Takes a list of strings and extracts a common prefix delimited by a dot,
    for example::
        extract_prefix(["entity.bang", "entity.bar", "entity.bat"])
    entity.
    """
    prefixes = set()
    for key in keys:
        parts = key.split('.')
        if len(parts) > 1:
            prefixes.add(parts[0])
        else:
            return ''

    if len(prefixes) == 1:
        return prefixes.pop() + '.'
    else:
        return ''


def temp_download_filename(destination, file_handle_id):
    suffix = 'synapse_download_' + (str(file_handle_id) if file_handle_id else str(uuid.uuid4()))
    if os.path.isdir(destination):
        return os.path.join(destination, suffix)
    else:
        return destination + '.' + suffix


def extract_zip_file_to_directory(zip_file, zip_entry_name, target_dir):
    """
    Extracts a specified file in a zip to the specified directory
    :param zip_file:        an opened zip file. e.g. "with zipfile.ZipFile(zipfilepath) as zip_file:"
    :param zip_entry_name:  the name of the file to be extracted from the zip e.g. folderInsideZipIfAny/fileName.txt
    :param target_dir:      the directory to which the file will be extracted

    :return: full path to the extracted file
    """
    file_base_name = os.path.basename(zip_entry_name)
    filepath = os.path.join(target_dir, file_base_name)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    with open(filepath, 'wb') as (cache_file):
        cache_file.write(zip_file.read(zip_entry_name))
    return filepath


def is_integer(x):
    try:
        return float.is_integer(x)
    except TypeError:
        try:
            int(x)
            return True
        except (ValueError, TypeError):
            return False


def topolgical_sort(graph):
    """Given a graph in the form of a dictionary returns a sorted list

    Adapted from: http://blog.jupo.org/2012/04/06/topological-sorting-acyclic-directed-graphs/
    
    :param graph: a dictionary with values containing lists of keys referencing back into the dictionary

    :returns: sorted list of items
    """
    graph_unsorted = graph.copy()
    graph_sorted = []
    while graph_unsorted:
        acyclic = False
        for node, edges in list(graph_unsorted.items()):
            for edge in edges:
                if edge in graph_unsorted:
                    break
            else:
                acyclic = True
                del graph_unsorted[node]
                graph_sorted.append((node, edges))

        if not acyclic:
            raise RuntimeError('A cyclic dependency occurred. Some files in provenance reference each other circularly.')

    return graph_sorted


def caller_module_name(current_frame):
    """
    :param current_frame: use inspect.currentframe().
    :return: the name of the module calling the function, foo(), in which this calling_module() is invoked.
     Ignores callers that belong in the same module as foo()
    """
    current_frame_filename = current_frame.f_code.co_filename
    caller_frame = current_frame.f_back
    caller_filename = caller_frame.f_code.co_filename
    while caller_filename == current_frame_filename:
        caller_frame = caller_frame.f_back
        caller_filename = caller_frame.f_code.co_filename

    return inspect.getmodulename(caller_filename)


def attempt_import(module_name, fail_message):
    try:
        return importlib.import_module(module_name)
    except ImportError:
        sys.stderr.write(fail_message + "To install this library on Mac or Linux distributions:\n    (sudo) pip install %s\n\nOn Windows, right click the Command Prompt(cmd.exe) and select 'Run as administrator' then:\n    pip install %s\n\n\n\n\n" % (
         module_name, module_name))
        raise


def require_param(param, name):
    if param is None:
        raise ValueError('%s parameter is required.' % name)