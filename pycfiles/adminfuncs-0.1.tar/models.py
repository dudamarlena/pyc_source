# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/user/workspace/myproject/dajngoadmin/blog/models.py
# Compiled at: 2017-06-16 07:06:15
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from multiselectfield import MultiSelectField
import PIL.Image as Image
from django.template.defaultfilters import slugify
import re

class Blog(models.Model):
    BOOL_CHOICES = (
     (
      True, 'Approved'), (False, 'Pending'))
    META_CHECKBOX = (('1', 'Allow search engines to index this page (assumed).'),
     ('2', 'Allow search engines to follow links on this page (assumed).'),
     ('3', 'Prevents search engines from indexing this page.'),
     ('4', 'Prevents search engines from following links on this page.'))
    id = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True, max_length=255)
    title = models.CharField(max_length=160)
    location = models.CharField(max_length=255)
    short_description = RichTextUploadingField()
    description = RichTextUploadingField()
    author = models.CharField(max_length=50)
    upload_image = models.ImageField(help_text='Image should be of 2900 x 1660 px')
    created_date = models.DateTimeField(blank=True, null=True)
    modified_date = models.DateTimeField(blank=True, null=True, default='')
    soft_delete = models.CharField(max_length=5, default=1)
    meta_title = models.CharField(max_length=255, blank=True, default='')
    meta_keywords = models.CharField(max_length=255, blank=True, default='')
    meta_description = models.TextField(max_length=955, blank=True, default='')
    og_title = models.CharField(max_length=255, blank=True, default='')
    og_description = models.TextField(max_length=955, blank=True, default='')
    og_url = models.CharField(max_length=255, blank=True, default='')
    canonical_url = models.CharField(max_length=255, blank=True, default='')
    meta_robot = MultiSelectField(choices=META_CHECKBOX, max_length=255, blank=True, null=True)
    status = models.BooleanField(choices=BOOL_CHOICES, default=False)

    class Meta:
        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'
        permissions = (('can_approve', 'Can Approve the Blog'), )

    def __unicode__(self):
        return self.title

    def get_thumb(self):
        return '/uploads/%s' % self.photo_thumb

    def get_medium(self):
        return '/uploads/%s' % self.photo_medium

    def get_original(self):
        return '/uploads/%s' % self.upload_image

    def save(self):
        sizes = {'thumbnail': {'height': 137, 'width': 336}}
        replaced = re.sub('[!@#$%^&*/?<>:;]', '-', self.title)
        get_slugs = Blog.objects.values_list('slug')
        get_ids = Blog.objects.values_list('id')
        get_list = []
        for item in list(get_ids):
            get_list.append(item[0])

        self.slug = slugify(replaced)
        for item in list(get_slugs):
            if item[0] == slugify(replaced):
                if self.id not in get_list:
                    import random
                    random_digit = random.randint(0, 999)
                    self.slug = slugify(replaced + str(random_digit))

        super(Blog, self).save()
        photopath = str(self.upload_image.path)
        im = Image.open(photopath)
        extension = photopath.rsplit('.', 1)[1]
        filename = photopath.rsplit('/', 1)[1].rsplit('.', 1)[0]
        fullpath = photopath.rsplit('/', 1)[0]
        if extension not in ('jpg', 'jpeg', 'gif', 'png', 'JPG', 'PNG', 'GIF', 'JPEG'):
            sys.exit()
        im.thumbnail((sizes['thumbnail']['width'],
         sizes['thumbnail']['height']), Image.ANTIALIAS)
        thumbname = 'listing_' + filename + '.' + extension
        im.save(fullpath + '/' + thumbname)
        super(Blog, self).save()