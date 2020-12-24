# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ssi/tests.py
# Compiled at: 2011-01-25 14:26:53
from django.test import TestCase, Client
from django.template import Template, Context
from django.core.urlresolvers import reverse
from ssi.utils import generate_ssi_cache_key

class SSITestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ssi_template_rendering(self):
        ssi_fragment = '<b> okidoki </b> {%now "jS F Y H:i"%} Hello {{foo}}'
        template_string = '\n            {% load nginxssi_tags %}\n            {% nginxssi %}' + ssi_fragment + '{% endnginxssi %}\n        '
        template = Template(template_string)
        context = Context({'foo': 'bar'})
        template_response = template.render(context)
        cache_key = generate_ssi_cache_key(ssi_fragment)
        self.assertTrue('<!--# include virtual="/nginxssi/%s/" -->' % cache_key in template_response)
        client = Client()
        response = client.get(reverse('nginxssi', args=(cache_key,)))
        template = Template(ssi_fragment)
        self.assertEquals(response.content.strip(), template.render(context).strip())