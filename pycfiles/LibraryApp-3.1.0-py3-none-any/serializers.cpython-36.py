# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Documents/LibraryApp/LibAppDjango/catalog/serializers.py
# Compiled at: 2019-07-29 10:10:34
# Size of source mod 2**32: 402 bytes
from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('title', 'author', 'summary', 'isbn', 'genre', 'language')


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('first_name', 'last_name')