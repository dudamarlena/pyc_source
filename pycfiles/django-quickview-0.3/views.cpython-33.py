# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Dev\python\django-quickview\docs\examplesite\friendslist\views.py
# Compiled at: 2013-02-26 03:19:44
# Size of source mod 2**32: 1703 bytes
from quickview import ModelQuickView
from friendslist.models import Spew, Friend, Comment
from quickview import ModelQuickView, PreSaveException

class FriendView(ModelQuickView):
    model = Friend
    use_dynamic_ajax_page = True
    use_pagination = True
    items_per_page = 5
    form_fields_to_exclude = ('added_by', 'added')

    @classmethod
    def pre_save(cls, request, obj):
        if not request.user.is_authenticated():
            raise PreSaveException('Must be logged in to add friends.')
        obj.added_by = request.user

    @classmethod
    def get_context(cls, request, *args, **kwargs):
        return {'user': request.user}

    @classmethod
    def view_add_comment(cls, request):
        if request.POST:
            comment = Comment.objects.create(author=request.POST.get('author'), text=request.POST.get('text'), friend=Friend.objects.get(pk=request.POST.get('friend_id')))
            return cls.list(request)
        return cls.render(request, 'comment.html')

    @classmethod
    def view_special(cls, request, friend_id, friends_name):
        return cls.list(request)


class SpewView(ModelQuickView):
    model = Spew
    use_dynamic_ajax_page = True
    use_pagination = True
    items_per_page = 5
    authentication_required = True
    form_fields_to_exclude = ('author', )

    @classmethod
    def get_context(cls, request, *args, **kwargs):
        return {'user': request.user}

    @classmethod
    def pre_save(cls, request, obj):
        obj.author = request.user