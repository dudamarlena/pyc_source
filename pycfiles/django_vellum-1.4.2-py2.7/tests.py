# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vellum/tests.py
# Compiled at: 2012-04-05 15:23:29
"""
>>> from django.test import Client
>>> from vellum.models import Post, Category
>>> import datetime
>>> from django.core.urlresolvers import reverse
>>> client = Client()

>>> category = Category(title='Django', slug='django')
>>> category.save()
>>> category2 = Category(title='Rails', slug='rails')
>>> category2.save()

>>> post = Post(title='DJ Ango', slug='dj-ango', body='Yo DJ! Turn that music up!', status=2, publish=datetime.datetime(2008,5,5,16,20))
>>> post.save()

>>> post2 = Post(title='Where my grails at?', slug='where', body='I Can haz Holy plez?', status=2, publish=datetime.datetime(2008,4,2,11,11))
>>> post2.save()

>>> post.categories.add(category)
>>> post2.categories.add(category2)

>>> response = client.get(reverse('blog_index'))
>>> response.context[0]['object_list']
[<Post: DJ Ango>, <Post: Where my grails at?>]
>>> response.status_code
200

>>> response = client.get(reverse('blog_category_list'))
>>> response.context[0]['object_list']
[<Category: Django>, <Category: Rails>]
>>> response.status_code
200

>>> response = client.get(category.get_absolute_url())
>>> response.context[0]['object_list']
[<Post: DJ Ango>]
>>> response.status_code
200

>>> response = client.get(post.get_absolute_url())
>>> response.context[0]['object']
<Post: DJ Ango>
>>> response.status_code
200

>>> response = client.get(reverse('blog_search'), {'q': 'DJ'})
>>> response.context[0]['object_list']
[<Post: DJ Ango>]
>>> response.status_code
200
>>> response = client.get(reverse('blog_search'), {'q': 'Holy'})
>>> response.context[0]['object_list']
[<Post: Where my grails at?>]
>>> response.status_code
200
>>> response = client.get(reverse('blog_search'), {'q': ''})
>>> response.context[0]['message']
'Search term was too vague. Please try again.'

>>> response = client.get(reverse('blog_detail', args=[2008, 'apr', 2, 'where']))
>>> response.context[0]['object']
<Post: Where my grails at?>
>>> response.status_code
200
"""