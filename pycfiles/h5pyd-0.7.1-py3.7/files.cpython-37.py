# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/h5pyd/_hl/files.py
# Compiled at: 2020-02-06 09:56:32
# Size of source mod 2**32: 15971 bytes
from __future__ import absolute_import
import os, time, json
from .objectid import GroupID
from .group import Group
from .httpconn import HttpConn
from .config import Config
VERBOSE_REFRESH_TIME = 1.0

class File(Group):
    __doc__ = '\n        Represents an HDF5 file.\n    '

    @property
    def attrs(self):
        """ Attributes attached to this object """
        from . import attrs
        return attrs.AttributeManager(self)

    @property
    def filename(self):
        """File name on disk"""
        return self.id.http_conn.domain

    @property
    def driver(self):
        return 'rest_driver'

    @property
    def mode(self):
        """ Python mode used to open file """
        return self.id.http_conn.mode

    @property
    def fid(self):
        """File ID (backwards compatibility) """
        return self.id.domain

    @property
    def libver(self):
        """File format version bounds (2-tuple: low, high)"""
        return ('0.0.1', )

    @property
    def serverver(self):
        return self._version

    @property
    def userblock_size(self):
        """ User block size (in bytes) """
        return 0

    @property
    def created(self):
        """Creation time of the domain"""
        return self.id.http_conn.created

    @property
    def owner(self):
        """Username of the owner of the domain"""
        return self.id.http_conn.owner

    @property
    def limits(self):
        return self._limits

    def __init__(self, domain, mode=None, endpoint=None, username=None, password=None, bucket=None, api_key=None, use_session=True, use_cache=True, logger=None, owner=None, linked_domain=None, retries=3, **kwds):
        """Create a new file object.

        See the h5py user guide for a detailed explanation of the options.

        domain
            URI of the domain name to access. E.g.: tall.data.hdfgroup.org.
        mode
            Access mode: 'r', 'r+', 'w', or 'a'
        endpoint
            Server endpoint.   Defaults to "http://localhost:5000"
        linked_domain
            Create new domain using the root of the linked domain
        """
        groupid = None
        if mode is None and endpoint is None and username is None and password is None and isinstance(domain, GroupID):
            groupid = domain
        else:
            if mode:
                if mode not in ('r', 'r+', 'w', 'w-', 'x', 'a'):
                    raise ValueError('Invalid mode; must be one of r, r+, w, w-, x, a')
                else:
                    if mode is None:
                        mode = 'r'
                    else:
                        cfg = Config()
                        for protocol in ('http://', 'https://', 'hdf5://'):
                            if domain.startswith(protocol):
                                if protocol.startswith('http'):
                                    domain = domain[len(protocol):]
                                    n = domain.find('/')
                                    if n < 0:
                                        raise IOError(400, 'invalid url format')
                                    endpoint = protocol + domain[:n]
                                    domain = domain[n:]
                                    break
                                else:
                                    domain = domain[len(protocol) - 1:]

                        if domain.find('/') > 0:
                            raise IOError(400, 'relative paths or not valid')
                        if endpoint is None:
                            if 'H5SERV_ENDPOINT' in os.environ:
                                endpoint = os.environ['H5SERV_ENDPOINT']
                            else:
                                if 'hs_endpoint' in cfg:
                                    endpoint = cfg['hs_endpoint']
                        if username is None:
                            if 'H5SERV_USERNAME' in os.environ:
                                username = os.environ['H5SERV_USERNAME']
                            else:
                                if 'hs_username' in cfg:
                                    username = cfg['hs_username']
                        if password is None:
                            if 'H5SERV_PASSWORD' in os.environ:
                                password = os.environ['H5SERV_PASSWORD']
                            else:
                                if 'hs_password' in cfg:
                                    password = cfg['hs_password']
                        if bucket is None:
                            if 'HS_BUCKET' in os.environ:
                                bucket = os.environ['HS_BUCKET']
                            else:
                                if 'hs_bucket' in cfg:
                                    bucket = cfg['hs_bucket']
                        if api_key is None:
                            if 'HS_API_KEY' in os.environ:
                                api_key = os.environ['HS_API_KEY']
                            else:
                                if 'hs_api_key' in cfg:
                                    api_key = cfg['hs_api_key']
                        http_conn = HttpConn(domain, endpoint=endpoint, username=username,
                          password=password,
                          bucket=bucket,
                          mode=mode,
                          api_key=api_key,
                          use_session=use_session,
                          use_cache=use_cache,
                          logger=logger,
                          retries=retries)
                        root_json = None
                        req = '/'
                        params = {}
                        if use_cache:
                            if mode == 'r':
                                params['getobjs'] = 'T'
                                params['include_attrs'] = 'T'
                        if bucket:
                            params['bucket'] = bucket
                        rsp = http_conn.GET(req, params=params)
                        if rsp.status_code == 200:
                            root_json = json.loads(rsp.text)
                        if rsp.status_code != 200:
                            if mode in ('r', 'r+'):
                                http_conn.close()
                                raise IOError(rsp.status_code, rsp.reason)
                        if rsp.status_code == 200:
                            if mode in ('w-', 'x'):
                                http_conn.close()
                                raise IOError(409, 'domain already exists')
                        if rsp.status_code == 200 and mode == 'w':
                            rsp = http_conn.DELETE(req, params=params)
                            if rsp.status_code != 200:
                                http_conn.close()
                                raise IOError(rsp.status_code, rsp.reason)
                            root_json = None
                    if root_json:
                        if 'root' not in root_json:
                            http_conn.close()
                            raise IOError(404, 'Location is a folder, not a file')
                        else:
                            if root_json is None:
                                if mode not in ('w', 'a', 'x'):
                                    http_conn.close()
                                    raise IOError(404, 'File not found')
                                body = {}
                                if owner:
                                    body['owner'] = owner
                                if linked_domain:
                                    body['linked_domain'] = linked_domain
                                rsp = http_conn.PUT(req, body=body)
                                if rsp.status_code != 201:
                                    http_conn.close()
                                    raise IOError(rsp.status_code, rsp.reason)
                                root_json = json.loads(rsp.text)
                            if 'root' not in root_json:
                                http_conn.close()
                                raise IOError(404, 'Unexpected error')
                            root_uuid = root_json['root']
                            if 'limits' in root_json:
                                self._limits = root_json['limits']
                            else:
                                self._limits = None
                        if 'version' in root_json:
                            self._version = root_json['version']
                    else:
                        self._version = None
                if mode == 'a':
                    for name in (username, 'default'):
                        if not username:
                            continue
                        req = '/acls/' + name
                        rsp = http_conn.GET(req)
                        if rsp.status_code == 200:
                            rspJson = json.loads(rsp.text)
                            domain_acl = rspJson['acl']
                            if not domain_acl['update']:
                                http_conn.close()
                                raise IOError(403, 'Forbidden')
                            else:
                                break

                if mode in ('w', 'w-', 'x', 'a'):
                    http_conn._mode = 'r+'
            else:
                group_json = None
                if 'domain_objs' in root_json:
                    if mode == 'r':
                        objdb = root_json['domain_objs']
                        http_conn._objdb = objdb
                        if root_uuid in objdb:
                            group_json = objdb[root_uuid]
                req = group_json or '/groups/' + root_uuid
                rsp = http_conn.GET(req)
                if rsp.status_code != 200:
                    http_conn.close()
                    raise IOError(rsp.status_code, 'Unexpected Error')
                group_json = json.loads(rsp.text)
            groupid = GroupID(None, group_json, http_conn=http_conn)
        self._name = '/'
        self._id = groupid
        self._verboseInfo = None
        self._verboseUpdated = None
        Group.__init__(self, self._id)

    def _getVerboseInfo(self):
        now = time.time()
        if self._verboseUpdated is None or now - self._verboseUpdated > VERBOSE_REFRESH_TIME:
            req = '/?verbose=1'
            rsp_json = self.GET(req)
            self.log.debug('get verbose info: {}'.format(rsp_json))
            props = {}
            for k in ('num_objects', 'num_datatypes', 'num_groups', 'num_datasets',
                      'allocated_bytes', 'total_size', 'lastModified'):
                if k in rsp_json:
                    props[k] = rsp_json[k]

            self._verboseInfo = props
            self._verboseUpdated = now
        return self._verboseInfo

    @property
    def modified(self):
        """Last modified time of the domain as a datetime object."""
        props = self._getVerboseInfo()
        modified = self.id.http_conn.modified
        if 'lastModified' in props:
            modified = props['lastModified']
        return modified

    @property
    def num_objects(self):
        props = self._getVerboseInfo()
        num_objects = 0
        if 'num_objects' in props:
            num_objects = props['num_objects']
        return num_objects

    @property
    def num_datatypes(self):
        props = self._getVerboseInfo()
        num_datatypes = 0
        if 'num_datatypes' in props:
            num_datatypes = props['num_datatypes']
        return num_datatypes

    @property
    def num_groups(self):
        props = self._getVerboseInfo()
        num_groups = 0
        if 'num_groups' in props:
            num_groups = props['num_groups']
        return num_groups

    @property
    def num_datasets(self):
        props = self._getVerboseInfo()
        num_datasets = 0
        if 'num_datasets' in props:
            num_datasets = props['num_datasets']
        return num_datasets

    @property
    def allocated_bytes(self):
        props = self._getVerboseInfo()
        allocated_bytes = 0
        if 'allocated_bytes' in props:
            allocated_bytes = props['allocated_bytes']
        return allocated_bytes

    @property
    def total_size(self):
        props = self._getVerboseInfo()
        total_size = 0
        if 'total_size' in props:
            total_size = props['total_size']
        return total_size

    def getACL(self, username):
        req = '/acls/' + username
        rsp_json = self.GET(req)
        acl_json = rsp_json['acl']
        return acl_json

    def getACLs(self):
        req = '/acls'
        rsp_json = self.GET(req)
        acls_json = rsp_json['acls']
        return acls_json

    def putACL(self, acl):
        if 'userName' not in acl:
            raise IOError(404, "ACL has no 'userName' key")
        perm = {}
        for k in ('create', 'read', 'update', 'delete', 'readACL', 'updateACL'):
            if k not in acl:
                raise IOError(404, 'Missing ACL field: {}'.format(k))
            perm[k] = acl[k]

        req = '/acls/' + acl['userName']
        self.PUT(req, body=perm)

    def flush(self):
        """  Tells the service to complete any pending updates to permanent storage
        """
        self.log.debug('flush')
        if self._id.id.startswith('g-'):
            self.log.debug('sending PUT flush request')
            req = '/'
            body = {'flush': 1}
            self.PUT(req, body=body)

    def close(self):
        """ Clears reference to remote resource.
        """
        self.log.debug('close, mode: {}'.format(self.mode))
        if self.mode == 'r+':
            if self._id.id.startswith('g-'):
                self.log.debug('sending PUT flush request')
                req = '/'
                body = {'flush': 1}
                self.PUT(req, body=body)
        if self._id._http_conn:
            self._id._http_conn.close()
        self._id.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.id:
            self.close()

    def __repr__(self):
        if not self.id:
            r = '<Closed HDF5 file>'
        else:
            filename = self.filename
            if isinstance(filename, bytes):
                filename = filename.decode('utf8', 'replace')
            full_path = os.path.basename(filename)
            r = f'<HDF5 file "{full_path}" (mode {self.mode})>'
        return r