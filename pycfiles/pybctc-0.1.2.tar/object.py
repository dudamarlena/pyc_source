# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\yanglin\test/..\pybcs\object.py
# Compiled at: 2012-03-18 20:38:22
import os, common
from httpc import *

class NameException(Exception):

    def __init__(self, msg=None):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return 'NameExecption: ' + str(self.msg)


class Object:

    def __init__(self, bucket, object_name):
        if object_name[0] != '/':
            raise NameException('object name must start with "/"')
        self.bcs = bucket.bcs
        self.bucket = bucket
        self.object_name = object_name
        self.c = self.bcs.c
        self.etag = None
        bcs = bucket.bcs
        bucket_name = bucket.bucket_name
        self.put_url = bcs.sign('PUT', bucket_name, object_name)
        self.post_url = bcs.sign('POST', bucket_name, object_name)
        self.get_url = bcs.sign('GET', bucket_name, object_name)
        self.head_url = bcs.sign('HEAD', bucket_name, object_name)
        self.del_url = bcs.sign('DELETE', bucket_name, object_name)
        return

    def __str__(self):
        return '%s/%s%s' % (self.bcs.host, self.bucket.bucket_name, self.object_name)

    def ref_str(self):
        return '%s/%s%s' % ('bs:/', self.bucket.bucket_name, self.object_name)

    def handle_response(self, r):
        try:
            self.etag = r['header']['etag']
            self.version = r['header']['x-bs-version']
        except:
            pass

        return r

    @network
    def put_file(self, local_file, headers={}):
        if os.path.isdir(local_file):
            raise FileSystemException(local_file + '/ not a file')
        r = self.c.put_file(self.put_url, local_file, headers)
        return self.handle_response(r)

    def put_file_part(self, local_file, start, length, headers={}):
        """ upload part of file, [start, start+length)"""
        if os.path.isdir(local_file):
            raise FileSystemException(local_file + '/ not a file')
        r = self.c.put_file_part(self.put_url, local_file, start, length, headers)
        return self.handle_response(r)

    @network
    def put_file_retain_versions(self, local_file, headers={}):
        if os.path.isdir(local_file):
            raise FileSystemException(local_file + '/ not a file')
        self.put_url += '&x-bs-versioning=1'
        r = self.c.put_file(self.put_url, local_file, headers)
        return self.handle_response(r)

    @network
    def post_file(self, local_file, headers={}):
        if os.path.isdir(local_file):
            raise FileSystemException(local_file + '/ not a file')
        r = self.c.post_file(self.post_url, local_file, headers)
        return self.handle_response(r)

    @network
    def post_file_retain_versions(self, local_file, headers={}):
        if os.path.isdir(local_file):
            raise FileSystemException(local_file + '/ not a file')
        self.post_url += '&x-bs-versioning=1'
        r = self.c.post_file(self.post_url, local_file, headers)
        return self.handle_response(r)

    @network
    def get_to_file(self, local_file, headers={}):
        if os.path.isdir(local_file):
            raise FileSystemException(local_file + '/ not a file')
        r = self.c.get_file(self.get_url, local_file, headers)
        return self.handle_response(r)

    @network
    def get(self, headers={}):
        r = self.c.get(self.get_url, headers)
        return self.handle_response(r)

    @network
    def head(self, headers={}):
        r = self.c.head(self.head_url, headers)
        return self.handle_response(r)

    @network
    def delete(self, headers={}):
        return self.c.delete(self.del_url, headers)

    @network
    def setmeta(self, headers={}):
        return self.copy_to(self, headers)

    @network
    def copy_to(self, dst, headers={}):
        headers.update({'x-bs-copy-source': self.ref_str(), 
           'x-bs-copy-source-directive': 'copy'})
        return self.c.put(dst.put_url, '', headers)

    @network
    def copy_from(self, dst, headers={}):
        headers.update({'x-bs-copy-source': dst.ref_str(), 
           'x-bs-copy-source-directive': 'copy'})
        return self.c.put(self.put_url, '', headers)

    @network
    def set_acl(self, acl, headers={}):
        r = self.c.put(self.put_url + '&acl=1', acl, headers)

    @network
    def get_acl(self, headers={}):
        r = self.c.get(self.get_url + '&acl=1', headers)
        return r

    @network
    def list_versions(self, headers={}):
        r = self.c.get(self.get_url + '&x-bs-versions=1', headers)
        return r

    @network
    def make_public(self):
        acl = '{"statements":[{"action":["*"],"effect":"allow","resource":["%s%s"],"user":["*"]}]}' % (self.bucket.bucket_name, self.object_name)
        self.set_acl(acl)

    @network
    def make_private_to_user(self, user):
        acl = '{"statements":[{"action":["*"],"effect":"allow","resource":["%s%s"],"user":["%s"]}]}' % (self.bucket.bucket_name, self.object_name, user)
        self.set_acl(acl)


class Superfile(Object):

    def __init__(self, bucket, object_name, object_list):
        Object.__init__(self, bucket, object_name)
        self.object_list = object_list

    def assertSubObjectExist(self):
        for o in self.object_list:
            if not o.etag:
                o.head()

    def put(self, headers={}):
        self.assertSubObjectExist()
        tmp_list = [ '"part_%d": {"url": "%s", "etag":"%s"}' % (idx, o.ref_str(), o.etag) for (idx, o) in enumerate(self.object_list)
                   ]
        tmp_list = (',').join(tmp_list)
        self.superfile_meta = '{"object_list": {%s}}' % tmp_list
        url = '%s&superfile=1' % self.put_url
        return self.c.put(url, self.superfile_meta, headers)

    @network
    def put_file(self, local_file, headers={}):
        raise NotImplementException()

    @network
    def put_file_retain_versions(self, local_file, headers={}):
        raise NotImplementException()

    @network
    def post_file(self, local_file, headers={}):
        raise NotImplementException()

    @network
    def post_file_retain_versions(self, local_file, headers={}):
        raise NotImplementException()