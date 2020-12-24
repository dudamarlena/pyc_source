# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_autocomplete/term_autocomplete.py
# Compiled at: 2019-10-28 00:11:41
# Size of source mod 2**32: 2635 bytes
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from django_filters import FilterSet
from irekua_database import models

class EntailmentSerializer(serializers.Serializer):
    term_type = serializers.CharField(source='target.term_type')
    description = serializers.CharField(source='target.description')
    value = serializers.CharField(source='target.value')
    id = serializers.IntegerField(source='target.id')
    scope = serializers.CharField(source='target.scope')


class TermSerializer(serializers.ModelSerializer):
    term_type = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.Term
        fields = [
         'id',
         'scope',
         'term_type',
         'value',
         'description']


class ComplexTermSerializer(serializers.ModelSerializer):
    term_type = serializers.StringRelatedField(many=False)
    entailments = EntailmentSerializer(many=True,
      read_only=True,
      source='entailment_source')

    class Meta:
        model = models.Term
        fields = [
         'id',
         'scope',
         'term_type',
         'value',
         'description',
         'entailments']


class SynonymSerializer(serializers.ModelSerializer):
    target = ComplexTermSerializer()

    class Meta:
        model = models.Term
        fields = [
         'target']


class FullTermSerializer(serializers.ModelSerializer):
    term_type = serializers.StringRelatedField(many=False)
    entailments = EntailmentSerializer(many=True,
      read_only=True,
      source='entailment_source')
    synonyms = SynonymSerializer(many=True,
      source='synonym_source')

    class Meta:
        model = models.Term
        fields = [
         'id',
         'scope',
         'term_type',
         'value',
         'description',
         'entailments',
         'synonyms']


class TermFilter(FilterSet):

    class Meta:
        model = models.Term
        fields = {'value':[
          'icontains'], 
         'term_type':[
          'exact']}


class TermListView(ListAPIView):
    serializer_class = FullTermSerializer
    filterset_class = TermFilter

    def get_queryset(self):
        queryset = models.Term.objects.all()
        event_type = models.EventType.objects.get(pk=(self.kwargs['pk']))
        for term in event_type.should_imply.all():
            queryset = queryset.filter(entailment_source__target=term)

        return queryset