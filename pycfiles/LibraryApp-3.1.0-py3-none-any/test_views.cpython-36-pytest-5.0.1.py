# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Documents/LibraryApp/LibAppDjango/catalog/tests/test_views.py
# Compiled at: 2019-08-12 04:51:41
# Size of source mod 2**32: 9582 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from django.test import TestCase
from catalog.models import Author
from django.urls import reverse
import datetime
from django.utils import timezone
from catalog.models import BookInstance, Book, Genre, Language
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

class BookListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_books = 13
        for book_id in range(number_of_books):
            Book.objects.create(title=('testBook {0}'.format(book_id)), isbn=('testIsbn {0}'.format(book_id)))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/books/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/book_list.html')

    def test_pagination_is_four(self):
        response = self.client.get(reverse('books'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['book_list']) == 4)

    def test_lists_all_books(self):
        response = self.client.get(reverse('books') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['book_list']) == 4)


class TestPage(TestCase):

    def test_index_page(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13
        for author_id in range(number_of_authors):
            Author.objects.create(first_name=('Christian {0}'.format(author_id)), last_name=('Surname {0}'.format(author_id)))

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_four(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['author_list']) == 4)

    def test_lists_all_authors(self):
        response = self.client.get(reverse('authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['author_list']) == 4)


class LoanedBookInstancesByUserListViewTest(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1',
          password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2',
          password='2HJ1vRV0Z&3iD')
        test_user1.save()
        test_user2.save()
        test_author = Author.objects.create(first_name='John',
          last_name='Smith')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(title='Book Title',
          summary='My book summary',
          isbn='ABCDEFG',
          author=test_author,
          language=test_language)
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book)
        test_book.save()
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.now() + datetime.timedelta(days=(book_copy % 5))
            if book_copy % 2:
                the_borrower = test_user1
            else:
                the_borrower = test_user2
            status = 'm'
            BookInstance.objects.create(book=test_book, imprint='Unlikely Imprint, 2016',
              due_back=return_date,
              borrower=the_borrower,
              status=status)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my_borrowed'))
        self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='testuser1',
          password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my_borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/bookinstance_list_borrowed_user.html')

    def test_only_borrowed_books_in_list(self):
        self.client.login(username='testuser1',
          password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my_borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bookinstance_list' in response.context)
        self.assertEqual(len(response.context['bookinstance_list']), 0)
        get_ten_books = BookInstance.objects.all()[:10]
        for copy in get_ten_books:
            copy.status = 'o'
            copy.save()

        response = self.client.get(reverse('my_borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bookinstance_list' in response.context)
        for bookitem in response.context['bookinstance_list']:
            self.assertEqual(response.context['user'], bookitem.borrower)
            self.assertEqual('o', bookitem.status)

    def test_pages_paginated_to_ten(self):
        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()

        self.client.login(username='testuser1',
          password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my_borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['bookinstance_list']), 10)

    def test_pages_ordered_by_due_date(self):
        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()

        self.client.login(username='testuser1',
          password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('my_borrowed'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['bookinstance_list']), 10)
        last_date = 0
        for copy in response.context['bookinstance_list']:
            if last_date == 0:
                last_date = copy.due_back
            else:
                self.assertTrue(last_date <= copy.due_back)