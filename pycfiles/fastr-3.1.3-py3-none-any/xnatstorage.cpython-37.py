# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/xnatstorage.py
# Compiled at: 2019-10-16 04:21:09
# Size of source mod 2**32: 28519 bytes
"""
This module contains the XNATStorage plugin for fastr
"""
import fnmatch, netrc, os, re, time, tempfile, urllib.parse
from collections import OrderedDict
import requests
from requests.exceptions import RequestException
import xnat, xnat.exceptions, fastr, fastr.data
from fastr import exceptions
from fastr.core.ioplugin import IOPlugin

class XNATStorage(IOPlugin):
    __doc__ = "\n    .. warning::\n\n        As this IOPlugin is under development, it has not been thoroughly\n        tested.\n\n    The XNATStorage plugin is an IOPlugin that can download data from and\n    upload data to an XNAT server. It uses its own ``xnat://`` URL scheme.\n    This is a scheme specific for this plugin and though it looks somewhat\n    like the XNAT rest interface, a different type or URL.\n\n    Data resources can be access directly by a data url::\n\n        xnat://xnat.example.com/data/archive/projects/sandbox/subjects/subject001/experiments/experiment001/scans/T1/resources/DICOM\n        xnat://xnat.example.com/data/archive/projects/sandbox/subjects/subject001/experiments/*_BRAIN/scans/T1/resources/DICOM\n\n    In the second URL you can see a wildcard being used. This is possible at\n    long as it resolves to exactly one item.\n\n    The ``id`` query element will change the field from the default experiment to\n    subject and the ``label`` query element sets the use of the label as the\n    fastr id (instead of the XNAT id) to ``True`` (the default is ``False``)\n\n    To disable ``https`` transport and use ``http`` instead the query string\n    can be modified to add ``insecure=true``. This will make the plugin send\n    requests over ``http``::\n\n        xnat://xnat.example.com/data/archive/projects/sandbox/subjects/subject001/experiments/*_BRAIN/scans/T1/resources/DICOM?insecure=true\n\n    For sinks it is import to know where to save the data. Sometimes you want\n    to save data in a new assessor/resource and it needs to be created. To\n    allow the Fastr sink to create an object in XNAT, you have to supply the\n    type as a query parameter::\n\n        xnat://xnat.bmia.nl/data/archive/projects/sandbox/subjects/S01/experiments/_BRAIN/assessors/test_assessor/resources/IMAGE/files/image.nii.gz?resource_type=xnat:resourceCatalog&assessor_type=xnat:qcAssessmentData\n\n    Valid options are: subject_type, experiment_type, assessor_type, scan_type,\n    and resource_type.\n\n    If you want to do a search where\n    multiple resources are returned, it is possible to use a search url::\n\n        xnat://xnat.example.com/search?projects=sandbox&subjects=subject[0-9][0-9][0-9]&experiments=*_BRAIN&scans=T1&resources=DICOM\n\n    This will return all DICOMs for the T1 scans for experiments that end with _BRAIN that belong to a\n    subjectXXX where XXX is a 3 digit number. By default the ID for the samples\n    will be the experiment XNAT ID (e.g. XNAT_E00123). The wildcards that can\n    be the used are the same UNIX shell-style wildcards as provided by the\n    module :py:mod:`fnmatch`.\n\n    It is possible to change the id to a different fields id or label. Valid\n    fields are project, subject, experiment, scan, and resource::\n\n        xnat://xnat.example.com/search?projects=sandbox&subjects=subject[0-9][0-9][0-9]&experiments=*_BRAIN&scans=T1&resources=DICOM&id=subject&label=true\n\n    The following variables can be set in the search query:\n\n    ============= ============== =============================================================================================\n    variable      default        usage\n    ============= ============== =============================================================================================\n    projects      ``*``          The project(s) to select, can contain wildcards (see :py:mod:`fnmatch`)\n    subjects      ``*``          The subject(s) to select, can contain wildcards (see :py:mod:`fnmatch`)\n    experiments   ``*``          The experiment(s) to select, can contain wildcards (see :py:mod:`fnmatch`)\n    scans         ``*``          The scan(s) to select, can contain wildcards (see :py:mod:`fnmatch`)\n    resources     ``*``          The resource(s) to select, can contain wildcards (see :py:mod:`fnmatch`)\n    id            ``experiment`` What field to use a the id, can be: project, subject, experiment, scan, or resource\n    label         ``false``      Indicate the XNAT label should be used as fastr id, options ``true`` or ``false``\n    insecure      ``false``      Change the url scheme to be used to http instead of https\n    verify        ``true``       (Dis)able the verification of SSL certificates\n    regex         ``false``      Change search to use regex :py:func:`re.match` instead of fnmatch for matching\n    overwrite     ``false``      Tell XNAT to overwrite existing files if a file with the name is already present\n    ============= ============== =============================================================================================\n\n    For storing credentials the ``.netrc`` file can be used. This is a common\n    way to store credentials on UNIX systems. It is required that the file is\n    only accessible by the owner only or a ``NetrcParseError`` will be raised.\n    A netrc file is really easy to create, as its entries look like::\n\n        machine xnat.example.com\n                login username\n                password secret123\n\n    See the :py:mod:`netrc module <netrc>` or the\n    `GNU inet utils website <http://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html#The-_002enetrc-file>`_\n    for more information about the ``.netrc`` file.\n\n    .. note::\n\n        On windows the location of the netrc file is assumed to be\n        ``os.path.expanduser('~/_netrc')``. The leading underscore is\n        because windows does not like filename starting with a dot.\n\n    .. note::\n\n        For scan the label will be the scan type (this is initially\n        the same as the series description, but can be updated manually\n        or the XNAT scan type cleanup).\n\n    .. warning::\n\n        labels in XNAT are not guaranteed to be unique, so be careful\n        when using them as the sample ID.\n\n    For background on XNAT, see the\n    `XNAT API DIRECTORY <https://wiki.xnat.org/display/XNAT16/XNAT+REST+API+Directory>`_\n    for the REST API of XNAT.\n    "
    scheme = ('xnat', 'xnat+http', 'xnat+https')

    def __init__(self):
        super(XNATStorage, self).__init__()
        self._xnat = (None, None)

    def cleanup(self):
        if self.xnat is not None:
            fastr.log.info('Attempting to cleanly disconnecting XNAT.')
            self.xnat.disconnect()

    @property
    def server(self):
        return self._xnat[0]

    @property
    def xnat(self):
        return self._xnat[1]

    def connect(self, server, path='', insecure=False, verify=True):
        if self.server != server:
            if self.xnat is not None:
                self.xnat.disconnect()
            try:
                netrc_file = os.path.join('~', '_netrc' if os.name == 'nt' else '.netrc')
                netrc_file = os.path.expanduser(netrc_file)
                user, _, password = netrc.netrc(netrc_file).authenticators(server)
            except TypeError:
                raise exceptions.FastrValueError('Could not retrieve login info for "{}" from the .netrc file!'.format(server))

            schema = 'http' if insecure else 'https'
            session = xnat.connect((urllib.parse.urlunparse([schema, server, path, '', '', ''])), user=user,
              password=password,
              debug=(fastr.config.debug),
              verify=verify)
            session.request_timeout = 120
            self._xnat = (
             server, session)

    @staticmethod
    def _path_to_dict(path):
        fastr.log.info('Converting {} to dict...'.format(path))
        if not path.startswith('/data/'):
            raise ValueError('Resources to be located should have a path starting with /data/ (found {})'.format(path))
        elif path.startswith('/data/archive/'):
            path_prefix_parts = 2
        else:
            path_prefix_parts = 1
        parts = path.lstrip('/').split('/', 11 + path_prefix_parts)
        path_iterator = parts[path_prefix_parts:].__iter__()
        location = OrderedDict()
        for key, value in zip(path_iterator, path_iterator):
            if key == 'files':
                filepath = [
                 value] + list(path_iterator)
                value = '/'.join(filepath)
            location[key] = value

        fastr.log.info('Found {}'.format(location))
        return location

    def _locate_resource(self, url, create=False, use_regex=False):
        resources = self._find_objects(url=url, create=create, use_regex=use_regex)
        if len(resources) == 0:
            raise ValueError('Could not find data object at {}'.format(url))
        else:
            if len(resources) > 1:
                raise ValueError('Data item does not point to a unique resource! Matches found: {}'.format([x.fulluri for x in resources]))
            else:
                resource = resources[0]
                resource_cls = self.xnat.XNAT_CLASS_LOOKUP['xnat:abstractResource']
                assert isinstance(resource, resource_cls), 'The resource should be an instance of {}'.format(resource_cls)
            return resource

    def parse_uri(self, url):
        url = urllib.parse.urlparse(url)
        if url.scheme not in self.scheme:
            raise exceptions.FastrValueError('URL scheme {} not of supported type {}!'.format(url.scheme, self.scheme))
        query = urllib.parse.parse_qs(url.query)
        path_prefix = url.path[:url.path.find('/data/')]
        url = url._replace(path=(url.path[len(path_prefix):]))
        if not url.path.startswith('/data/archive/'):
            if url.path.startswith('/data/'):
                fastr.log.info('Patching archive into url path starting with data')
                url = url._replace(path=(url.path[:6] + 'archive/' + url.path[6:]))
        url_str = urllib.parse.urlunparse(url)
        fastr.log.info('New URL: {}'.format(url_str))
        if not url.path.startswith('/data/archive'):
            raise exceptions.FastrValueError('Can only fetch urls with the /data/archive path')
        if url.scheme == 'xnat+http':
            insecure = True
        else:
            if url.scheme == 'xnat+https':
                insecure = False
            else:
                fastr.log.warning('Using old-style insecure lookup, please use a xnat+http:// or xnat+https:// url scheme instead!')
                insecure = query.get('insecure', ['0'])[0] in ('true', '1')
        verify = query.get('verify', ['1'])[0] in ('true', '1')
        use_regex = query.get('regex', ['0'])[0] in ('true', '1')
        return (
         url, path_prefix, insecure, verify, use_regex, query)

    def fetch_url(self, inurl, outpath):
        """
        Get the file(s) or values from XNAT.

        :param inurl: url to the item in the data store
        :param outpath: path where to store the fetch data locally
        """
        url, path_prefix, insecure, verify, use_regex, query = self.parse_uri(inurl)
        self.connect((url.netloc), path=path_prefix, insecure=insecure, verify=verify)
        location = self._path_to_dict(url.path)
        filepath = location.get('files', '')
        resource = self._locate_resource(inurl, use_regex=use_regex)
        workdir = outpath
        if not os.path.isdir(workdir):
            directory, filename = os.path.split(workdir)
            workdir = os.path.join(directory, filename.replace('.', '_'))
            os.makedirs(workdir)
        else:
            workdir = tempfile.mkdtemp(prefix=('fastr_xnat_{}_tmp'.format(resource.id)), dir=workdir)
            max_tries = tries = 3
            success = False
            while tries > 0 and not success:
                try:
                    fastr.log.info('Download attempt {} of {}'.format(max_tries - tries + 1, max_tries))
                    tries -= 1
                    resource.download_dir(workdir, verbose=False)
                    success = True
                except requests.exceptions.ChunkedEncodingError:
                    if tries <= 0:
                        raise
                    else:
                        time.sleep((max_tries - tries) * 10)

            resource_label = resource.label.replace(' ', '_')
            if filepath == '':
                filepath = file_name = 'files'
                target = 'resources/{}'.format(resource_label)
            else:
                file_directory, file_name = os.path.split(filepath)
            target = 'resources/{}/files/{}'.format(resource_label, file_directory).rstrip('/')
        for root, dirs, files in os.walk(workdir):
            if root.endswith(target):
                if file_name in files or file_name in dirs:
                    pass
                data_path = os.path.join(root, file_name)
                fastr.log.info('Found data in {}'.format(data_path))
                break
        else:
            message = 'Could not find {} file in downloaded resource!'.format(filepath)
            fastr.log.error(message)
            raise exceptions.FastrValueError(message)

        return data_path

    def put_url(self, inpath, outurl):
        """
        Upload the files to the XNAT storage

        :param inpath: path to the local data
        :param outurl: url to where to store the data in the external data store.
        """
        url, path_prefix, insecure, verify, use_regex, query = self.parse_uri(outurl)
        self.connect((url.netloc), path=path_prefix, insecure=insecure, verify=verify)
        resource = self._locate_resource(outurl, create=True, use_regex=use_regex)
        parsed_url = urllib.parse.urlparse(outurl)
        location = self._path_to_dict(parsed_url.path)
        fastr.log.info('Uploading to: {}'.format(resource.fulluri))
        fastr.log.info('Uploading to path: {}'.format(location['files']))
        try:
            overwrite = urllib.parse.parse_qs(url.query).get('overwrite', ['0'])[0] in ('true',
                                                                                        '1')
            self.upload(resource, inpath, (location['files']), overwrite=overwrite)
            return True
        except xnat.exceptions.XNATUploadError as exception:
            try:
                fastr.log.error('Encountered error when uploading data: {}'.format(exception))
                return False
            finally:
                exception = None
                del exception

    @staticmethod
    def upload(resource, in_path, location, retries=3, overwrite=False):
        success = False
        tries = retries
        file_size = os.path.getsize(in_path)
        with open(in_path, 'rb') as (in_file_handle):
            while not success:
                if tries > 0:
                    tries -= 1
                    try:
                        in_file_handle.seek(0)
                        resource.upload(in_file_handle, location, overwrite=overwrite)
                        success = True
                    except (xnat.exceptions.XNATError, RequestException) as exception:
                        try:
                            fastr.log.warning('Encountered XNAT error during upload: {}'.format(exception))
                            if tries > 0:
                                fastr.log.warning('Retrying {} times'.format(tries))
                        finally:
                            exception = None
                            del exception

            max_retries = retries
            resource.clearcache()
            resource.files.clearcache()
            while location not in resource.files and retries > 0:
                resource.clearcache()
                resource.files.clearcache()
                retries -= 1
                try:
                    in_file_handle.seek(0)
                    resource.upload(in_file_handle, location, overwrite=True)
                except xnat.exceptions.XNATError:
                    delay = 10 * (max_retries - retries)
                    fastr.log.warning('Got exception during upload, sleep {} seconds and retry'.format(delay))
                    time.sleep(delay)

        resource.clearcache()
        resource.files.clearcache()
        if location not in resource.files:
            raise xnat.exceptions.XNATUploadError('Problem with uploading to XNAT (file not found, persisted after retries)')
        else:
            xnat_size = int(resource.files[location].size)
            if xnat_size != file_size:
                raise xnat.exceptions.XNATUploadError('Problem with uploading to XNAT (file size differs uploaded {}, expected {})'.format(xnat_size, file_size))
            else:
                fastr.log.info('It appears the file is uploaded to {} with a file size of {}'.format(resource.files[location].fulluri, xnat_size))

    def _find_objects--- This code section failed: ---

 L. 433         0  LOAD_GLOBAL              fastr
                2  LOAD_ATTR                log
                4  LOAD_METHOD              info
                6  LOAD_STR                 'Locating {}'
                8  LOAD_METHOD              format
               10  LOAD_FAST                'url'
               12  CALL_METHOD_1         1  '1 positional argument'
               14  CALL_METHOD_1         1  '1 positional argument'
               16  POP_TOP          

 L. 435        18  LOAD_GLOBAL              urllib
               20  LOAD_ATTR                parse
               22  LOAD_METHOD              urlparse
               24  LOAD_FAST                'url'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  STORE_FAST               'parsed_url'

 L. 436        30  LOAD_FAST                'parsed_url'
               32  LOAD_ATTR                path
               34  STORE_FAST               'path'

 L. 437        36  LOAD_GLOBAL              urllib
               38  LOAD_ATTR                parse
               40  LOAD_METHOD              parse_qs
               42  LOAD_FAST                'parsed_url'
               44  LOAD_ATTR                query
               46  CALL_METHOD_1         1  '1 positional argument'
               48  STORE_FAST               'query'

 L. 439        50  LOAD_FAST                'path'
               52  LOAD_METHOD              startswith
               54  LOAD_STR                 '/data/'
               56  CALL_METHOD_1         1  '1 positional argument'
               58  POP_JUMP_IF_TRUE     68  'to 68'

 L. 440        60  LOAD_GLOBAL              ValueError
               62  LOAD_STR                 'Resources to be located should have a path starting with /data/'
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  RAISE_VARARGS_1       1  'exception instance'
             68_0  COME_FROM            58  '58'

 L. 443        68  LOAD_FAST                'self'
               70  LOAD_METHOD              _path_to_dict
               72  LOAD_FAST                'path'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               'location'

 L. 445        78  LOAD_STR                 'resources'
               80  LOAD_FAST                'location'
               82  COMPARE_OP               not-in
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L. 446        86  LOAD_GLOBAL              ValueError
               88  LOAD_STR                 'All files should be located inside a resource, did not find resources level in {}'
               90  LOAD_METHOD              format

 L. 447        92  LOAD_FAST                'location'
               94  CALL_METHOD_1         1  '1 positional argument'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  RAISE_VARARGS_1       1  'exception instance'
            100_0  COME_FROM            84  '84'

 L. 451       100  LOAD_STR                 'resources'
              102  LOAD_STR                 'xnat:resourceCatalog'
              104  BUILD_MAP_1           1 
              106  STORE_FAST               'types'

 L. 453       108  SETUP_LOOP          196  'to 196'
              110  LOAD_FAST                'location'
              112  LOAD_METHOD              keys
              114  CALL_METHOD_0         0  '0 positional arguments'
              116  GET_ITER         
            118_0  COME_FROM           174  '174'
              118  FOR_ITER            194  'to 194'
              120  STORE_FAST               'key'

 L. 454       122  LOAD_FAST                'key'
              124  LOAD_METHOD              rstrip
              126  LOAD_STR                 's'
              128  CALL_METHOD_1         1  '1 positional argument'
              130  LOAD_STR                 '_type'
              132  BINARY_ADD       
              134  STORE_FAST               'option1'

 L. 455       136  LOAD_FAST                'key'
              138  LOAD_STR                 '_type'
              140  BINARY_ADD       
              142  STORE_FAST               'option2'

 L. 456       144  LOAD_FAST                'option1'
              146  LOAD_FAST                'query'
              148  COMPARE_OP               in
              150  POP_JUMP_IF_FALSE   168  'to 168'

 L. 457       152  LOAD_FAST                'query'
              154  LOAD_FAST                'option1'
              156  BINARY_SUBSCR    
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  LOAD_FAST                'types'
              164  LOAD_FAST                'key'
              166  STORE_SUBSCR     
            168_0  COME_FROM           150  '150'

 L. 458       168  LOAD_FAST                'option2'
              170  LOAD_FAST                'query'
              172  COMPARE_OP               in
              174  POP_JUMP_IF_FALSE   118  'to 118'

 L. 459       176  LOAD_FAST                'query'
              178  LOAD_FAST                'option2'
              180  BINARY_SUBSCR    
              182  LOAD_CONST               0
              184  BINARY_SUBSCR    
              186  LOAD_FAST                'types'
              188  LOAD_FAST                'key'
              190  STORE_SUBSCR     
              192  JUMP_BACK           118  'to 118'
              194  POP_BLOCK        
            196_0  COME_FROM_LOOP      108  '108'

 L. 461       196  LOAD_CONST               None
              198  STORE_FAST               'items'

 L. 463   200_202  SETUP_LOOP          636  'to 636'
              204  LOAD_FAST                'location'
              206  LOAD_METHOD              items
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  GET_ITER         
          212_214  FOR_ITER            634  'to 634'
              216  UNPACK_SEQUENCE_2     2 
              218  STORE_FAST               'object_type'
              220  STORE_FAST               'object_key'

 L. 466       222  LOAD_FAST                'object_type'
              224  LOAD_STR                 'files'
              226  COMPARE_OP               ==
              228  POP_JUMP_IF_FALSE   232  'to 232'

 L. 467       230  BREAK_LOOP       
            232_0  COME_FROM           228  '228'

 L. 469       232  LOAD_GLOBAL              fastr
              234  LOAD_ATTR                log
              236  LOAD_METHOD              info
              238  LOAD_STR                 'Locating {} / {} in {}'
              240  LOAD_METHOD              format
              242  LOAD_FAST                'object_type'
              244  LOAD_FAST                'object_key'
              246  LOAD_FAST                'items'
              248  CALL_METHOD_3         3  '3 positional arguments'
              250  CALL_METHOD_1         1  '1 positional argument'
              252  POP_TOP          

 L. 470       254  LOAD_FAST                'self'
              256  LOAD_ATTR                _resolve_url_part
              258  LOAD_FAST                'object_type'
              260  LOAD_FAST                'object_key'
              262  LOAD_FAST                'use_regex'
              264  LOAD_FAST                'items'
              266  LOAD_CONST               ('use_regex', 'parents')
              268  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              270  STORE_FAST               'new_items'

 L. 472       272  LOAD_GLOBAL              len
              274  LOAD_FAST                'new_items'
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  LOAD_CONST               0
              280  COMPARE_OP               ==
          282_284  POP_JUMP_IF_FALSE   628  'to 628'

 L. 473       286  LOAD_FAST                'create'
          288_290  POP_JUMP_IF_TRUE    312  'to 312'

 L. 474       292  LOAD_GLOBAL              ValueError
              294  LOAD_STR                 'Could not find data parent_object at {} (No values at level {})'
              296  LOAD_METHOD              format
              298  LOAD_FAST                'url'

 L. 475       300  LOAD_FAST                'object_type'
              302  CALL_METHOD_2         2  '2 positional arguments'
              304  CALL_FUNCTION_1       1  '1 positional argument'
              306  RAISE_VARARGS_1       1  'exception instance'
          308_310  JUMP_FORWARD        628  'to 628'
            312_0  COME_FROM           288  '288'

 L. 476       312  LOAD_FAST                'items'
              314  LOAD_CONST               None
              316  COMPARE_OP               is-not
          318_320  POP_JUMP_IF_FALSE   608  'to 608'
              322  LOAD_GLOBAL              len
              324  LOAD_FAST                'items'
              326  CALL_FUNCTION_1       1  '1 positional argument'
              328  LOAD_CONST               1
              330  COMPARE_OP               ==
          332_334  POP_JUMP_IF_FALSE   608  'to 608'

 L. 477       336  LOAD_GLOBAL              fastr
              338  LOAD_ATTR                log
              340  LOAD_METHOD              debug
              342  LOAD_STR                 'Items: {}'
              344  LOAD_METHOD              format
              346  LOAD_FAST                'items'
              348  CALL_METHOD_1         1  '1 positional argument'
              350  CALL_METHOD_1         1  '1 positional argument'
              352  POP_TOP          

 L. 478       354  LOAD_FAST                'items'
              356  LOAD_CONST               0
              358  BINARY_SUBSCR    
              360  STORE_FAST               'parent_object'

 L. 481       362  LOAD_FAST                'object_type'
              364  LOAD_FAST                'types'
              366  COMPARE_OP               in
          368_370  POP_JUMP_IF_FALSE   382  'to 382'

 L. 482       372  LOAD_FAST                'types'
              374  LOAD_FAST                'object_type'
              376  BINARY_SUBSCR    
              378  STORE_FAST               'xsi_type'
              380  JUMP_FORWARD        398  'to 398'
            382_0  COME_FROM           368  '368'

 L. 484       382  LOAD_GLOBAL              ValueError
              384  LOAD_STR                 'Could not find the correct xsi:type for {} (available hints: {})'
              386  LOAD_METHOD              format
              388  LOAD_FAST                'object_type'

 L. 485       390  LOAD_FAST                'types'
              392  CALL_METHOD_2         2  '2 positional arguments'
              394  CALL_FUNCTION_1       1  '1 positional argument'
              396  RAISE_VARARGS_1       1  'exception instance'
            398_0  COME_FROM           380  '380'

 L. 487       398  LOAD_STR                 '*'
              400  LOAD_FAST                'object_key'
              402  COMPARE_OP               in
          404_406  POP_JUMP_IF_TRUE    438  'to 438'
              408  LOAD_STR                 '?'
              410  LOAD_FAST                'object_key'
              412  COMPARE_OP               in
          414_416  POP_JUMP_IF_TRUE    438  'to 438'
              418  LOAD_STR                 '['
              420  LOAD_FAST                'object_key'
              422  COMPARE_OP               in
          424_426  POP_JUMP_IF_TRUE    438  'to 438'
              428  LOAD_STR                 ']'
              430  LOAD_FAST                'object_key'
              432  COMPARE_OP               in
          434_436  POP_JUMP_IF_FALSE   452  'to 452'
            438_0  COME_FROM           424  '424'
            438_1  COME_FROM           414  '414'
            438_2  COME_FROM           404  '404'

 L. 488       438  LOAD_GLOBAL              ValueError
              440  LOAD_STR                 'Illegal characters found in name of object_key to create! (characters ?*[] or illegal!), found: {}'
              442  LOAD_METHOD              format

 L. 489       444  LOAD_FAST                'object_key'
              446  CALL_METHOD_1         1  '1 positional argument'
              448  CALL_FUNCTION_1       1  '1 positional argument'
              450  RAISE_VARARGS_1       1  'exception instance'
            452_0  COME_FROM           434  '434'

 L. 491       452  LOAD_GLOBAL              fastr
              454  LOAD_ATTR                log
              456  LOAD_METHOD              info
              458  LOAD_STR                 'Creating new object under {} with type {}'
              460  LOAD_METHOD              format
              462  LOAD_FAST                'parent_object'
              464  LOAD_ATTR                uri
              466  LOAD_FAST                'xsi_type'
              468  CALL_METHOD_2         2  '2 positional arguments'
              470  CALL_METHOD_1         1  '1 positional argument'
              472  POP_TOP          

 L. 494       474  LOAD_FAST                'self'
              476  LOAD_ATTR                xnat
              478  LOAD_ATTR                XNAT_CLASS_LOOKUP
              480  LOAD_FAST                'xsi_type'
              482  BINARY_SUBSCR    
              484  STORE_FAST               'cls'

 L. 495       486  LOAD_FAST                'cls'
              488  LOAD_ATTR                SECONDARY_LOOKUP_FIELD
              490  LOAD_FAST                'object_key'
              492  BUILD_MAP_1           1 
              494  STORE_FAST               'kwargs'

 L. 496       496  SETUP_EXCEPT        520  'to 520'

 L. 497       498  LOAD_FAST                'cls'
              500  BUILD_TUPLE_0         0 
              502  LOAD_STR                 'parent'
              504  LOAD_FAST                'parent_object'
              506  BUILD_MAP_1           1 
              508  LOAD_FAST                'kwargs'
              510  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              512  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              514  POP_TOP          
              516  POP_BLOCK        
              518  JUMP_FORWARD        566  'to 566'
            520_0  COME_FROM_EXCEPT    496  '496'

 L. 498       520  DUP_TOP          
              522  LOAD_GLOBAL              xnat
              524  LOAD_ATTR                exceptions
              526  LOAD_ATTR                XNATResponseError
              528  COMPARE_OP               exception-match
          530_532  POP_JUMP_IF_FALSE   564  'to 564'
              534  POP_TOP          
              536  POP_TOP          
              538  POP_TOP          

 L. 499       540  LOAD_GLOBAL              fastr
              542  LOAD_ATTR                log
              544  LOAD_METHOD              warning
              546  LOAD_STR                 'Got a response error when creating the object {} (parent {}), continuing to check if creating was in a race condition and another processed created it'
              548  LOAD_METHOD              format

 L. 502       550  LOAD_FAST                'object_key'

 L. 503       552  LOAD_FAST                'parent_object'
              554  CALL_METHOD_2         2  '2 positional arguments'
              556  CALL_METHOD_1         1  '1 positional argument'
              558  POP_TOP          
              560  POP_EXCEPT       
              562  JUMP_FORWARD        566  'to 566'
            564_0  COME_FROM           530  '530'
              564  END_FINALLY      
            566_0  COME_FROM           562  '562'
            566_1  COME_FROM           518  '518'

 L. 506       566  LOAD_FAST                'self'
              568  LOAD_ATTR                _resolve_url_part
              570  LOAD_FAST                'object_type'
              572  LOAD_FAST                'object_key'
              574  LOAD_FAST                'use_regex'
              576  LOAD_FAST                'items'
              578  LOAD_CONST               ('use_regex', 'parents')
              580  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              582  STORE_FAST               'new_items'

 L. 508       584  LOAD_GLOBAL              len
              586  LOAD_FAST                'new_items'
              588  CALL_FUNCTION_1       1  '1 positional argument'
              590  LOAD_CONST               1
              592  COMPARE_OP               !=
          594_596  POP_JUMP_IF_FALSE   628  'to 628'

 L. 509       598  LOAD_GLOBAL              ValueError
              600  LOAD_STR                 'There appears to be a problem creating the object_key!'
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  RAISE_VARARGS_1       1  'exception instance'
              606  JUMP_FORWARD        628  'to 628'
            608_0  COME_FROM           332  '332'
            608_1  COME_FROM           318  '318'

 L. 511       608  LOAD_GLOBAL              ValueError
              610  LOAD_STR                 'To create an object, the path should point to a unique parent object! Found {} matching items: {}'
              612  LOAD_METHOD              format

 L. 512       614  LOAD_GLOBAL              len
              616  LOAD_FAST                'items'
              618  CALL_FUNCTION_1       1  '1 positional argument'
              620  LOAD_FAST                'items'
              622  CALL_METHOD_2         2  '2 positional arguments'
              624  CALL_FUNCTION_1       1  '1 positional argument'
              626  RAISE_VARARGS_1       1  'exception instance'
            628_0  COME_FROM           606  '606'
            628_1  COME_FROM           594  '594'
            628_2  COME_FROM           308  '308'
            628_3  COME_FROM           282  '282'

 L. 514       628  LOAD_FAST                'new_items'
              630  STORE_FAST               'items'
              632  JUMP_BACK           212  'to 212'
              634  POP_BLOCK        
            636_0  COME_FROM_LOOP      200  '200'

 L. 516       636  LOAD_FAST                'items'
              638  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 452_0

    def _resolve_url_part(self, level, query=None, use_regex=False, parents=None):
        """
        Get all matching projects

        :param dict query: the query to find projects to match for
        :return:
        """
        if parents is None:
            parents = [
             self.xnat]
        if query is None:
            query = '.*' if use_regex else '*'
        fastr.log.info('Find {}: {} (parents: {})'.formatlevelqueryparents)
        objects = []
        for parent in parents:
            extra_options = getattr(parent, level)
            if use_regex:
                objects.extend((x for x in extra_options.values() if re.match(query, getattr(x, extra_options.secondary_lookup_field)) or x.id == query))
            elif all((x not in query for x in '*?[]')):
                if query in extra_options:
                    objects.append(extra_options[query])
            else:
                objects.extend((x for x in extra_options.values() if fnmatch.fnmatchcase(getattr(x, extra_options.secondary_lookup_field), query) or x.id == query))

        fastr.log.info('Found: {}'.format(objects))
        return objects

    def expand_url(self, url):
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.path == '/search':
            query = urllib.parse.parse_qs(parsed_url.query)
            valid_fields = ('projects', 'subjects', 'experiments', 'scans', 'resources',
                            'id', 'label', 'insecure', 'verify', 'regex')
            valid_query = True
            for key in query.keys():
                if key not in valid_fields:
                    fastr.log.error('Using invalid query field {} options are {}!'.format(key, valid_fields))
                    valid_query = False

            if not valid_query:
                raise ValueError('The query was malformed, see the error log for details.')
            id_field = query.get('id', ['experiment'])[0]
            id_use_label = query.get('label', ['0'])[0].lower() in ('1', 'true')
            use_regex = query.get('regex', ['0'])[0].lower() in ('1', 'true')
            insecure = query.get('insecure', ['0'])[0] in ('true', '1')
            verify = query.get('verify', ['1'])[0] in ('true', '1')
            self.connect((parsed_url.netloc), insecure=insecure, verify=verify)
            if id_field not in ('project', 'subject', 'experiment', 'scan', 'resource'):
                raise exceptions.FastrValueError('Requested id field ({}) is not a valid option!'.format(id_field))
            default = ['.*'] if use_regex else ['*']
            search_path = '/data/archive/projects/{p}/subjects/{s}/experiments/{e}/scans/{sc}/resources/{r}'.format(p=(query.get('projects', default)[0]),
              s=(query.get('subjects', default)[0]),
              e=(query.get('experiments', default)[0]),
              sc=(query.get('scans', default)[0]),
              r=(query.get('resources', default)[0]))
            resources = self._find_objects(search_path, use_regex=use_regex)
            urls = []
            for resource in resources:
                match = re.match('/data/experiments/(?P<experiment>[a-zA-Z0-9_\\-]+)/scans/(?P<scan>[a-zA-Z0-9_\\-]+)/resources/(?P<resource>[a-zA-Z0-9_\\-]+)', resource.uri)
                experiment = self.xnat.experiments[match.group('experiment')]
                project = self.xnat.projects[experiment.project]
                subject = self.xnat.subjects[experiment.subject_id]
                scan = experiment.scans[match.group('scan')]
                newpath = '/data/archive/projects/{}/subjects/{}/experiments/{}/scans/{}/resources/{}/files/{}'.format(project.id, subject.id, experiment.id, scan.id, resource.id, query.get('files', [''])[0])
                newurl = urllib.parse.urlunparse(('xnat', parsed_url.netloc, newpath, parsed_url.params, '', ''))
                if id_field == 'resource':
                    id_obj = resource
                else:
                    if id_field == 'scan':
                        id_obj = scan
                    else:
                        if id_field == 'experiment':
                            id_obj = experiment
                        else:
                            if id_field == 'subject':
                                id_obj = subject
                            else:
                                id_obj = project
                if id_use_label:
                    id_ = id_obj.label
                else:
                    id_ = id_obj.id
                urls.append((id_, newurl))

            return tuple(urls)
        return url