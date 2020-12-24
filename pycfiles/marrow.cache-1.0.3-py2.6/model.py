# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/marrow/cache/model.py
# Compiled at: 2015-04-23 10:59:08
from __future__ import unicode_literals
from wrapt import decorator
from inspect import isclass
from mongoengine import Document, EmbeddedDocument
from mongoengine import StringField, DateTimeField, GenericReferenceField, DynamicField, EmbeddedDocumentField
from .exc import CacheMiss
from .compat import py3, unicode, iteritems
from .util import sha256, timedelta, resolve, wraps, ref, utcnow, chain, isclass, deque, contextmanager, stack, pformat, fetch

class CacheKey(EmbeddedDocument):
    """The unique key cached values are indexed on."""
    prefix = StringField(db_field=b'p', default=None)
    reference = GenericReferenceField(db_field=b'r', default=None)
    hash = StringField(db_field=b'h')

    def __repr__(self):
        return (b'CacheKey({0.prefix}, {0.reference}, {0.hash})').format(self)

    @classmethod
    def new(cls, prefix, reference, args, kw):
        hash = sha256()
        hash.update(unicode(pformat(args)).encode(b'utf8'))
        hash.update(unicode(pformat(kw)).encode(b'utf8'))
        result = cls(prefix=prefix, reference=reference, hash=hash.hexdigest())
        return result


class CacheMark(object):
    """The bulk of the caching machinery is contained within this decorator class.
        
        This provides a single location for all of the settings and callbacks associated with a function or method whose
        result you wish cached.  Instances are constructed using the ``@Cache.memoize`` and ``@Cache.method`` decorators.
        """

    def __init__(self, manager, expiry, prefix=None, reference=False, refresh=False, populate=True, processor=None):
        self.manager = manager
        self.expiry = expiry
        self.prefix = prefix
        self.reference = reference
        self.refresh = refresh
        self.populate = populate
        self.processor = processor
        super(CacheMark, self).__init__()

    @decorator
    def __call__(self, wrapped, instance, args, kw):
        prefix = self.prefix if self.prefix else resolve(wrapped)
        reference = self.reference
        if reference and isinstance(instance, Document):
            veto = getattr(instance, b'__nocache__', False)
            if not instance.pk or instance._created or veto and veto[(-1)]:
                return wrapped(*args, **kw)
            reference = instance if reference is True else reference
        _args = self.processor(instance, args, kw) if self.processor else (args, kw)
        key = CacheKey.new(prefix, (None if reference in (True, False) else reference), *_args)
        try:
            return self.manager.get(key, refresh=self.expiry if self.refresh else None)
        except CacheMiss:
            if not self.populate:
                raise

        return self.manager.set(key, wrapped(*args, **kw), self.expiry()).value


class Cache(Document):
    """A cached value."""
    meta = dict(collection=b'cache', allow_inheritance=False, indexes=[
     dict(fields=('expires', ), expireAfterSeconds=0)])
    DEFAULT_DELTA = timedelta(weeks=1, days=0, hours=0, minutes=0, seconds=0)
    key = EmbeddedDocumentField(CacheKey, db_field=b'_id', primary_key=True)
    value = DynamicField(db_field=b'v')
    expires = DateTimeField(db_field=b'e', default=lambda : utcnow() + timedelta(weeks=1))

    def __repr__(self):
        return (b'Cache({1.prefix}, {1.reference}, {1.hash}, {0.expires})').format(self, self.key if self.key else CacheKey())

    @classmethod
    def get(cls, criteria, refresh=None):
        """"""
        result = cls.objects(pk=criteria).scalar(b'expires', b'value').first()
        if not result:
            raise CacheMiss()
        if result[0].replace(tzinfo=None) < utcnow():
            cls.objects(pk=criteria).delete()
            raise CacheMiss()
        if refresh:
            cls.objects(pk=criteria).update(set__expires=refresh(), write_concern={b'w': 0})
        return result[1]

    @classmethod
    def set(cls, criteria, value, expires):
        """"""
        return cls(pk=criteria, value=value, expires=expires).save(force_insert=True, write_concern={b'w': 0})

    @classmethod
    def generate_expiry(cls, expires, weeks, days, hours, minutes, seconds):

        def generate_expiry_inner():
            if weeks or days or hours or minutes or seconds:
                return expires() + timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
            if cls.DEFAULT_DELTA:
                return expires() + cls.DEFAULT_DELTA
            return expires()

        return generate_expiry_inner

    @classmethod
    def memoize(cls, prefix=None, reference=None, expires=utcnow, weeks=0, days=0, hours=0, minutes=0, seconds=0, refresh=False, populate=True):
        """"""
        return CacheMark(cls, cls.generate_expiry(expires, weeks, days, hours, minutes, seconds), prefix, False if reference is None else reference, refresh, populate)

    @classmethod
    def method(cls, *attributes, **kw):
        """"""

        def method_args_callback(instance, args, kw):
            return (
             tuple(fetch(instance, i) for i in attributes) + args[1:], kw)

        return CacheMark(cls, cls.generate_expiry(kw.pop(b'expires', utcnow), **dict((i, kw.get(i, 0)) for i in ('weeks',
                                                                                                                 'days',
                                                                                                                 'hours',
                                                                                                                 'minutes',
                                                                                                                 'seconds'))), kw.get(b'prefix', None), kw.get(b'reference', True), kw.get(b'refresh', False), kw.get(b'populate', True), method_args_callback)

    @staticmethod
    @contextmanager
    def disable(target=None):
        with stack(Document if target is None else target, b'__nocache__', True):
            yield
        return

    @staticmethod
    @contextmanager
    def enable(target=None):
        with stack(Document if target is None else target, b'__nocache__', False):
            yield
        return