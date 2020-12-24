# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jon/DMN/Scripts/django-rolodex/rolodex/API/serializers.py
# Compiled at: 2016-01-21 18:17:44
from rest_framework import serializers
from rolodex.models import Person, Org, Contact, PersonRole, OrgContactRole, P2P, Org2Org, P2Org, Org2P, P2P_Type, Org2Org_Type, P2Org_Type
from django.contrib.auth.models import User

class RoleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PersonRole
        fields = ('role', 'description')


class ContactRoleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OrgContactRole
        fields = ('role', 'description')


class P2P_TypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = P2P_Type
        fields = ('relationship_type', )


class Org2Org_TypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Org2Org_Type
        fields = ('relationship_type', )


class P2Org_TypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = P2Org_Type
        fields = ('relationship_type', )


class PersonSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Person
        fields = ('id', 'slug', 'firstName', 'lastName', 'position', 'department',
                  'gender', 'role', 'person_contact', 'org_relations', 'p_relations')


class OrgSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Org
        fields = ('id', 'slug', 'orgName', 'org_relations', 'p_relations', 'org_contact')


class ContactSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contact
        fields = ('id', 'person', 'org', 'type', 'contact', 'role', 'notes')


class P2PSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = P2P
        fields = ('id', 'from_ent', 'to_ent', 'relation', 'from_date', 'to_date', 'description')


class Org2OrgSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Org2Org
        fields = ('id', 'from_ent', 'to_ent', 'relation', 'from_date', 'to_date', 'description')


class P2OrgSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = P2Org
        fields = ('id', 'from_ent', 'to_ent', 'relation', 'from_date', 'to_date', 'description')


class Org2PSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Org2P
        fields = ('id', 'from_ent', 'to_ent', 'relation', 'from_date', 'to_date', 'description')