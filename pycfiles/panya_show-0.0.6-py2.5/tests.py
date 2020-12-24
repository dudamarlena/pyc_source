# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/show/tests.py
# Compiled at: 2010-08-24 03:41:12
import unittest
from django.conf import settings
from django.contrib.sites.models import Site
from show.models import ShowContributor, Credit, Show

class ShowTestCase(unittest.TestCase):

    def test_get_primary_contributors(self):
        web_site = Site(domain='web.address.com')
        web_site.save()
        settings.SITE_ID = web_site.id
        show = Show(title='title')
        show.save()
        contributor1 = ShowContributor(title='title', state='published')
        contributor1.save()
        contributor1.sites.add(web_site)
        contributor2 = ShowContributor(title='title', state='published')
        contributor2.save()
        contributor2.sites.add(web_site)
        contributor3 = ShowContributor(title='title', state='published')
        contributor3.save()
        contributor3.sites.add(web_site)
        contributor4 = ShowContributor(title='title', state='published')
        contributor4.save()
        contributor4.sites.add(web_site)
        unpublished_contributor = ShowContributor(title='title')
        unpublished_contributor.save()
        Credit(show=show, contributor=contributor1, role=2).save()
        Credit(show=show, contributor=contributor2, role=10).save()
        Credit(show=show, contributor=contributor3, role=2).save()
        Credit(show=show, contributor=unpublished_contributor, role=2).save()
        Credit(show=show, contributor=contributor4).save()
        primary_contributors = show.get_primary_contributors()
        self.failUnless(contributor1 in primary_contributors)
        self.failUnless(contributor3 in primary_contributors)
        self.failIf(contributor2 in primary_contributors)
        self.failIf(unpublished_contributor in primary_contributors)
        self.failIf(contributor4 in primary_contributors)

    def test_is_contributor_name_in_title(self):
        show = Show(title='The Contributor Title Show')
        show.save()
        matching_contributor = ShowContributor(title='       ConTRIbutoR Title            ')
        matching_contributor.save()
        nonmatching_contributor = ShowContributor(title='  Foo Bar   ')
        nonmatching_contributor.save()
        self.failUnless(show.is_contributor_title_in_title(matching_contributor))
        self.failIf(show.is_contributor_title_in_title(nonmatching_contributor))