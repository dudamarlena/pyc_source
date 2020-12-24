# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pybitbucket/ref.py
# Compiled at: 2016-12-28 18:40:02
# Size of source mod 2**32: 3553 bytes
from __future__ import unicode_literals
from pybitbucket.bitbucket import Bitbucket, BitbucketBase, Client

class Ref(BitbucketBase):
    id_attribute = 'name'

    @staticmethod
    def is_type(*args):
        return False

    @staticmethod
    def find_refs_in_repository(owner, repository_name, client=Client()):
        """
        A convenience method for finding refs in a repository.
        The method is a generator Ref subtypes of Tag and Branch.
        """
        return Bitbucket(client=client).repositoryRefs(owner=owner,
          repository_name=repository_name)


class Tag(Ref):
    resource_type = 'tags'

    @staticmethod
    def is_type(data):
        return Tag.has_v2_self_url(data)

    @staticmethod
    def find_tags_in_repository(repository_name, owner=None, client=Client()):
        """
        A convenience method for finding tags in a repository.
        The method is a generator Tag objects.
        """
        owner = owner or client.get_username()
        return Bitbucket(client=client).repositoryTags(owner=owner,
          repository_name=repository_name)

    @staticmethod
    def find_tag_by_ref_name_in_repository(ref_name, repository_name, owner=None, client=Client()):
        """
        A convenience method for finding a specific tag.
        In contrast to the pure hypermedia driven method on the Bitbucket
        class, this method returns a Tag object, instead of the
        generator.
        """
        owner = owner or client.get_username()
        return next(Bitbucket(client=client).repositoryTagByName(owner=owner,
          repository_name=repository_name,
          ref_name=ref_name))


class Branch(Ref):
    resource_type = 'branches'

    @staticmethod
    def is_type(data):
        return Branch.has_v2_self_url(data)

    @staticmethod
    def find_branches_in_repository(repository_name, owner=None, client=Client()):
        """
        A convenience method for finding branches in a repository.
        The method is a generator Branch objects.
        """
        owner = owner or client.get_username()
        return Bitbucket(client=client).repositoryBranches(owner=owner,
          repository_name=repository_name)

    @staticmethod
    def find_branch_by_ref_name_in_repository(ref_name, repository_name, owner=None, client=Client()):
        """
        A convenience method for finding a specific branch.
        In contrast to the pure hypermedia driven method on the Bitbucket
        class, this method returns a Branch object, instead of the
        generator.
        """
        owner = owner or client.get_username()
        return next(Bitbucket(client=client).repositoryBranchByName(owner=owner,
          repository_name=repository_name,
          ref_name=ref_name))


Client.bitbucket_types.add(Ref)
Client.bitbucket_types.add(Tag)
Client.bitbucket_types.add(Branch)