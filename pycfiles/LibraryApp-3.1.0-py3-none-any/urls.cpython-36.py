# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Documents/LibraryApp/LibAppDjango/catalog/urls.py
# Compiled at: 2019-08-12 04:18:21
# Size of source mod 2**32: 1349 bytes
from django.urls import path, include
from rest_framework import routers
from . import views
urlpatterns = [
 path('', (views.index), name='index'),
 path('books/', (views.BookListView.as_view()), name='books'),
 path('book/<int:pk>', (views.BookDetailView.as_view()), name='book-detail'),
 path('authors/', (views.AuthorListView.as_view()), name='authors'),
 path('author/<int:pk>', (views.AuthorDetailView.as_view()),
   name='author-detail')]
urlpatterns += [
 path('mybooks/', (views.LoanedBooksByUserListView.as_view()), name='my_borrowed')]
urlpatterns += [
 path('api/v1/books/', views.BookViewSet.as_view({'get':'list', 
  'post':'create', 
  'put':'update', 
  'patch':'partial_update', 
  'delete':'destroy'})),
 path('api/v1/authors/', views.AuthorViewSet.as_view({'get':'list', 
  'post':'create', 
  'put':'update', 
  'patch':'partial_update', 
  'delete':'destroy'}))]