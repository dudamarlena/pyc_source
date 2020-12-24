# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/customcontent/models.py
# Compiled at: 2011-05-29 08:44:55
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class ContentManager(models.Manager):

    def get_query_set(self):
        return super(ContentManager, self).get_query_set().filter(is_active=True)


class CustomContent(models.Model):
    """
        Represents an a set of items which are rendered out onto the page
        for a given url or tied to an object which can be used in templates
        or automatically added via middleware.
    """
    MATCHFMT_CHOICES = (('s', 'Simple string match'), )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_active.help_text = 'Whether or not this enabled on site'
    preview = models.BooleanField(default=True)
    preview.help_text = 'If enabled then a logged in user will see this regardless of if it is active'
    path_to_match = models.CharField(max_length=200, blank=True, null=True)
    match_format = models.CharField(choices=MATCHFMT_CHOICES, default='s', max_length=1)
    exact = models.BooleanField(default=False, editable=False)
    exact.help_text = 'Whether or not to show for all urls including fragments'
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    css = models.TextField(blank=True, null=True)
    css.help_text = 'CSS to include in the head of the template (inline)'
    js = models.TextField(blank=True, null=True)
    js.help_text = 'Javascript to include in the head of the template (inline)'
    extra_head = models.TextField(blank=True, null=True)
    extra_head.help_text = 'Extra tags to put into head before body'
    objects = models.Manager()
    live = ContentManager()

    class Meta:
        ordering = ('path_to_match', )

    def __unicode__(self):
        return '%s - %s' % (self.name, self.path_to_match)

    @staticmethod
    def find(request, exact=False):
        """
            Returns a CustomContent object(s) based on the current request
        """
        path = request.path
        if settings.MEDIA_URL in path:
            return None
        else:
            if request.user.is_authenticated():
                items = CustomContent.objects.all().filter(preview=True)
            else:
                items = CustomContent.live.all()
            if exact:
                items = items.filter(path_to_match=path)
                return items
            split_paths = path.split('/')
            paths = list()
            for cnt, path in enumerate(split_paths):
                paths.append(('/').join(split_paths[:cnt]) + '/')

            items = items.filter(path_to_match__in=paths)
            return items


class CustomItem(models.Model):
    """
        Holds some code in an optional container div for outputting onto
        a page defined via a CustomContent instance
    """
    CONTAINTAG_CHOICES = (
     ('div', 'div'),
     ('ul', 'ul'),
     ('p', 'p'))
    content = models.ForeignKey(CustomContent)
    container_tag = models.CharField(max_length=30, choices=CONTAINTAG_CHOICES, default='div', null=True, blank=True)
    container_tag.help_text = 'An optional element to contain your code in'
    container_id = models.CharField(blank=True, null=True, max_length=50)
    container_id.help_text = 'Your container elements ID'
    container_classes = models.CharField(blank=True, null=True, max_length=200)
    container_classes.help_text = 'A list of classes to add to the container'
    code = models.TextField()
    code.help_text = 'The HTML to output for this item'
    target_element = models.CharField(max_length=50, null=True, blank=True)
    target_element.help_text = 'If using middleware, insert this item at this elements position'
    target_position = models.BooleanField(default=False)
    target_position.help_text = 'If enabled item is positioned *before* target element'

    def render(self):
        wrapper = '<%(tag)s id="%(id)s" class="%(classes)s">%(code)s</%(tag)s>'
        if self.container_tag:
            return wrapper % {'tag': self.container_tag, 
               'code': self.code, 
               'classes': self.container_classes, 
               'id': self.container_id}
        else:
            return self.code