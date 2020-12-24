# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/claudiob/Projects/legendary/env/src/radish/radish/features/admin.py
# Compiled at: 2011-07-05 18:36:44
from lettuce import *
from radish.features import base
from radish.settings import *
from django.core.urlresolvers import reverse

@step('I navigate to the admin page')
def i_navigate_to_the_admin_page(step):
    step.given('I access the URL "%s"' % reverse('admin:index'))


@step('I am not logged in(?:| as an admin)$')
def i_am_not_logged_in_as_an_admin(step):
    step.given('I navigate to the admin page')
    step.given('I click on the "Log out" link if exists')


@step('I am logged in(?:| as an admin)$')
def i_am_logged_in_as_an_admin(step):
    step.given('I navigate to the admin page')
    try:
        step.given('I should see the administration panel')
    except:
        step.given('I fill the "username" field with "%s"' % ADMIN_LOGIN)
        step.given('I fill the "password" field with "%s"' % ADMIN_PASSWORD)
        step.given('I click the "Log in" button')


@step('I should see the administration panel')
def i_am_on_the_administration_panel(step):
    step.given('I should see the message "Site administration"')