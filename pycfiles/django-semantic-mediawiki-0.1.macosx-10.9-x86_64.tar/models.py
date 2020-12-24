# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nikita/Code/djangowiki/ve/lib/python2.7/site-packages/django_semantic_mediawiki/models.py
# Compiled at: 2014-02-28 10:10:46
from __future__ import unicode_literals
from django.db import models
import requests, collections, json
from django.conf import settings

class WikiManager(models.Manager):

    def get_query_set(self):
        return WikiQuerySet(self.model)

    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)


class WikiQuerySet(object):

    def __init__(self, model=None, query={}, using=None):
        self.model = model
        self.query = query
        self.executed = False
        self._cache = []
        self._cache_full = False
        if using is None:
            try:
                using = settings.DATABASES[b'semantic'][b'NAME']
            except KeyError:
                raise Exception(b"No API selected. You should either add an api url in settings.DATABASES['semantic']['NAME']" + b" or specify an url with the 'using' parameter " + b"(eg: Model.objects.all(using='http://wiki.urlab.be/api.php?action=ask&query=')) ")

        self.using = using
        return

    def all(self):
        return WikiQuerySet(model=self.model, query=self.query, using=self.using)

    _clone = all

    def _request_crafter(self, i):
        if b'order' in self.query:
            sort, order = [], []
            for conventional, col in self.query[b'order']:
                sign = b'ASC' if conventional else b'DESC'
                order.append(sign)
                sort.append(col)

            sort_str = (b'|sort={sort}|order={order}').format(sort=(b',').join(sort), order=(b',').join(order))
        else:
            sort_str = b''
        columns = filter(lambda x: x is not None, map(lambda x: x.db_column, self.model._meta.fields))
        columns_str = (b'').join(map(lambda x: b'|?' + x, columns))
        return (b'{domain}[[Category:{model}]]{sort}{columns}|offset={offset}&format=json').format(domain=self.using, sort=sort_str, model=self.model._meta.object_name, columns=columns_str, offset=i)

    def _http(self, url):
        print (b'R = {} ').format(url)
        return requests.get(url)

    def _deserialize(self, text):
        return json.loads(text, object_pairs_hook=collections.OrderedDict, encoding=b'unicode_escape')

    @property
    def ordered(self):
        return b'order' in self.query

    def reverse(self):
        if not self.ordered:
            raise Exception(b'Cannot reverse non-ordered query.')
        clone = self.all()
        clone.query[b'order'] = map(lambda (order, key): (not order, key), self.query[b'order'])
        return clone

    def order_by(self, *fields):
        if self.executed:
            raise Exception(b'Cannot order a query once it has been executed.')
        clone = self.all()
        if not self.ordered:
            clone.query[b'order'] = []
        fields = map(lambda x: (x[0] != b'-', x[1:] if x[0] == b'-' else x), fields)
        clone.query[b'order'] += fields
        return clone

    def __len__(self):
        return len(list(self.iterator()))

    count = __len__

    def get(self, *args, **kwargs):
        clone = self.filter(*args, **kwargs)
        num = len(clone)
        if num == 1:
            return clone._create_model(clone.result[0])
        if not num:
            raise self.model.DoesNotExist(b'%s matching query does not exist.' % self.model._meta.object_name)
        raise self.model.MultipleObjectsReturned(b'get() returned more than one %s -- it returned %s!' % (
         self.model._meta.object_name, num))

    def iterator(self):
        i = 0
        if not self.executed:
            self.executed = True
            self.end = False
        else:
            for elem in self._cache:
                i += 1
                yield elem

        if not self._cache_full:
            while not self.end:
                url = self._request_crafter(i=i)
                j = self._deserialize(self._http(url).text)
                response = j[b'query'][b'results']
                self.end = b'query-continue' not in j
                for key, item in response.iteritems():
                    i += 1
                    new_item = {}
                    new_item[b'key'] = (b':').join(key.split(b':')[1:])
                    new_item[b'url'] = item[b'fullurl']
                    for colum, value in item[b'printouts'].iteritems():
                        new_item[colum] = value

                    obj = self._create_model(new_item)
                    self._cache.append(obj)
                    yield obj

        self._cache_full = True

    __iter__ = iterator

    def __getitem__(self, k):
        return list(self).__getitem__(k)

    def _create_model(self, line):
        fields = filter(lambda x: x.db_column is not None, self.model._meta.fields)
        cols = {}
        for field in fields:
            cols[field.name] = line[field.db_column.capitalize()]

        return self.model(name=line[b'key'], url=line[b'url'], **cols)

    def filter(self, *args, **kwargs):
        if self.executed:
            raise Exception(b'Cannot filter a query once it has been executed.')
        clone = self.all()
        for key in kwargs:
            val = kwargs[key]
            if not key == b'Category':
                key += b':'
            clone.query += (b'[[{}:{}]]').format(key, val)

        return clone


class WikiCharField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs[b'max_length'] = 500
        super(WikiCharField, self).__init__(*args, **kwargs)


class WikiModel(models.Model):
    objects = WikiManager()

    class Meta:
        abstract = True
        managed = False