# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\django\django-nimble\nimble\serializers\debt.py
# Compiled at: 2017-01-15 11:08:07
# Size of source mod 2**32: 703 bytes
from rest_framework import serializers, viewsets
from nimble.models.debt import Debt
from .user import UserSerializer

class DebtSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True, default=serializers.CreateOnlyDefault('Junk'))

    class Meta:
        model = Debt
        fields = Debt.api_keys()

    def validate_author(self, value):
        """
        This will force the author when a new debt is created via the API.
        """
        return self.context['request'].user


class DebtViewSet(viewsets.ModelViewSet):
    queryset = Debt.objects.all()
    serializer_class = DebtSerializer