# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/pytigon/pytigon/prj/schdevtools/schbuilder/schema.py
# Compiled at: 2020-03-08 11:48:32
# Size of source mod 2**32: 498 bytes
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
import graphene
from .models import SChAppSet

class _SChAppSet(DjangoObjectType):

    class Meta:
        model = SChAppSet


def extend_query(query_class):

    class query(query_class):
        app_sets = graphene.List(_SChAppSet)

        def resolve_app_sets(self, info):
            return SChAppSet.objects.all()

    return query


def extend_mutation(mutation_class):
    return mutation_class