# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_default_reviewer.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.utils import six
from django.utils.six.moves import zip
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import INVALID_FORM_DATA
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.reviews.models import DefaultReviewer, Group
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import default_reviewer_item_mimetype, default_reviewer_list_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import get_default_reviewer_item_url, get_default_reviewer_list_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceListTests(BaseWebAPITestCase):
    """Testing the DefaultReviewerResource list APIs."""
    fixtures = [
     b'test_users']
    basic_post_fixtures = [b'test_scmtools']
    basic_post_use_admin = True
    sample_api_url = b'default-reviewers/'
    resource = resources.default_reviewer
    test_http_methods = ('POST', )

    @add_fixtures([b'test_scmtools'])
    def test_get(self):
        """Testing the GET default-reviewers/ API"""
        user = User.objects.get(username=b'doc')
        group = Group.objects.create(name=b'group1')
        repository = self.create_repository()
        DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer = DefaultReviewer.objects.create(name=b'default2', file_regex=b'/foo')
        default_reviewer.people.add(user)
        default_reviewer.groups.add(group)
        default_reviewer.repository.add(repository)
        rsp = self.api_get(get_default_reviewer_list_url(), expected_mimetype=default_reviewer_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewers = rsp[b'default_reviewers']
        self.assertEqual(len(default_reviewers), 2)
        self.assertEqual(default_reviewers[0][b'name'], b'default1')
        self.assertEqual(default_reviewers[0][b'file_regex'], b'.*')
        self.assertEqual(default_reviewers[1][b'name'], b'default2')
        self.assertEqual(default_reviewers[1][b'file_regex'], b'/foo')
        users = default_reviewers[1][b'users']
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0][b'title'], user.username)
        groups = default_reviewers[1][b'groups']
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0][b'title'], group.name)
        repos = default_reviewers[1][b'repositories']
        self.assertEqual(len(repos), 1)
        self.assertEqual(repos[0][b'title'], repository.name)

    @add_fixtures([b'test_site'])
    def test_get_with_site(self):
        """Testing the GET default-reviewers/ API with a local site"""
        local_site = self.get_local_site(name=self.local_site_name)
        DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*', local_site=local_site)
        DefaultReviewer.objects.create(name=b'default2', file_regex=b'/foo')
        rsp = self.api_get(get_default_reviewer_list_url(), expected_mimetype=default_reviewer_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewers = rsp[b'default_reviewers']
        self.assertEqual(len(default_reviewers), 1)
        self.assertEqual(default_reviewers[0][b'name'], b'default2')
        self.assertEqual(default_reviewers[0][b'file_regex'], b'/foo')
        self._login_user(local_site=True)
        rsp = self.api_get(get_default_reviewer_list_url(self.local_site_name), expected_mimetype=default_reviewer_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewers = rsp[b'default_reviewers']
        self.assertEqual(len(default_reviewers), 1)
        self.assertEqual(default_reviewers[0][b'name'], b'default1')
        self.assertEqual(default_reviewers[0][b'file_regex'], b'.*')

    @add_fixtures([b'test_site'])
    def test_get_with_site_no_access(self):
        """Testing the GET default-reviewers/ API
        with a local site and Permission Denied error
        """
        self.api_get(get_default_reviewer_list_url(self.local_site_name), expected_status=403)

    @add_fixtures([b'test_scmtools'])
    def test_get_with_repositories(self):
        """Testing the GET default-reviewers/?repositories= API"""
        repository1 = self.create_repository(name=b'repo 1')
        repository2 = self.create_repository(name=b'repo 2')
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer.repository.add(repository1)
        default_reviewer.repository.add(repository2)
        default_reviewer = DefaultReviewer.objects.create(name=b'default2', file_regex=b'/foo')
        default_reviewer.repository.add(repository2)
        rsp = self.api_get(b'%s?repositories=%s' % (
         get_default_reviewer_list_url(), repository2.pk), expected_mimetype=default_reviewer_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewers = rsp[b'default_reviewers']
        self.assertEqual(len(default_reviewers), 2)
        self.assertEqual(default_reviewers[0][b'name'], b'default1')
        self.assertEqual(default_reviewers[1][b'name'], b'default2')
        rsp = self.api_get(b'%s?repositories=%s,%s' % (
         get_default_reviewer_list_url(), repository1.pk,
         repository2.pk), expected_mimetype=default_reviewer_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewers = rsp[b'default_reviewers']
        self.assertEqual(len(default_reviewers), 1)
        self.assertEqual(default_reviewers[0][b'name'], b'default1')

    def test_get_with_users(self):
        """Testing the GET default-reviewers/?users= API"""
        user1 = User.objects.get(username=b'doc')
        user2 = User.objects.get(username=b'dopey')
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer.people.add(user1)
        default_reviewer.people.add(user2)
        default_reviewer = DefaultReviewer.objects.create(name=b'default2', file_regex=b'/foo')
        default_reviewer.people.add(user2)
        rsp = self.api_get(b'%s?users=dopey' % get_default_reviewer_list_url(), expected_mimetype=default_reviewer_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewers = rsp[b'default_reviewers']
        self.assertEqual(len(default_reviewers), 2)
        self.assertEqual(default_reviewers[0][b'name'], b'default1')
        self.assertEqual(default_reviewers[1][b'name'], b'default2')
        rsp = self.api_get(b'%s?users=doc,dopey' % get_default_reviewer_list_url(), expected_mimetype=default_reviewer_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewers = rsp[b'default_reviewers']
        self.assertEqual(len(default_reviewers), 1)
        self.assertEqual(default_reviewers[0][b'name'], b'default1')

    def test_get_with_groups(self):
        """Testing the GET default-reviewers/?groups= API"""
        group1 = Group.objects.create(name=b'group1')
        group2 = Group.objects.create(name=b'group2')
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer.groups.add(group1)
        default_reviewer.groups.add(group2)
        default_reviewer = DefaultReviewer.objects.create(name=b'default2', file_regex=b'/foo')
        default_reviewer.groups.add(group2)
        rsp = self.api_get(b'%s?groups=group2' % get_default_reviewer_list_url(), expected_mimetype=default_reviewer_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewers = rsp[b'default_reviewers']
        self.assertEqual(len(default_reviewers), 2)
        self.assertEqual(default_reviewers[0][b'name'], b'default1')
        self.assertEqual(default_reviewers[1][b'name'], b'default2')
        rsp = self.api_get(b'%s?groups=group1,group2' % get_default_reviewer_list_url(), expected_mimetype=default_reviewer_list_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewers = rsp[b'default_reviewers']
        self.assertEqual(len(default_reviewers), 1)
        self.assertEqual(default_reviewers[0][b'name'], b'default1')

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        if post_valid_data:
            self.create_review_group(name=b'group1', with_local_site=with_local_site)
            self.create_review_group(name=b'group2', with_local_site=with_local_site)
            repo1 = self.create_repository(name=b'Test Repo 1', with_local_site=with_local_site, path=b'test-repo-1')
            repo2 = self.create_repository(name=b'Test Repo 2', with_local_site=with_local_site, path=b'test-repo-2')
            if with_local_site:
                site = self.get_local_site(name=local_site_name)
                site.users.add(User.objects.get(username=b'doc'))
                site.users.add(User.objects.get(username=b'dopey'))
            post_data = {b'name': b'my-default', 
               b'file_regex': b'.*', 
               b'users': b'doc,dopey', 
               b'groups': b'group1,group2', 
               b'repositories': (b',').join([six.text_type(repo1.pk),
                               six.text_type(repo2.pk)])}
        else:
            post_data = {}
        return (
         get_default_reviewer_list_url(local_site_name),
         default_reviewer_item_mimetype,
         post_data,
         [
          local_site_name])

    def check_post_result(self, user, rsp, local_site_name):
        self.assertIn(b'default_reviewer', rsp)
        item_rsp = rsp[b'default_reviewer']
        self.assertEqual(item_rsp[b'name'], b'my-default')
        self.assertEqual(item_rsp[b'file_regex'], b'.*')
        default_reviewer = DefaultReviewer.objects.get(pk=item_rsp[b'id'])
        self.assertEqual(default_reviewer.name, b'my-default')
        self.assertEqual(default_reviewer.file_regex, b'.*')
        if local_site_name:
            self.assertEqual(default_reviewer.local_site.name, local_site_name)
        people = list(default_reviewer.people.all())
        self.assertEqual(len(people), 2)
        self.assertEqual(people[0].username, b'doc')
        self.assertEqual(people[1].username, b'dopey')
        groups = list(default_reviewer.groups.all())
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0].name, b'group1')
        self.assertEqual(groups[1].name, b'group2')
        repos = list(default_reviewer.repository.all())
        self.assertEqual(len(repos), 2)
        self.assertEqual(repos[0].name, b'Test Repo 1')
        self.assertEqual(repos[1].name, b'Test Repo 2')

    @add_fixtures([b'test_users'])
    def test_post_with_defaults(self):
        """Testing the POST default-reviewers/ API with field defaults"""
        self._login_user(admin=True)
        name = b'default1'
        file_regex = b'.*'
        rsp = self.api_post(get_default_reviewer_list_url(), {b'name': name, 
           b'file_regex': file_regex}, expected_mimetype=default_reviewer_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewer = DefaultReviewer.objects.get(pk=rsp[b'default_reviewer'][b'id'])
        self.assertEqual(default_reviewer.local_site, None)
        self.assertEqual(default_reviewer.name, name)
        self.assertEqual(default_reviewer.file_regex, file_regex)
        return

    @add_fixtures([b'test_users'])
    def test_post_with_permission_denied(self):
        """Testing the POST default-reviewers/ API
        with Permission Denied error
        """
        self._login_user()
        self.api_post(get_default_reviewer_list_url(), {b'name': b'default1', 
           b'file_regex': b'.*'}, expected_status=403)

    @add_fixtures([b'test_users', b'test_site'])
    def test_post_with_invalid_regex(self):
        """Testing the POST default-reviewers/ API with an invalid regex"""
        self._login_user(admin=True)
        rsp = self.api_post(get_default_reviewer_list_url(), {b'name': b'default1', 
           b'file_regex': b'\\'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertIn(b'file_regex', rsp[b'fields'])

    @add_fixtures([b'test_users'])
    def test_post_with_invalid_username(self):
        """Testing the POST default-reviewers/ API with invalid username"""
        self._login_user(admin=True)
        rsp = self.api_post(get_default_reviewer_list_url(), {b'name': b'default1', 
           b'file_regex': b'.*', 
           b'users': b'foo'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'users', rsp[b'fields'])

    @add_fixtures([b'test_users', b'test_site'])
    def test_post_with_user_invalid_site(self):
        """Testing the POST default-reviewers/ API
        with user and invalid site
        """
        self._login_user(admin=True)
        local_site = self.get_local_site(name=self.local_site_name)
        rsp = self.api_post(get_default_reviewer_list_url(local_site), {b'name': b'default1', 
           b'file_regex': b'.*', 
           b'users': b'grumpy'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'users', rsp[b'fields'])

    @add_fixtures([b'test_users'])
    def test_post_with_invalid_group(self):
        """Testing the POST default-reviewers/ API with invalid group"""
        self._login_user(admin=True)
        rsp = self.api_post(get_default_reviewer_list_url(), {b'name': b'default1', 
           b'file_regex': b'.*', 
           b'groups': b'foo'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'groups', rsp[b'fields'])

    @add_fixtures([b'test_users', b'test_site'])
    def test_post_with_group_invalid_site(self):
        """Testing the POST default-reviewers/ API
        with group and invalid site
        """
        self._login_user(admin=True)
        local_site = self.get_local_site(name=self.local_site_name)
        Group.objects.create(name=b'group1', local_site=local_site)
        rsp = self.api_post(get_default_reviewer_list_url(), {b'name': b'default1', 
           b'file_regex': b'.*', 
           b'groups': b'group1'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'groups', rsp[b'fields'])

    @add_fixtures([b'test_users'])
    def test_post_with_invalid_repository(self):
        """Testing the POST default-reviewers/ API with invalid repository"""
        self._login_user(admin=True)
        rsp = self.api_post(get_default_reviewer_list_url(), {b'name': b'default1', 
           b'file_regex': b'.*', 
           b'repositories': b'12345'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'repositories', rsp[b'fields'])

    @add_fixtures([b'test_users', b'test_site', b'test_scmtools'])
    def test_post_with_repository_invalid_site(self):
        """Testing the POST default-reviewers/ API
        with repository and invalid site
        """
        repository = self.create_repository(with_local_site=True)
        self._login_user(admin=True)
        rsp = self.api_post(get_default_reviewer_list_url(), {b'name': b'default1', 
           b'file_regex': b'.*', 
           b'repositories': six.text_type(repository.pk)}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'repositories', rsp[b'fields'])


@six.add_metaclass(BasicTestsMetaclass)
class ResourceItemTests(BaseWebAPITestCase):
    """Testing the DefaultReviewerResource item APIs."""
    fixtures = [
     b'test_users']
    basic_get_fixtures = [b'test_scmtools']
    basic_put_fixtures = [b'test_scmtools']
    basic_delete_use_admin = True
    basic_put_use_admin = True
    sample_api_url = b'default-reviewers/<id>/'
    resource = resources.default_reviewer

    def compare_item(self, item_rsp, default_reviewer):
        self.assertEqual(default_reviewer.name, item_rsp[b'name'])
        self.assertEqual(default_reviewer.file_regex, item_rsp[b'file_regex'])
        users = list(default_reviewer.people.all())
        for user_rsp, user in zip(item_rsp[b'users'], users):
            self.assertEqual(user_rsp[b'title'], user.username)

        self.assertEqual(len(item_rsp[b'users']), len(users))
        groups = list(default_reviewer.groups.all())
        for group_rsp, group in zip(item_rsp[b'groups'], groups):
            self.assertEqual(group_rsp[b'title'], group.name)

        self.assertEqual(len(item_rsp[b'groups']), len(groups))
        repos = list(default_reviewer.repository.all())
        for repo_rsp, repo in zip(item_rsp[b'repositories'], repos):
            self.assertEqual(repo_rsp[b'title'], repo.name)

        self.assertEqual(len(item_rsp[b'repositories']), len(repos))

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        if with_local_site:
            local_site = self.get_local_site(name=local_site_name)
        else:
            local_site = None
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*', local_site=local_site)
        return (
         get_default_reviewer_item_url(default_reviewer.pk, local_site_name), [])

    def check_delete_result(self, user):
        self.assertEqual(DefaultReviewer.objects.filter(name=b'default1').count(), 0)

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        if with_local_site:
            default_reviewer.local_site = self.get_local_site(name=local_site_name)
            default_reviewer.save()
        default_reviewer.people.add(User.objects.get(username=b'doc'))
        default_reviewer.groups.add(self.create_review_group(name=b'group1', with_local_site=with_local_site))
        default_reviewer.repository.add(self.create_repository(with_local_site=with_local_site))
        return (
         get_default_reviewer_item_url(default_reviewer.pk, local_site_name),
         default_reviewer_item_mimetype,
         default_reviewer)

    def test_get_not_modified(self):
        """Testing the GET default-reviewers/<id>/ API
        with Not Modified response
        """
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        self._testHttpCaching(get_default_reviewer_item_url(default_reviewer.pk), check_etags=True)

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        if with_local_site:
            local_site = self.get_local_site(name=local_site_name)
            local_site.users.add(User.objects.get(username=b'doc'))
            local_site.users.add(User.objects.get(username=b'dopey'))
            default_reviewer.local_site = local_site
            default_reviewer.save()
        default_reviewer.people.add(User.objects.get(username=b'doc'))
        default_reviewer.groups.add(self.create_review_group(name=b'group1', with_local_site=with_local_site))
        repo1 = self.create_repository(with_local_site=with_local_site, name=b'Test Repo 1', path=b'test-repo-1')
        default_reviewer.repository.add(repo1)
        if put_valid_data:
            self.create_review_group(name=b'group2', with_local_site=with_local_site)
            repo2 = self.create_repository(with_local_site=with_local_site, name=b'Test Repo 2', path=b'test-repo-2')
            put_data = {b'name': b'New name', 
               b'file_regex': b'/foo/', 
               b'users': b'doc,dopey', 
               b'groups': b'group1,group2', 
               b'repositories': (b',').join([six.text_type(repo1.pk),
                               six.text_type(repo2.pk)])}
        else:
            put_data = {}
        return (get_default_reviewer_item_url(default_reviewer.pk, local_site_name),
         default_reviewer_item_mimetype,
         put_data,
         default_reviewer, [])

    def check_put_result(self, user, item_rsp, default_reviewer):
        self.assertEqual(item_rsp[b'name'], b'New name')
        self.assertEqual(item_rsp[b'file_regex'], b'/foo/')
        default_reviewer = DefaultReviewer.objects.get(pk=item_rsp[b'id'])
        self.assertEqual(default_reviewer.name, b'New name')
        self.assertEqual(default_reviewer.file_regex, b'/foo/')
        people = list(default_reviewer.people.all())
        self.assertEqual(len(people), 2)
        self.assertEqual(people[0].username, b'doc')
        self.assertEqual(people[1].username, b'dopey')
        groups = list(default_reviewer.groups.all())
        self.assertEqual(len(groups), 2)
        self.assertEqual(groups[0].name, b'group1')
        self.assertEqual(groups[1].name, b'group2')
        repos = list(default_reviewer.repository.all())
        self.assertEqual(len(repos), 2)
        self.assertEqual(repos[0].name, b'Test Repo 1')
        self.assertEqual(repos[1].name, b'Test Repo 2')

    @add_fixtures([b'test_users'])
    def test_put_with_invalid_username(self):
        """Testing the PUT default-reviewers/<id>/ API with invalid username"""
        self._login_user(admin=True)
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'users': b'foo'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'users', rsp[b'fields'])

    @add_fixtures([b'test_users', b'test_site'])
    def test_put_with_user_invalid_site(self):
        """Testing the PUT default-reviewers/<id>/ API
        with user and invalid site
        """
        self._login_user(admin=True)
        local_site = self.get_local_site(name=self.local_site_name)
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*', local_site=local_site)
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk, self.local_site_name), {b'users': b'grumpy'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'users', rsp[b'fields'])

    @add_fixtures([b'test_users'])
    def test_put_with_invalid_group(self):
        """Testing the PUT default-reviewers/<id>/ API with invalid group"""
        self._login_user(admin=True)
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'groups': b'foo'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'groups', rsp[b'fields'])

    @add_fixtures([b'test_users', b'test_site'])
    def test_put_with_group_invalid_site(self):
        """Testing the PUT default-reviewers/<id>/ API
        with group and invalid site
        """
        self._login_user(admin=True)
        local_site = self.get_local_site(name=self.local_site_name)
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        Group.objects.create(name=b'group1', local_site=local_site)
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'groups': b'group1'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'groups', rsp[b'fields'])

    @add_fixtures([b'test_users'])
    def test_put_with_invalid_repository(self):
        """Testing the PUT default-reviewers/<id>/ API
        with invalid repository
        """
        self._login_user(admin=True)
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'repositories': b'12345'}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'repositories', rsp[b'fields'])

    @add_fixtures([b'test_users', b'test_site', b'test_scmtools'])
    def test_put_with_repository_invalid_site(self):
        """Testing the PUT default-reviewers/<id>/ API
        with repository and invalid site
        """
        repository = self.create_repository(with_local_site=True)
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        self._login_user(admin=True)
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'repositories': six.text_type(repository.pk)}, expected_status=400)
        self.assertIn(b'fields', rsp)
        self.assertIn(b'repositories', rsp[b'fields'])

    @add_fixtures([b'test_users'])
    @webapi_test_template
    def test_put_clear_groups(self):
        """Testing PUT <URL> API with empty groups field"""
        group = Group.objects.create(name=b'group1')
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer.groups.add(group)
        self._login_user(admin=True)
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'file_regex': b'.*', 
           b'name': b'default1', 
           b'groups': b''}, expected_mimetype=default_reviewer_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewer = DefaultReviewer.objects.get(pk=default_reviewer.pk)
        self.assertEqual(list(default_reviewer.groups.all()), [])
        self.assertIn(b'default_reviewer', rsp)
        self.compare_item(rsp[b'default_reviewer'], default_reviewer)

    @add_fixtures([b'test_users'])
    @webapi_test_template
    def test_put_groups_only_commas(self):
        """Testing PUT <URL> API with groups field containing only commas"""
        group = Group.objects.create(name=b'group1')
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer.groups.add(group)
        self._login_user(admin=True)
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'file_regex': b'.*', 
           b'name': b'default1', 
           b'groups': b' , , , '}, expected_mimetype=default_reviewer_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewer = DefaultReviewer.objects.get(pk=default_reviewer.pk)
        self.assertEqual(list(default_reviewer.groups.all()), [])
        self.assertIn(b'default_reviewer', rsp)
        self.compare_item(rsp[b'default_reviewer'], default_reviewer)

    @add_fixtures([b'test_users'])
    @webapi_test_template
    def test_put_clear_users(self):
        """Testing PUT <URL> API with empty users field"""
        doc = User.objects.get(username=b'doc')
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer.people.add(doc)
        self._login_user(admin=True)
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'file_regex': b'.*', 
           b'name': b'default1', 
           b'users': b''}, expected_mimetype=default_reviewer_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewer = DefaultReviewer.objects.get(pk=default_reviewer.pk)
        self.assertEqual(list(default_reviewer.people.all()), [])
        self.assertIn(b'default_reviewer', rsp)
        self.compare_item(rsp[b'default_reviewer'], default_reviewer)

    @add_fixtures([b'test_users'])
    @webapi_test_template
    def test_put_users_only_commas(self):
        """Testing PUT <URL> API with users field containing only commas"""
        doc = User.objects.get(username=b'doc')
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer.people.add(doc)
        self._login_user(admin=True)
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'file_regex': b'.*', 
           b'name': b'default1', 
           b'users': b' , , , '}, expected_mimetype=default_reviewer_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewer = DefaultReviewer.objects.get(pk=default_reviewer.pk)
        self.assertEqual(list(default_reviewer.people.all()), [])
        self.assertIn(b'default_reviewer', rsp)
        self.compare_item(rsp[b'default_reviewer'], default_reviewer)

    @add_fixtures([b'test_users', b'test_scmtools'])
    @webapi_test_template
    def test_put_clear_repositories(self):
        """Testing PUT <URL> API with empty repositories field"""
        repository = self.create_repository()
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer.repository.add(repository)
        self._login_user(admin=True)
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'file_regex': b'.*', 
           b'name': b'default1', 
           b'repositories': b''}, expected_mimetype=default_reviewer_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewer = DefaultReviewer.objects.get(pk=default_reviewer.pk)
        self.assertEqual(list(default_reviewer.repository.all()), [])
        self.assertIn(b'default_reviewer', rsp)
        self.compare_item(rsp[b'default_reviewer'], default_reviewer)

    @add_fixtures([b'test_users', b'test_scmtools'])
    @webapi_test_template
    def test_put_repositories_only_comma(self):
        """Testing PUT <URL> API with repositories field containing only
        commas
        """
        repository = self.create_repository()
        default_reviewer = DefaultReviewer.objects.create(name=b'default1', file_regex=b'.*')
        default_reviewer.repository.add(repository)
        self._login_user(admin=True)
        rsp = self.api_put(get_default_reviewer_item_url(default_reviewer.pk), {b'file_regex': b'.*', 
           b'name': b'default1', 
           b'repositories': b' , , , '}, expected_mimetype=default_reviewer_item_mimetype)
        self.assertIn(b'stat', rsp)
        self.assertEqual(rsp[b'stat'], b'ok')
        default_reviewer = DefaultReviewer.objects.get(pk=default_reviewer.pk)
        self.assertEqual(list(default_reviewer.repository.all()), [])
        self.assertIn(b'default_reviewer', rsp)
        self.compare_item(rsp[b'default_reviewer'], default_reviewer)