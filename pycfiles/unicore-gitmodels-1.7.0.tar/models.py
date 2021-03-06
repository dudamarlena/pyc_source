# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sdehaan/Documents/Repositories/unicore-gitmodels/unicore_gitmodels/models.py
# Compiled at: 2014-10-10 08:14:19
import re, unicodedata
from gitmodel import fields, models
from unicore_gitmodels.fields import ListField
RE_NUMERICAL_SUFFIX = re.compile('^[\\w-]*-(\\d+)+$')

class FilterMixin(object):

    @classmethod
    def filter(cls, **fields):
        items = list(cls.all())
        for field, value in fields.items():
            if hasattr(cls, field):
                items = [ a for a in items if getattr(a, field) == value ]
            else:
                raise Exception('invalid field %s' % field)

        return items


class SlugifyMixin(object):

    def slugify(self, value):
        """
        Normalizes string, converts to lowercase, removes non-alpha characters,
        and converts spaces to hyphens.
        """
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\\w\\s-]', '', value).strip().lower())
        return re.sub('[-\\s]+', '-', value)

    def generate_slug(self):
        if hasattr(self, 'title') and self.title:
            if hasattr(self, 'slug') and not self.slug:
                self.slug = self.slugify(unicode(self.title))[:40]

    def save(self, *args, **kwargs):
        self.generate_slug()
        return super(SlugifyMixin, self).save(*args, **kwargs)


class GitCategoryModel(SlugifyMixin, FilterMixin, models.GitModel):
    slug = fields.SlugField(required=True)
    title = fields.CharField(required=True)
    subtitle = fields.CharField(required=False)
    language = fields.CharField(required=False)
    featured_in_navbar = fields.BooleanField(default=False)
    source = fields.RelatedField('GitCategoryModel', required=False)
    position = fields.IntegerField(required=False, default=0)

    def __unicode__(self):
        return self.title

    @property
    def uuid(self):
        return self.id

    def __eq__(self, other):
        if not other:
            return False
        if isinstance(other, dict):
            return self.slug == other['slug']
        return self.slug == other.slug

    def __ne__(self, other):
        if not other:
            return True
        if isinstance(other, dict):
            return self.slug != other['slug']
        return self.slug != other.slug

    def to_dict(self):
        source = self.source.to_dict() if self.source else None
        return {'uuid': self.uuid, 
           'slug': self.slug, 
           'title': self.title, 
           'subtitle': self.subtitle, 
           'language': self.language, 
           'featured_in_navbar': self.featured_in_navbar, 
           'source': source, 
           'position': self.position}

    @classmethod
    def all(cls):
        items = list(super(GitCategoryModel, cls).all())
        sorted_items = sorted(items, key=lambda cat: cat.position)
        return models.ModelSet(c for c in sorted_items)


class GitPageModel(SlugifyMixin, FilterMixin, models.GitModel):
    slug = fields.SlugField(required=True)
    title = fields.CharField(required=True)
    subtitle = fields.CharField(required=False)
    description = fields.CharField(required=False)
    content = fields.CharField(required=False)
    created_at = fields.DateTimeField(required=False)
    modified_at = fields.DateTimeField(required=False)
    published = fields.BooleanField(default=True)
    primary_category = fields.RelatedField(GitCategoryModel, required=False)
    featured = fields.BooleanField(default=False)
    featured_in_category = fields.BooleanField(default=False)
    language = fields.CharField(required=False)
    source = fields.RelatedField('GitPageModel', required=False)
    linked_pages = ListField(default=[], required=False)
    position = fields.IntegerField(required=False, default=0)

    def __unicode__(self):
        return self.title

    @property
    def uuid(self):
        return self.id

    @classmethod
    def all(cls):
        items = list(super(GitPageModel, cls).all())
        sorted_items = sorted(items, key=lambda page: page.position)
        return models.ModelSet(c for c in sorted_items)

    def to_dict(self):
        primary_category = self.primary_category.to_dict() if self.primary_category else None
        source = self.source.to_dict() if self.source else None
        return {'uuid': self.uuid, 
           'slug': self.slug, 
           'title': self.title, 
           'subtitle': self.subtitle, 
           'description': self.description, 
           'content': self.content, 
           'created_at': self.created_at, 
           'modified_at': self.modified_at, 
           'published': self.published, 
           'primary_category': primary_category, 
           'source': source, 
           'language': self.language, 
           'featured': self.featured, 
           'featured_in_category': self.featured_in_category, 
           'linked_pages': self.linked_pages, 
           'position': self.position}

    def get_linked_pages(self):
        if self.linked_pages is None:
            return []
        else:
            return [ self.__class__.get(uuid) for uuid in self.linked_pages ]