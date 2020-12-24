# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dvs/Dropbox/Code/djangoql/test_project/core/admin.py
# Compiled at: 2019-04-13 19:28:46
# Size of source mod 2**32: 3675 bytes
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.db.models import Q, Count
from django.utils.timezone import now
from djangoql.admin import DjangoQLSearchMixin
from djangoql.schema import DjangoQLSchema, IntField
from .models import Book
admin.site.unregister(User)

class BookQLSchema(DjangoQLSchema):
    suggest_options = {Book: ['genre']}


@admin.register(Book)
class BookAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    djangoql_schema = BookQLSchema
    list_display = ('name', 'author', 'genre', 'written', 'is_published')
    list_filter = ('is_published', )
    filter_horizontal = ('similar_books', )


class UserAgeField(IntField):
    __doc__ = '\n    Search by given number of full years\n    '
    model = User
    name = 'age'

    def get_lookup_name(self):
        """
        We'll be doing comparisons vs. this model field
        """
        return 'date_joined'

    def get_lookup(self, path, operator, value):
        if operator == 'in':
            result = None
            for year in value:
                condition = self.get_lookup(path, '=', year)
                result = condition if result is None else result | condition

            return result
        else:
            if operator == 'not in':
                result = None
                for year in value:
                    condition = self.get_lookup(path, '!=', year)
                    result = condition if result is None else result & condition

                return result
            else:
                value = self.get_lookup_value(value)
                search_field = '__'.join(path + [self.get_lookup_name()])
                year_start = self.years_ago(value + 1)
                year_end = self.years_ago(value)
                if operator == '=':
                    return Q(**{'%s__gt' % search_field: year_start}) & Q(**{'%s__lte' % search_field: year_end})
                if operator == '!=':
                    return Q(**{'%s__lte' % search_field: year_start}) | Q(**{'%s__gt' % search_field: year_end})
                if operator == '>':
                    return Q(**{'%s__lt' % search_field: year_start})
                if operator == '>=':
                    return Q(**{'%s__lt' % search_field: year_end})
                if operator == '<':
                    return Q(**{'%s__gt' % search_field: year_end})
            if operator == '<=':
                return Q(**{'%s__gte' % search_field: year_start})

    def years_ago(self, n):
        timestamp = now()
        try:
            return timestamp.replace(year=(timestamp.year - n))
        except ValueError:
            return timestamp.replace(month=2, day=28, year=(timestamp.year - n))


class UserQLSchema(DjangoQLSchema):
    exclude = (
     Book,)
    suggest_options = {Group: ['name']}

    def get_fields(self, model):
        fields = super(UserQLSchema, self).get_fields(model)
        if model == User:
            fields = [
             UserAgeField(), IntField(name='groups_count')] + fields
        return fields


@admin.register(User)
class CustomUserAdmin(DjangoQLSearchMixin, UserAdmin):
    djangoql_schema = UserQLSchema
    search_fields = ('username', 'first_name', 'last_name')
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'group')

    def group(self, obj):
        return ', '.join([g.name for g in obj.groups.all()])

    group.short_description = 'Groups'

    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        return qs.annotate(groups_count=(Count('groups'))).prefetch_related('groups')