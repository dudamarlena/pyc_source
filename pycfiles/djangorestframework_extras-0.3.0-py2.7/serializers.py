# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_framework_extras/users/serializers.py
# Compiled at: 2017-05-03 09:02:01
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework import fields

class UserSerializerForSuperUser(serializers.HyperlinkedModelSerializer):
    password = fields.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'
        write_only_fields = ('password', )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super(UserSerializerForSuperUser, self).create(validated_data)
        if password is not None:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super(UserSerializerForSuperUser, self).update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserSerializerForStaff(serializers.HyperlinkedModelSerializer):
    password = fields.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'password')
        read_only_fields = ('last_login', 'date_joined', 'is_active', 'is_superuser')
        write_only_fields = ('password', )

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super(UserSerializerForStaff, self).create(validated_data)
        if password is not None:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super(UserSerializerForStaff, self).update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserSerializerForUser(serializers.HyperlinkedModelSerializer):
    password = fields.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = ('last_login', 'date_joined', 'is_active')
        write_only_fields = ('password', )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super(UserSerializerForUser, self).update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user