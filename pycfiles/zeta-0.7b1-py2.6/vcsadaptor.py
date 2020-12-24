# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/lib/vcsadaptor.py
# Compiled at: 2010-06-12 03:35:53
"""Vcs adaptor pattern.

API definition for extension module implementing the respository access.

`vcs` attributes,
      url
      type.vcs_typename
      loginname
      password

init( vcs )
  Return the client object.

info( self, url=None, revno=None )
  self  - can be VcsRepository() or VcsFile() but contains `client` attribute.
  url   - info about url
  revno - Revision for which the file's info in required

  If url==None,
    Return the information about the repository
        { 'l_revision' : rev , 'l_author' : auth, 'l_date' : date }
  Else,
    Return the info tuple for the url
        { 'l_revision' : rev , 'l_author' : auth, 'l_date' : date, 
          'mime_type': mime_type, 'size': size, 'repos_path': repos_path }

list( self, url_dir, revno=None, recurse=False )
  self    - VcsRepository() and contains `client` attribute.
  url_dir - file url (directory) for which the content is required.
  revno   - Revision for which the listing is required.
  recurse - True, will list all the files/directories under 'url_dir'

  Return directory listing, as a list of tuple of,
      [ mod_revision, mime_type, url, author, size, timestamp, repo_path ]

cat( self, url, revno=None, annotate=False )
  url      - file url for which the content is required.
  revno    - revision for which the file content is required.
  annotate - if annotate is False, then,
                revision, author, timestamp
                are None
  Return the file content as,
    ( lineno, line, revision, author, timestamp )

diff( self, url, revno1, revno2, url2=None )
  url    - file url for which the content is required.
  revno1 - older version
  revno2 - newer version
  url2   - a different (url2, revno2) as newer revision
  Return the difference unified diff text.

logs( self, url, revstart=None, revend=None )
  url                - file url for which the log messages are required.
  revstart to revend - log entries between revisions.
  Return the log entry as a tuple of,
      [ message,  revision, author, timestamp ]

changedfiles( self, url=None, revstart=Non, revend=None )
  url      - file url under which all the changed files should be identified
  revstart to revend - Changed files between specified revisions.
  Return the list of files as,
    [ { 'repos_path' : repos_path,
        'changetype' : <string>,
        'mime_type'  : mime_type,
      },
      ...
    ]
"""
import os, zeta.lib.helpers as h

class VcsFile(object):

    def __init__(self, vrep, url, revno=None, mimetype=None):
        """Instance representing an entry in a directory of repository tree,
        """
        self.vrep = vrep
        self.vcs = vrep.vcs
        self.vcsmod = vrep.vcsmod
        self.client = vrep.client
        self.url = url
        self.rooturl = vrep.rooturl
        info = self.vcsmod.info(self, url, revno=revno)
        self.revno = revno or info['l_revision']
        self.repopath = vrep.url_2_repopath(url)
        if self.rooturl == url:
            self.mimetype = 'text/directory'
        else:
            self.mimetype = mimetype or info.get('mime_type', '')

    def info(self, *args, **kwargs):
        """Place Holder,
        To be implemented by extension module,
        Return the information for the url.
        """
        pass

    def cat(self, *args, **kwargs):
        """Place Holder,
        To be implemented by extension module,
        Return the file content in the format specified by the api definition
        """
        pass

    def diff(self, *args, **kwargs):
        """Place Holder,
        To be implemented by extension module,
        Return the file content in the format specified by the api definition
        """
        pass


class VcsRepository(object):

    def __init__(self, vcs, vcsmod):
        """Instance that encapsulates the repository details and associated
        methods to access the respository
            self.url    - url to repository
            self.client - client object
            self.vcsmod - extension module implementing the repository
                          specific features.
            self.info   - info dictionary
        """
        self.vcs = vcs
        self.vcsmod = vcsmod
        self.rooturl = self.vcs.rooturl.rstrip('/')
        self.client = self.vcsmod.init(vcs)
        self.linfo = vcsmod.info(self, self.rooturl)
        self.finfo = vcsmod.info(self, self.rooturl, revno=1)

    def file(self, url, revno=None):
        """Manufacture VcsFile object for `url` at `revno`, optionally
        annotated"""
        vfile = VcsFile(self, url, revno=revno)
        vfile.info = h.hitch(vfile, VcsFile, self.vcsmod.info, url=url)
        vfile.cat = h.hitch(vfile, VcsFile, self.vcsmod.cat, url)
        vfile.diff = h.hitch(vfile, VcsFile, self.vcsmod.diff, url)
        return vfile

    def changedfiles(self, url=None, revstart=None, revend=None):
        """Manufacture a list of VcsFile object for each changed files,
        under `url` between `revstart` and `revend`"""
        cstats = self.vcsmod.changedfiles(self, url, revstart, revend)
        for d in cstats:
            d.setdefault('vfile', d['changetype'] != 'deleted' and self.file(os.path.join(self.rooturl, d['repos_path']), revno=revend) or None)

        return cstats

    def info(self, *args, **kwargs):
        """Place Holder,
        To be implemented by extension module,
        Return the information on repository"""
        pass

    def diff(self, *args, **kwargs):
        """Place Holder,
        To be implemented by extension module,
        Return the difference two revisions"""
        pass

    def list(self, *args, **kwargs):
        """Place Holder,
        To be implemented by extension module,
        Return the directory listing in a repository independant format"""
        pass

    def logs(self, *args, **kwargs):
        """Place Holder,
        To be implemented by extension module,
        Return the log messages in a repository independant format"""
        pass

    def url_2_repopath(self, url):
        repopath = url[len(self.rooturl):] or '/'
        return repopath[0] != '/' and '/' + repopath or repopath

    def repopath_2_url(repopath):
        return os.path.join(self.rooturl, repopath)


import zeta.lib.vcs.svn as svn, zeta.lib.vcs.bzr as bzr
vcsmods = {'svn': svn, 
   'bzr': bzr}

def open_repository(vcs):
    """Create repository interface and bind the adapter"""
    vcsmod = vcsmods[vcs.type.vcs_typename]
    vrep = VcsRepository(vcs, vcsmod)
    vrep.info = h.hitch(vrep, VcsRepository, vcsmod.info)
    vrep.list = h.hitch(vrep, VcsRepository, vcsmod.list)
    vrep.logs = h.hitch(vrep, VcsRepository, vcsmod.logs)
    vrep.diff = h.hitch(vrep, VcsRepository, vcsmod.diff)
    return vrep