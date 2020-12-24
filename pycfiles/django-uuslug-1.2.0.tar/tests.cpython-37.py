# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/val/Projects/workon/mpro/uuslug/django-uuslug/uuslug/tests/tests.py
# Compiled at: 2019-12-08 17:06:25
# Size of source mod 2**32: 10283 bytes
from django.test import TestCase
from uuslug import slugify, uuslug
from uuslug.models import CoolSlug, AnotherSlug, TruncatedSlug, SmartTruncatedSlug, SmartTruncatedExactWordBoundrySlug, CoolSlugDifferentSeparator, TruncatedSlugDifferentSeparator, AutoTruncatedSlug

class SlugUnicodeTestCase(TestCase):
    __doc__ = 'Tests for Slug - Unicode'

    def test_manager(self):
        txt = 'This is a test ---'
        r = slugify(txt)
        self.assertEqual(r, 'this-is-a-test')
        txt = 'This -- is a ## test ---'
        r = slugify(txt)
        self.assertEqual(r, 'this-is-a-test')
        txt = '影師嗎'
        r = slugify(txt)
        self.assertEqual(r, 'ying-shi-ma')
        txt = "C'est déjà l'été."
        r = slugify(txt)
        self.assertEqual(r, 'c-est-deja-l-ete')
        txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
        r = slugify(txt)
        self.assertEqual(r, 'nin-hao-wo-shi-zhong-guo-ren')
        txt = 'Компьютер'
        r = slugify(txt)
        self.assertEqual(r, 'kompiuter')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt)
        self.assertEqual(r, 'jaja-lol-mememeoo-a')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=9)
        self.assertEqual(r, 'jaja-lol')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=15)
        self.assertEqual(r, 'jaja-lol-mememe')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=50)
        self.assertEqual(r, 'jaja-lol-mememeoo-a')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=15, word_boundary=True)
        self.assertEqual(r, 'jaja-lol-a')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=17, word_boundary=True)
        self.assertEqual(r, 'jaja-lol-mememeoo')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=18, word_boundary=True)
        self.assertEqual(r, 'jaja-lol-mememeoo')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=19, word_boundary=True)
        self.assertEqual(r, 'jaja-lol-mememeoo-a')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=20, word_boundary=True, separator='.')
        self.assertEqual(r, 'jaja.lol.mememeoo.a')
        txt = 'jaja---lol-méméméoo--a'
        r = slugify(txt, max_length=20, word_boundary=True, separator='ZZZZZZ')
        self.assertEqual(r, 'jajaZZZZZZlolZZZZZZmememeooZZZZZZa')
        txt = '___This is a test ---'
        r = slugify(txt)
        self.assertEqual(r, 'this-is-a-test')
        txt = '___This is a test___'
        r = slugify(txt)
        self.assertEqual(r, 'this-is-a-test')
        txt = 'one two three four five'
        r = slugify(txt, max_length=13, word_boundary=True, save_order=True)
        self.assertEqual(r, 'one-two-three')
        txt = 'one two three four five'
        r = slugify(txt, max_length=13, word_boundary=True, save_order=False)
        self.assertEqual(r, 'one-two-three')
        txt = 'one two three four five'
        r = slugify(txt, max_length=12, word_boundary=True, save_order=False)
        self.assertEqual(r, 'one-two-four')
        txt = 'one two three four five'
        r = slugify(txt, max_length=12, word_boundary=True, save_order=True)
        self.assertEqual(r, 'one-two')
        txt = 'this has a stopword'
        r = slugify(txt, stopwords=['stopword'])
        self.assertEqual(r, 'this-has-a')
        txt = 'the quick brown fox jumps over the lazy dog'
        r = slugify(txt, stopwords=['the'])
        self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')
        txt = 'Foo A FOO B foo C'
        r = slugify(txt, stopwords=['foo'])
        self.assertEqual(r, 'a-b-c')
        txt = 'Foo A FOO B foo C'
        r = slugify(txt, stopwords=['FOO'])
        self.assertEqual(r, 'a-b-c')
        txt = 'the quick brown fox jumps over the lazy dog in a hurry'
        r = slugify(txt, stopwords=['the', 'in', 'a', 'hurry'])
        self.assertEqual(r, 'quick-brown-fox-jumps-over-lazy-dog')


class SlugUniqueTestCase(TestCase):
    __doc__ = 'Tests for Slug - Unique'

    def test_manager(self):
        name = 'john'
        with self.assertNumQueries(2):
            obj = CoolSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'john')
        with self.assertNumQueries(3):
            obj = CoolSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'john-1')

    def test_start_no(self):
        name = 'Foo Bar'
        with self.assertNumQueries(2):
            obj = AnotherSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'foo-bar')
        with self.assertNumQueries(3):
            obj = AnotherSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'foo-bar-2')
        with self.assertNumQueries(4):
            obj = AnotherSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'foo-bar-3')

    def test_max_length(self):
        name = 'jaja---lol-méméméoo--a'
        obj = TruncatedSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja-lol-mememeoo')
        obj = TruncatedSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja-lol-mememe-2')
        obj = TruncatedSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja-lol-mememe-3')

    def test_max_length_exact_word_boundry(self):
        name = 'jaja---lol-méméméoo--a'
        obj = SmartTruncatedExactWordBoundrySlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja-lol-mememeoo-a')
        obj = SmartTruncatedExactWordBoundrySlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja-lol-mememeoo-9')
        obj = SmartTruncatedExactWordBoundrySlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja-lol-mememeo-10')


class SlugUniqueDifferentSeparatorTestCase(TestCase):
    __doc__ = 'Tests for Slug - Unique with different separator '

    def test_manager(self):
        name = 'john'
        with self.assertNumQueries(2):
            obj = CoolSlugDifferentSeparator.objects.create(name=name)
        self.assertEqual(obj.slug, 'john')
        with self.assertNumQueries(3):
            obj = CoolSlugDifferentSeparator.objects.create(name=name)
        self.assertEqual(obj.slug, 'john_1')
        with self.assertNumQueries(4):
            obj = CoolSlugDifferentSeparator.objects.create(name=name)
        self.assertEqual(obj.slug, 'john_2')

    def test_max_length(self):
        name = 'jaja---lol-méméméoo--a'
        obj = TruncatedSlugDifferentSeparator.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja_lol_mememeoo')
        obj = TruncatedSlugDifferentSeparator.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja_lol_mememe_2')
        obj = TruncatedSlugDifferentSeparator.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja_lol_mememe_3')


class SlugMaxLengthTestCase(TestCase):
    __doc__ = 'Tests for Slug - Max length less than field length'

    def test_manager(self):
        name = 'johnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohnjohn'
        with self.assertNumQueries(2):
            obj = CoolSlug.objects.create(name=name)
        self.assertEqual(obj.slug, name[:200])
        with self.assertNumQueries(3):
            obj = CoolSlug.objects.create(name=name)
        self.assertEqual(obj.slug, name[:198] + '-1')

    def test_max_length_greater_than_field_slug(self):
        name = 'jaja---lol-méméméoo--a-méméméoo'
        obj = AutoTruncatedSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja-lol-m')
        obj = AutoTruncatedSlug.objects.create(name=name)
        self.assertEqual(obj.slug, 'jaja-lol-1')


class ModelInstanceExeptionTestCase(TestCase):

    def test_uuslug_checks_for_model_instance(self):
        self.assertRaises(Exception, uuslug, 'test_slug', CoolSlug)