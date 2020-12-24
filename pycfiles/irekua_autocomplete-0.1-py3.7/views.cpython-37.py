# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_autocomplete/views.py
# Compiled at: 2019-10-28 00:04:31
# Size of source mod 2**32: 3483 bytes
from django.db import models
from dal import autocomplete
from irekua_database import models as irekua_models

class InstitutionAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.Institution.objects.all()
        if self.q:
            institution_name_query = models.Q(institution_name__istartswith=(self.q))
            institution_code_query = models.Q(institution_code__istartswith=(self.q))
            subdependency_query = models.Q(subdependency__istartswith=(self.q))
            qs = qs.filter(institution_name_query | institution_code_query | subdependency_query)
        return qs


class DeviceBrandAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.DeviceBrand.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=(self.q))
        return qs


class DeviceAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.Device.objects.all()
        if self.q:
            brand_query = models.Q(brand__name__istartswith=(self.q))
            model_query = models.Q(model__istartswith=(self.q))
            type_query = models.Q(device_type__name__istartswith=(self.q))
            qs = qs.filter(brand_query | model_query | type_query)
        return qs


class CollectionAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.Collection.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=(self.q))
        return qs


class CollectionTypeAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.CollectionType.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=(self.q))
        return qs


class MetacollectionAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.MetaCollection.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=(self.q))
        return qs


class TermsAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.Term.objects.all()
        term_type = self.forwarded.get('term_type', None)
        if term_type:
            qs = qs.filter(term_type=term_type)
        if self.q:
            qs = qs.filter(value__istartswith=(self.q))
        return qs


class TagsAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.Tag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=(self.q))
        return qs


class AnnotationToolsAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.AnnotationTool.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=(self.q))
        return qs


class SamplingEventTypesAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.SamplingEventType.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=(self.q))
        return qs


class UserAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        qs = irekua_models.User.objects.all()
        if self.q:
            qs = qs.filter(email__istartswith=(self.q))
        return qs

    def get_result_label(self, item):
        return item.email