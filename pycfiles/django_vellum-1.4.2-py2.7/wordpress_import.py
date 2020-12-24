# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/management/commands/wordpress_import.py
# Compiled at: 2012-04-05 15:23:47
"""
Import Wordpress posts from an XML file into django-vellum

To generate the XML file, login to the Wordpress Dashboard. Navigate to
    Tools -> Export
and select "Posts" rather than "All content".

Props to:
    http://blog.sejo.be/2010/02/14/import-wordpress-django-mingus/
"""
from optparse import make_option
from datetime import datetime
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from vellum.models import Post, Category

class Command(BaseCommand):
    help = 'Imports Wordpress posts from an XML file into django-vellum'
    args = 'filename.xml'
    option_list = BaseCommand.option_list + (
     make_option('--excerpt', action='store_true', dest='excerpt', default=False, help="Automagically search the post body for the\n                         <!--more--> quicktag and place anything preceeding the\n                         tag into the post's tease field."),)

    def handle(self, *args, **options):
        try:
            file = args[0]
        except IndexError:
            raise CommandError('No file was specified')

        try:
            tree = ET.parse(file)
        except IOError:
            raise CommandError('%s could not be found' % file)

        wp = 'http://wordpress.org/export/1.1/'
        for item in tree.findall('channel/item'):
            slug = item.find('{%s}post_name' % wp).text
            if slug is None:
                slug = slugify(item.find('title').text)
            print 'Importing post "%s"...' % slug
            try:
                post = Post.objects.get(slug=slug)
            except:
                post = Post()
                post.title = item.find('title').text
                post.slug = slug
                post.body = item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text
                post.created = item.find('{%s}post_date' % wp).text
                if item.find('{%s}status' % wp).text == 'publish':
                    post.status = 2
                else:
                    post.status = 1
                    post.created = datetime.now()
                post.publish = post.created
                if options['excerpt']:
                    partition = post.body.partition('<!--more-->')
                    if partition[2]:
                        post.tease = partition[0]
                post.save()

            descriptors = item.findall('category')
            categories = []
            for descriptor in descriptors:
                if descriptor.attrib['domain'] == 'post_tag':
                    post.tags.add(descriptor.text)
                if descriptor.attrib['domain'] == 'category':
                    category = descriptor.text
                    try:
                        cat = Category.objects.get(slug=slugify(category))
                    except:
                        cat = Category(title=category, slug=slugify(category))
                        cat.save()

                    post.categories.add(cat)

            post.save()
            comments = item.findall('{%s}comment' % wp)
            for comment in comments:
                email = comment.find('{%s}comment_author_email' % wp).text
                if email is None:
                    continue
                c = Comment()
                c.user_name = comment.find('{%s}comment_author' % wp).text
                c.user_email = comment.find('{%s}comment_author_email' % wp).text
                c.comment = comment.find('{%s}comment_content' % wp).text
                c.submit_date = comment.find('{%s}comment_date' % wp).text
                c.content_type = ContentType.objects.get(app_label='blog', model='post')
                c.object_pk = post.id
                c.site_id = Site.objects.get_current().id
                user_url = comment.find('{%s}comment_author_url' % wp).text
                if user_url:
                    c.user_url = user_url
                c.save()

        return