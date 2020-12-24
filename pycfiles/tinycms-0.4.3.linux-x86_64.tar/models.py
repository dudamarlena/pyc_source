# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms/models.py
# Compiled at: 2014-11-22 22:14:04
from django.db import models
from django.utils import translation
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from mptt.models import MPTTModel, TreeForeignKey
try:
    LANGUAGES = settings.LANGUAGES
except:
    LANGUAGES = (
     (
      settings.LANGUAGE_CODE, settings.LANGUAGE_CODE),)

try:
    TEMPLATES = settings.TINYCMS_TEMPLATES
except:
    TEMPLATES = (('tinycms/test_template.html', 'test_template'), )

class ContentInheritanceList(object):
    overwrite_classes = []

    @classmethod
    def registerModelInheritance(cls, classname):
        cls.overwrite_classes.insert(0, classname.lower())

    @classmethod
    def getInheritanceObject(cls, targetContent):
        for item in cls.overwrite_classes:
            try:
                result = getattr(targetContent, item)
                return result
            except:
                pass

        return


class Page(MPTTModel):
    """Class of web page.

    variables:
    slug -- A part of url.
    template -- Django template for this page.
    url_overwrite -- Url of this page.  When url_overwrite configured, slug is ignored.
    is_active -- When True, this page can be seen.
    parent -- Mptt foreign key for parent.
    """
    slug = models.CharField(max_length=512)
    template = models.CharField(max_length=1024, choices=TEMPLATES)
    url_overwrite = models.CharField(max_length=2048, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = [
         'slug']

    def __unicode__(self):
        return self.slug

    def get_url(self):
        """Return url of this page.
        """
        if self.url_overwrite != None and self.url_overwrite != '':
            tempurl = self.url_overwrite
            if tempurl[0] == '/':
                tempurl = tempurl[1:]
            return tempurl
        tempurl = ''
        if self.parent:
            tempurl = self.parent.get_url()
        tempslug = self.slug
        if tempslug[0] == '/':
            tempslug = tempslug[1:]
        if tempslug != '' and tempslug[(-1)] != '/':
            tempslug = tempslug + '/'
        tempurl += tempslug
        return tempurl
        return

    def get_absolute_url(self):
        temp = self.get_url()
        return reverse('tinycms_show_page', kwargs={'url': temp})

    def render(self, request, dics={}):
        """ Return HttpResponse of this page.

        Arguments:
        request -- HttpRequest
        dics -- Special Key,Value for template
        """
        tempDic = {}
        for key, val in dics.items():
            tempDic[key] = val

        if not self.is_active:
            raise Http404
        lang = translation.get_language()
        contents = Content.objects.filter(page=self, language=lang)
        for item in contents:
            if item.value_name not in tempDic:
                tempDic[item.value_name] = []
            tempDic[item.value_name].append(item.render())

        tempDic['page'] = self
        return render(request, self.template, tempDic)

    def save(self):
        """Deplicate check and add url
        """
        if not Dispatcher.checkValid(self):
            raise Exception('Duplicated url')
        super(Page, self).save()
        Dispatcher.register()


class Content(models.Model):
    """Contents of a page.

    Variables:
    page -- Foreign key for page
    value_name -- This content will be passed by {value_name:content} to template.
    language -- Language of this content
    content -- HTML content.
    """
    page = models.ForeignKey('Page', related_name='contents')
    value_name = models.CharField(max_length=256)
    language = models.CharField(max_length=256, choices=LANGUAGES)
    content = models.TextField(default='')

    def __unicode__(self):
        return unicode(self.page) + ':' + unicode(self.value_name) + ':' + unicode(self.language)

    def render(self):
        """Return HTML string.
        """
        target = ContentInheritanceList.getInheritanceObject(self)
        if target == None:
            return self.content
        else:
            return target.render()
            return


class Dispatcher(object):
    """ URL dispatcher.
    """
    dispatchURLs = None

    @classmethod
    def checkValid(cls, item):
        """Check item's url exists or not.

        Variables:
        item -- Page object.
        """
        if not (
         isinstance(item, Page), 'item must Page object'):
            raise AssertionError
            if cls.dispatchURLs == None:
                cls.register()
            url = item.get_url()
            if url in cls.dispatchURLs and cls.dispatchURLs[url] != item:
                return False
        return True

    @classmethod
    def dispatch(cls, url, request):
        """ Dispatch url and return HttpResponse

        Variables:
        url -- url string.
        request -- HttpRequest
        """
        if cls.dispatchURLs == None:
            cls.register()
        if url in cls.dispatchURLs:
            return cls.dispatchURLs[url].render(request)
        else:
            cls.register()
            if url in cls.dispatchURLs:
                return cls.dispatchURLs[url].render(request)
            raise Http404
            return

    @classmethod
    def clear(cls):
        """ Delete dispatchURLs
        """
        cls.dispatchURLs = {}

    @classmethod
    def register(cls):
        """Generate URL list.
        """
        cls.clear()
        page_roots = Page.objects.root_nodes()
        for item in page_roots:
            cls.generate_url(item)

    @classmethod
    def generate_url(cls, node):
        if node.is_active:
            cls.dispatchURLs[node.get_url()] = node
            for item in node.get_children():
                cls.generate_url(item)