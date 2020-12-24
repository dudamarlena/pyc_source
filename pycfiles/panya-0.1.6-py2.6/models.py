# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/panya/models.py
# Compiled at: 2011-05-26 02:47:52
import time
from datetime import datetime
from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import signals
from django.template import Template
from django.utils.encoding import smart_unicode
import secretballot
from panya.managers import PermittedManager
from panya.utils import generate_slug
from photologue.models import ImageModel
from secretballot.models import Vote

class ModelBase(ImageModel):
    objects = models.Manager()
    permitted = PermittedManager()
    state = models.CharField(max_length=32, choices=(
     ('unpublished', 'Unpublished'),
     ('published', 'Published'),
     ('staging', 'Staging')), default='unpublished', help_text="Set the item state. The 'Published' state makes the item visible to the public, 'Unpublished' retracts it and 'Staging' makes the item visible to staff users.", blank=True, null=True)
    publish_on = models.DateTimeField(blank=True, null=True, help_text="Date and time on which to publish this item (state will change to 'published').")
    retract_on = models.DateTimeField(blank=True, null=True, help_text="Date and time on which to retract this item (state will change to 'unpublished').")
    slug = models.SlugField(editable=False, max_length=255, db_index=True, unique=True)
    title = models.CharField(max_length=200, help_text='A short descriptive title.')
    description = models.TextField(help_text='A short description. More verbose than the title but limited to one or two sentences.', blank=True, null=True)
    created = models.DateTimeField('Created Date & Time', blank=True, help_text='Date and time on which this item was created. This is automatically set on creation, but can be changed subsequently.')
    modified = models.DateTimeField('Modified Date & Time', editable=False, help_text='Date and time on which this item was last modified. This is automatically set each time the item is saved.')
    owner = models.ForeignKey(User, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, editable=False, null=True)
    class_name = models.CharField(max_length=32, editable=False, null=True)
    categories = models.ManyToManyField('category.Category', blank=True, null=True, help_text='Categorizing this item.')
    tags = models.ManyToManyField('category.Tag', blank=True, null=True, help_text='Tag this item.')
    sites = models.ManyToManyField('sites.Site', blank=True, null=True, help_text='Makes item eligible to be published on selected sites.')
    publishers = models.ManyToManyField('publisher.Publisher', blank=True, null=True, help_text='Makes item eligible to be published on selected platform.')
    comments_enabled = models.BooleanField(verbose_name='Commenting Enabled', help_text='Enable commenting for this item. Comments will not display when disabled.', default=True)
    anonymous_comments = models.BooleanField(verbose_name='Anonymous Commenting Enabled', help_text='Enable anonymous commenting for this item.', default=True)
    comments_closed = models.BooleanField(verbose_name='Commenting Closed', help_text="Close commenting for this item. Comments will still display, but users won't be able to add new comments.", default=False)
    likes_enabled = models.BooleanField(verbose_name='Liking Enabled', help_text='Enable liking for this item. Likes will not display when disabled.', default=True)
    anonymous_likes = models.BooleanField(verbose_name='Anonymous Liking Enabled', help_text='Enable anonymous liking for this item.', default=True)
    likes_closed = models.BooleanField(verbose_name='Liking Closed', help_text="Close liking for this item. Likes will still display, but users won't be able to the item anymore.", default=False)

    class Meta:
        ordering = ('-created', )

    def as_leaf_class(self):
        """
        Returns the leaf class no matter where the calling instance is in the inheritance hierarchy.
        Inspired by http://www.djangosnippets.org/snippets/1031/
        """
        try:
            return self.__getattribute__(self.class_name.lower())
        except AttributeError:
            content_type = self.content_type
            model = content_type.model_class()
            if model == ModelBase:
                return self
            return model.objects.get(id=self.id)

    def save(self, *args, **kwargs):
        if not self.id and not self.created:
            self.created = datetime.now()
        self.modified = datetime.now()
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        if not self.class_name:
            self.class_name = self.__class__.__name__
        self.slug = generate_slug(self, self.title)
        super(ModelBase, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    @property
    def is_permitted(self):

        def for_site():
            if self.sites.filter(id__exact=settings.SITE_ID):
                return True
            else:
                return False

        if self.state == 'unpublished':
            return False
        if self.state == 'published':
            return for_site()
        if self.state == 'staging':
            if getattr(settings, 'STAGING', False):
                return for_site()
        return False

    @property
    def modelbase_obj(self):
        if self.__class__ == ModelBase:
            return self
        else:
            return self.modelbase_ptr

    def can_vote(self, request):
        """
        Determnines whether or not the current user can vote.
        Returns a bool as well as a string indicating the current vote status,
        with vote status being one of: 'closed', 'disabled', 'auth_required', 'can_vote', 'voted' 
        """
        modelbase_obj = self.modelbase_obj
        if modelbase_obj.likes_closed:
            return (False, 'closed')
        else:
            if not modelbase_obj.likes_enabled:
                return (False, 'disabled')
            if not request.user.is_authenticated() and not modelbase_obj.anonymous_likes:
                return (False, 'auth_required')
            if Vote.objects.filter(object_id=modelbase_obj.id, token=request.secretballot_token).count() == 0:
                return (True, 'can_vote')
            return (False, 'voted')

    def can_comment(self, request):
        modelbase_obj = self.modelbase_obj
        if modelbase_obj.comments_closed:
            return False
        if not modelbase_obj.comments_enabled:
            return False
        if not request.user.is_authenticated() and not modelbase_obj.anonymous_comments:
            return False
        return True

    @property
    def vote_total(self):
        """
        Calculates vote total as total_upvotes - total_downvotes. We are adding a method here instead of relying on django-secretballot's addition since that doesn't work for subclasses.
        """
        modelbase_obj = self.modelbase_obj
        return modelbase_obj.votes.filter(vote=+1).count() - modelbase_obj.votes.filter(vote=-1).count()

    @property
    def comment_count(self):
        """
        Counts total number of comments on ModelBase object.
        Comments should always be recorded on ModelBase objects.
        """
        comment_model = comments.get_model()
        modelbase_content_type = ContentType.objects.get(app_label='panya', model='modelbase')
        qs = comment_model.objects.filter(content_type__in=[
         self.content_type, modelbase_content_type], object_pk=smart_unicode(self.pk), site__pk=settings.SITE_ID)
        field_names = [ f.name for f in comment_model._meta.fields ]
        if 'is_public' in field_names:
            qs = qs.filter(is_public=True)
        if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
            qs = qs.filter(is_removed=False)
        return qs.count()


def set_managers(sender, **kwargs):
    """
    Make sure all classes have the appropriate managers 
    """
    cls = sender
    if issubclass(cls, ModelBase):
        cls.add_to_class('permitted', PermittedManager())


signals.class_prepared.connect(set_managers)
secretballot.enable_voting_on(ModelBase, total_name='secretballot_added_vote_total')