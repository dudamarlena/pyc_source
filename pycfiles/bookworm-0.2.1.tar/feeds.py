# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/booki/portal/feeds.py
# Compiled at: 2012-02-14 23:34:00
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils import feedgenerator
from django.contrib.auth.models import User
from booki.editor import models

class BookFeedRSS(Feed):
    """
    This represents RSS feed for a book.
    """

    def get_object(self, request, bookid):
        return get_object_or_404(models.Book, url_title=bookid)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.title

    def items(self, obj):
        return models.ChapterHistory.objects.raw('SELECT editor_chapterhistory.* FROM editor_chapterhistory LEFT OUTER JOIN editor_chapter ON (editor_chapter.id=editor_chapterhistory.chapter_id)  WHERE editor_chapter.book_id=%s  ORDER BY editor_chapterhistory.modified DESC LIMIT 50', (obj.id,))

    def item_title(self, item):
        return item.chapter.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.chapter.get_absolute_url()

    def item_author_name(self, item):
        return item.user.first_name

    def item_author_email(self, item):
        return item.user.email

    def item_author_link(self, item):
        return '/accounts/%s/' % item.user.username

    def item_pubdate(self, item):
        return item.modified


class BookFeedAtom(BookFeedRSS):
    """
    This represents Atom feed for a book.
    """
    feed_type = feedgenerator.Atom1Feed


class ChapterFeedRSS(Feed):
    """
    This represents RSS feed for a chapter.
    """

    def get_object(self, request, bookid, chapterid):
        return get_object_or_404(models.Chapter, book__url_title=bookid, url_title=chapterid)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.title

    def items(self, obj):
        return models.ChapterHistory.objects.raw('SELECT editor_chapterhistory.* FROM editor_chapterhistory LEFT OUTER JOIN editor_chapter ON (editor_chapter.id=editor_chapterhistory.chapter_id)  WHERE editor_chapter.id=%s ORDER BY editor_chapterhistory.modified DESC LIMIT 50', (obj.id,))

    def item_title(self, item):
        return item.chapter.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.chapter.get_absolute_url()

    def item_author_name(self, item):
        return item.user.first_name

    def item_author_email(self, item):
        return item.user.email

    def item_author_link(self, item):
        return '/accounts/%s/' % item.user.username

    def item_pubdate(self, item):
        return item.modified


class ChapterFeedAtom(ChapterFeedRSS):
    """
    This represents Atom feed for a chapter.
    """
    feed_type = feedgenerator.Atom1Feed


class UserFeedRSS(Feed):
    """
    This represents RSS feed for a user.
    """

    def get_object(self, request, userid):
        return get_object_or_404(User, username=userid)

    def title(self, obj):
        return obj.username or obj.first_name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return obj.username or obj.first_name

    def items(self, obj):
        return models.ChapterHistory.objects.raw('SELECT editor_chapterhistory.* FROM editor_chapterhistory LEFT OUTER JOIN editor_chapter ON (editor_chapter.id=editor_chapterhistory.chapter_id) LEFT OUTER JOIN editor_book ON (editor_book.id=editor_chapter.book_id) WHERE editor_chapterhistory.user_id=%s AND editor_book.hidden=FALSE ORDER BY editor_chapterhistory.modified DESC LIMIT 50', (obj.id,))

    def item_title(self, item):
        return item.chapter.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        return item.chapter.get_absolute_url()

    def item_author_name(self, item):
        return item.user.first_name

    def item_author_email(self, item):
        return item.user.email

    def item_author_link(self, item):
        return '/accounts/%s/' % item.user.username

    def item_pubdate(self, item):
        return item.modified


class UserFeedAtom(UserFeedRSS):
    """
    This represents Atom feed for a user.
    """
    feed_type = feedgenerator.Atom1Feed