# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/simo/PycharmProjects/mezzanine_page_auth/mezzanine_page_auth/tests/factories.py
# Compiled at: 2014-02-06 10:42:00
from __future__ import unicode_literals
import factory
from django.contrib.auth.models import User, Group
from mezzanine.pages.models import RichTextPage, Link
from ..models import PageAuthGroup
DOMAIN = b'comune.zolapredosa.bo.it'

class GroupF(factory.DjangoModelFactory):
    FACTORY_FOR = Group
    FACTORY_DJANGO_GET_OR_CREATE = ('name', )
    name = factory.Sequence(lambda n: b'group_%s' % n)


class OperatorsGroupF(GroupF):
    name = b'goperators'


class AdminsGroupF(GroupF):
    name = b'gadmins'


class UserF(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: b'user_%s' % n)
    password = factory.Sequence(lambda n: b'user_%s' % n)
    email = factory.LazyAttribute(lambda o: (b'{}@{}').format(o.username, DOMAIN))
    is_staff = True
    is_active = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop(b'password', None)
        user = super(UserF, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)


class AdminUserF(UserF):
    username = b'admin'
    password = b'admin'
    email = (b'admin@{}').format(DOMAIN)
    is_superuser = True


class RichTextPageF(factory.DjangoModelFactory):
    FACTORY_FOR = RichTextPage
    FACTORY_DJANGO_GET_OR_CREATE = ('title', )
    status = 2
    title = factory.Sequence(lambda n: (b'richtextpage_{}').format(n))
    description = factory.LazyAttribute(lambda page: (b'Description of {}').format(page.title))
    content = factory.LazyAttribute(lambda page: (b'<h1>{0}</h1><p>Content of page "{0}"</p>').format(page.title))
    login_required = False
    parent = None


class LinkF(factory.DjangoModelFactory):
    FACTORY_FOR = Link
    FACTORY_DJANGO_GET_OR_CREATE = ('title', )
    status = 2
    title = factory.Sequence(lambda n: (b'richtextpage_{}').format(n))
    slug = factory.LazyAttribute(lambda a: (b'{}').format(a.title))
    login_required = False
    parent = None


class RichTextPageWithLoginF(RichTextPageF):
    title = factory.Sequence(lambda n: (b'richtextpage_{} with login').format(n))
    login_required = True


class PageAuthGroupF(factory.DjangoModelFactory):
    FACTORY_FOR = PageAuthGroup
    group = factory.SubFactory(GroupF)
    page = factory.SubFactory(RichTextPageWithLoginF)


class GroupWithPageF(GroupF):
    membership = factory.RelatedFactory(PageAuthGroupF, b'group')


class RichTextPageWithGroupF(RichTextPageWithLoginF):
    membership = factory.RelatedFactory(PageAuthGroupF, b'page', group__name=b'goperators')