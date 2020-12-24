# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pybitbucket/snippet.py
# Compiled at: 2016-12-28 18:40:02
# Size of source mod 2**32: 7101 bytes
from __future__ import unicode_literals
from uritemplate import expand
from voluptuous import Schema, Optional, In
from pybitbucket.bitbucket import Bitbucket, BitbucketBase, Client, PayloadBuilder, RepositoryType, Enum

def open_files(filelist):
    files = []
    for filename in filelist:
        files.append(('file', (filename, open(filename, 'rb'))))

    return files


class SnippetRole(Enum):
    OWNER = 'owner'
    CONTRIBUTOR = 'contributor'
    MEMBER = 'member'


class SnippetPayload(PayloadBuilder):
    """SnippetPayload"""
    schema = Schema({Optional('title'): str, 
     Optional('scm'): In(RepositoryType), 
     Optional('is_private'): bool})

    def __init__(self, payload=None, owner=None):
        super(SnippetPayload, self).__init__(payload=payload)
        self._owner = owner

    @property
    def owner(self):
        return self._owner

    def add_owner(self, owner):
        return SnippetPayload(payload=(self._payload.copy()),
          owner=owner)

    def add_title(self, title):
        new = self._payload.copy()
        new['title'] = title
        return SnippetPayload(payload=new,
          owner=(self.owner))

    def add_scm(self, scm):
        new = self._payload.copy()
        new['scm'] = scm
        return SnippetPayload(payload=new,
          owner=(self.owner))

    def add_is_private(self, is_private):
        new = self._payload.copy()
        new['is_private'] = is_private
        return SnippetPayload(payload=new,
          owner=(self.owner))


class Snippet(BitbucketBase):
    """Snippet"""
    id_attribute = 'id'
    resource_type = 'snippets'
    templates = {'create': '{+bitbucket_url}/2.0/snippets'}

    @staticmethod
    def is_type(data):
        if data.get('links') is None or data['links'].get('self') is None or data['links']['self'].get('href') is None or data.get(Snippet.id_attribute) is None:
            return False
        else:
            is_v2 = True
            url_path = data['links']['self']['href'].split('/')
            position = -1
            is_v2 = is_v2 and data[Snippet.id_attribute] == url_path[position]
            position -= 2
            is_v2 = Snippet.resource_type == url_path[position]
            return is_v2

    def __init__(self, data, client=Client()):
        super(Snippet, self).__init__(data, client=client)
        if data.get('files'):
            self.filenames = [str(f) for f in data['files']]

    @classmethod
    def create(cls, files, payload=None, client=None):
        """Create a new snippet.

        :param files:
        :type files:
        :param payload: the options for creating the new snippet.
        :type payload: SnippetPayload
        :param client: the configured connection to Bitbucket.
            If not provided, assumes an Anonymous connection.
        :type client: bitbucket.Client
        :returns: the new build status object.
        :rtype: BuildStatus
        :raises: ValueError
        """
        client = client or Client()
        payload = payload or SnippetPayload()
        json = payload.validate().build()
        api_url = expand(cls.templates['create'], {'bitbucket_url': client.get_bitbucket_url()})
        return cls.post(api_url, json=json, files=files, client=client)

    def modify(self, files=None, payload=None):
        """
        A convenience method for changing the current snippet.
        The parameters make it easier to know what can be changed
        and allow references with file names instead of File objects.
        """
        files = files or open_files([])
        payload = payload or SnippetPayload()
        json = payload.validate().build()
        return self.put(json=json, files=files)

    def content(self, filename):
        """
        A method for obtaining the contents of a file on a snippet.
        If the filename is not on the snippet, no content is returned.
        """
        if not self.files.get(filename):
            return
        else:
            url = self.files[filename]['links']['self']['href']
            response = self.client.session.get(url)
            Client.expect_ok(response)
            return response.content

    @staticmethod
    def find_snippets_for_role(role=SnippetRole.OWNER, client=None):
        """
        A convenience method for finding snippets by the user's role.
        The method is a generator Snippet objects.

        :param role: the role of the current user on the snippets.
            If not provided, assumes the relationship owner.
        :type role: SnippetRole
        :param client: the configured connection to Bitbucket.
            If not provided, assumes an Anonymous connection.
        :type client: bitbucket.Client
        :returns: an iterator over the selected snippets.
        :rtype: iterator
        """
        client = client or Client()
        SnippetRole(role)
        return Bitbucket(client=client).snippetsForRole(role=role)

    @staticmethod
    def find_snippet_by_id_and_owner(id, owner=None, client=None):
        """
        A convenience method for finding a specific snippet.
        In contrast to the pure hypermedia driven method on the Bitbucket
        class, this method returns a Snippet object, instead of the
        generator.

        :param id: the id of the snippet.
        :type id: str
        :param owner: the owner of the snippet.
            If not provided, assumes the current user.
        :type owner: str
        :param client: the configured connection to Bitbucket.
            If not provided, assumes an Anonymous connection.
        :type client: bitbucket.Client
        :returns: the snippet referenced by the id.
        :rtype: bitbucket.Snippet
        """
        client = client or Client()
        owner = owner or client.get_username()
        return next(Bitbucket(client=client).snippetByOwnerAndSnippetId(owner=owner,
          snippet_id=id))


Client.bitbucket_types.add(Snippet)