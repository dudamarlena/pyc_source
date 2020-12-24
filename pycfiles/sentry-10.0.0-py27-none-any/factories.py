# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/testutils/factories.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function, unicode_literals
from django.conf import settings
import copy, io, os, petname, random, six, warnings
from importlib import import_module
from django.utils import timezone
from django.utils.text import slugify
from hashlib import sha1
from loremipsum import Generator
from uuid import uuid4
from sentry.event_manager import EventManager
from sentry.constants import SentryAppStatus
from sentry.incidents.models import Incident, IncidentGroup, IncidentProject, IncidentSeen, IncidentActivity
from sentry.mediators import sentry_apps, sentry_app_installations, sentry_app_installation_tokens, service_hooks
from sentry.models import Activity, Environment, Event, EventError, Group, Organization, OrganizationMember, OrganizationMemberTeam, Project, ProjectBookmark, Team, User, UserEmail, Release, Commit, ReleaseCommit, CommitAuthor, Repository, CommitFileChange, ProjectDebugFile, File, UserPermission, EventAttachment, UserReport, PlatformExternalIssue
from sentry.models.integrationfeature import Feature, IntegrationFeature
from sentry.utils import json
from sentry.utils.canonical import CanonicalKeyDict
loremipsum = Generator()

def get_fixture_path(name):
    return os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, b'tests', b'fixtures', name)


def make_sentence(words=None):
    if words is None:
        words = int(random.weibullvariate(8, 3))
    return (b' ').join(random.choice(loremipsum.words) for _ in range(words))


def make_word(words=None):
    if words is None:
        words = int(random.weibullvariate(8, 3))
    return random.choice(loremipsum.words)


DEFAULT_EVENT_DATA = {b'extra': {b'loadavg': [
                         0.97607421875, 0.88330078125, 0.833984375], 
              b'sys.argv': [
                          b'/Users/dcramer/.virtualenvs/sentry/bin/raven',
                          b'test',
                          b'https://ebc35f33e151401f9deac549978bda11:f3403f81e12e4c24942d505f086b2cad@sentry.io/1'], 
              b'user': b'dcramer'}, 
   b'modules': {b'raven': b'3.1.13'}, b'request': {b'cookies': {}, b'data': {}, b'env': {}, b'headers': {}, b'method': b'GET', 
                b'query_string': b'', 
                b'url': b'http://example.com'}, 
   b'stacktrace': {b'frames': [
                             {b'abs_path': b'www/src/sentry/models/foo.py', 
                                b'context_line': b'                        string_max_length=self.string_max_length)', 
                                b'filename': b'sentry/models/foo.py', 
                                b'function': b'build_msg', 
                                b'in_app': True, 
                                b'lineno': 29, 
                                b'module': b'raven.base', 
                                b'post_context': [
                                                b'                },',
                                                b'            })',
                                                b'',
                                                b"        if 'stacktrace' in data:",
                                                b'            if self.include_paths:'], 
                                b'pre_context': [
                                               b'',
                                               b'            data.update({',
                                               b"                'stacktrace': {",
                                               b"                    'frames': get_stack_info(frames,",
                                               b'                        list_max_length=self.list_max_length,'], 
                                b'vars': {b'culprit': b'raven.scripts.runner', 
                                          b'date': b'datetime.datetime(2013, 2, 14, 20, 6, 33, 479471)', 
                                          b'event_id': b'598fb19363e745ec8be665e6ba88b1b2', 
                                          b'event_type': b'raven.events.Message', 
                                          b'frames': b'<generator object iter_stack_frames at 0x103fef050>', 
                                          b'handler': b'<raven.events.Message object at 0x103feb710>', 
                                          b'k': b'logentry', 
                                          b'public_key': None, 
                                          b'result': {b'logentry': b"{'message': 'This is a test message generated using ``raven test``', 'params': []}"}, 
                                          b'self': b'<raven.base.Client object at 0x104397f10>', 
                                          b'stack': True, 
                                          b'tags': None, 
                                          b'time_spent': None}},
                             {b'abs_path': b'/Users/dcramer/.virtualenvs/sentry/lib/python2.7/site-packages/raven/base.py', 
                                b'context_line': b'                        string_max_length=self.string_max_length)', 
                                b'filename': b'raven/base.py', 
                                b'function': b'build_msg', 
                                b'in_app': False, 
                                b'lineno': 290, 
                                b'module': b'raven.base', 
                                b'post_context': [
                                                b'                },',
                                                b'            })',
                                                b'',
                                                b"        if 'stacktrace' in data:",
                                                b'            if self.include_paths:'], 
                                b'pre_context': [
                                               b'',
                                               b'            data.update({',
                                               b"                'stacktrace': {",
                                               b"                    'frames': get_stack_info(frames,",
                                               b'                        list_max_length=self.list_max_length,'], 
                                b'vars': {b'culprit': b'raven.scripts.runner', 
                                          b'date': b'datetime.datetime(2013, 2, 14, 20, 6, 33, 479471)', 
                                          b'event_id': b'598fb19363e745ec8be665e6ba88b1b2', 
                                          b'event_type': b'raven.events.Message', 
                                          b'frames': b'<generator object iter_stack_frames at 0x103fef050>', 
                                          b'handler': b'<raven.events.Message object at 0x103feb710>', 
                                          b'k': b'logentry', 
                                          b'public_key': None, 
                                          b'result': {b'logentry': b"{'message': 'This is a test message generated using ``raven test``', 'params': []}"}, 
                                          b'self': b'<raven.base.Client object at 0x104397f10>', 
                                          b'stack': True, 
                                          b'tags': None, 
                                          b'time_spent': None}}]}, 
   b'tags': [], b'platform': b'python'}

def _patch_artifact_manifest(path, org, release, project=None):
    manifest = json.loads(open(path, b'rb').read())
    manifest[b'org'] = org
    manifest[b'release'] = release
    if project:
        manifest[b'project'] = project
    return json.dumps(manifest)


class Factories(object):

    @staticmethod
    def create_organization(name=None, owner=None, **kwargs):
        if not name:
            name = petname.Generate(2, b' ', letters=10).title()
        org = Organization.objects.create(name=name, **kwargs)
        if owner:
            Factories.create_member(organization=org, user=owner, role=b'owner')
        return org

    @staticmethod
    def create_member(teams=None, **kwargs):
        kwargs.setdefault(b'role', b'member')
        om = OrganizationMember.objects.create(**kwargs)
        if teams:
            for team in teams:
                Factories.create_team_membership(team=team, member=om)

        return om

    @staticmethod
    def create_team_membership(team, member=None, user=None):
        if member is None:
            member, _ = OrganizationMember.objects.get_or_create(user=user, organization=team.organization, defaults={b'role': b'member'})
        return OrganizationMemberTeam.objects.create(team=team, organizationmember=member, is_active=True)

    @staticmethod
    def create_team(organization, **kwargs):
        if not kwargs.get(b'name'):
            kwargs[b'name'] = petname.Generate(2, b' ', letters=10).title()
        if not kwargs.get(b'slug'):
            kwargs[b'slug'] = slugify(six.text_type(kwargs[b'name']))
        members = kwargs.pop(b'members', None)
        team = Team.objects.create(organization=organization, **kwargs)
        if members:
            for user in members:
                Factories.create_team_membership(team=team, user=user)

        return team

    @staticmethod
    def create_environment(project, **kwargs):
        name = kwargs.get(b'name', petname.Generate(3, b' ', letters=10)[:64])
        env = Environment.objects.create(organization_id=project.organization_id, project_id=project.id, name=name)
        env.add_project(project, is_hidden=kwargs.get(b'is_hidden'))
        return env

    @staticmethod
    def create_project(organization=None, teams=None, **kwargs):
        if not kwargs.get(b'name'):
            kwargs[b'name'] = petname.Generate(2, b' ', letters=10).title()
        if not kwargs.get(b'slug'):
            kwargs[b'slug'] = slugify(six.text_type(kwargs[b'name']))
        if not organization and teams:
            organization = teams[0].organization
        project = Project.objects.create(organization=organization, **kwargs)
        if teams:
            for team in teams:
                project.add_team(team)

        return project

    @staticmethod
    def create_project_bookmark(project, user):
        return ProjectBookmark.objects.create(project_id=project.id, user=user)

    @staticmethod
    def create_project_key(project):
        return project.key_set.get_or_create()[0]

    @staticmethod
    def create_release(project, user=None, version=None, date_added=None):
        if version is None:
            version = os.urandom(20).encode(b'hex')
        if date_added is None:
            date_added = timezone.now()
        release = Release.objects.create(version=version, organization_id=project.organization_id, date_added=date_added)
        release.add_project(project)
        Activity.objects.create(type=Activity.RELEASE, project=project, ident=Activity.get_version_ident(version), user=user, data={b'version': version})
        if user:
            author = Factories.create_commit_author(project=project, user=user)
            repo = Factories.create_repo(project, name=(b'organization-{}').format(project.slug))
            commit = Factories.create_commit(project=project, repo=repo, author=author, release=release, key=b'deadbeef', message=b'placeholder commit message')
            release.update(authors=[
             six.text_type(author.id)], commit_count=1, last_commit_id=commit.id)
        return release

    @staticmethod
    def create_artifact_bundle(org, release, project=None):
        import zipfile
        bundle = io.BytesIO()
        bundle_dir = get_fixture_path(b'artifact_bundle')
        with zipfile.ZipFile(bundle, b'w', zipfile.ZIP_DEFLATED) as (zipfile):
            for path, _, files in os.walk(bundle_dir):
                for filename in files:
                    fullpath = os.path.join(path, filename)
                    relpath = os.path.relpath(fullpath, bundle_dir)
                    if filename == b'manifest.json':
                        manifest = _patch_artifact_manifest(fullpath, org, release, project)
                        zipfile.writestr(relpath, manifest)
                    else:
                        zipfile.write(fullpath, relpath)

        return bundle.getvalue()

    @staticmethod
    def create_repo(project, name=None):
        repo = Repository.objects.create(organization_id=project.organization_id, name=name or (b'{}-{}').format(petname.Generate(2, b'', letters=10), random.randint(1000, 9999)))
        return repo

    @staticmethod
    def create_commit(repo, project=None, author=None, release=None, message=None, key=None, date_added=None):
        commit = Commit.objects.get_or_create(organization_id=repo.organization_id, repository_id=repo.id, key=key or sha1(uuid4().hex).hexdigest(), defaults={b'message': message or make_sentence(), 
           b'author': author or Factories.create_commit_author(organization_id=repo.organization_id), 
           b'date_added': date_added or timezone.now()})[0]
        if release:
            assert project
            ReleaseCommit.objects.create(organization_id=repo.organization_id, project_id=project.id, release=release, commit=commit, order=1)
        Factories.create_commit_file_change(commit=commit, filename=b'/models/foo.py')
        Factories.create_commit_file_change(commit=commit, filename=b'/worsematch/foo.py')
        Factories.create_commit_file_change(commit=commit, filename=b'/models/other.py')
        return commit

    @staticmethod
    def create_commit_author(organization_id=None, project=None, user=None):
        return CommitAuthor.objects.get_or_create(organization_id=organization_id or project.organization_id, email=user.email if user else (b'{}@example.com').format(make_word()), defaults={b'name': user.name if user else make_word()})[0]

    @staticmethod
    def create_commit_file_change(commit, filename):
        return CommitFileChange.objects.get_or_create(organization_id=commit.organization_id, commit=commit, filename=filename, type=b'M')

    @staticmethod
    def create_user(email=None, **kwargs):
        if email is None:
            email = uuid4().hex + b'@example.com'
        kwargs.setdefault(b'username', email)
        kwargs.setdefault(b'is_staff', True)
        kwargs.setdefault(b'is_active', True)
        kwargs.setdefault(b'is_superuser', False)
        user = User(email=email, **kwargs)
        if not kwargs.get(b'password'):
            user.set_password(b'admin')
        user.save()
        assert UserEmail.objects.filter(user=user, email=email).update(is_verified=True)
        return user

    @staticmethod
    def create_useremail(user, email, **kwargs):
        if not email:
            email = uuid4().hex + b'@example.com'
        kwargs.setdefault(b'is_verified', True)
        useremail = UserEmail(user=user, email=email, **kwargs)
        useremail.save()
        return useremail

    @staticmethod
    def create_event(group=None, project=None, event_id=None, normalize=True, **kwargs):
        if event_id is None:
            event_id = uuid4().hex
        kwargs.setdefault(b'project', project if project else group.project)
        kwargs.setdefault(b'data', copy.deepcopy(DEFAULT_EVENT_DATA))
        kwargs.setdefault(b'platform', kwargs[b'data'].get(b'platform', b'python'))
        kwargs.setdefault(b'message', kwargs[b'data'].get(b'message', b'message'))
        if kwargs.get(b'tags'):
            tags = kwargs.pop(b'tags')
            if isinstance(tags, dict):
                tags = list(tags.items())
            kwargs[b'data'][b'tags'] = tags
        if kwargs.get(b'stacktrace'):
            stacktrace = kwargs.pop(b'stacktrace')
            kwargs[b'data'][b'stacktrace'] = stacktrace
        user = kwargs.pop(b'user', None)
        if user is not None:
            kwargs[b'data'][b'user'] = user
        kwargs[b'data'].setdefault(b'errors', [{b'type': EventError.INVALID_DATA, b'name': b'foobar'}])
        if b'logentry' not in kwargs[b'data']:
            kwargs[b'data'][b'logentry'] = {b'message': kwargs[b'message'] or b'<unlabeled event>'}
        if normalize:
            manager = EventManager(CanonicalKeyDict(kwargs[b'data']))
            manager.normalize()
            kwargs[b'data'] = manager.get_data()
            kwargs[b'data'].update(manager.materialize_metadata())
            kwargs[b'message'] = manager.get_search_message()
        kwargs[b'data'].setdefault(b'node_id', Event.generate_node_id(kwargs[b'project'].id, event_id))
        event = Event(event_id=event_id, group=group, **kwargs)
        event.data.bind_ref(event)
        event.save()
        return event

    @staticmethod
    def store_event(data, project_id, assert_no_errors=True):
        manager = EventManager(data)
        manager.normalize()
        if assert_no_errors:
            errors = manager.get_data().get(b'errors')
            assert not errors, errors
        event = manager.save(project_id)
        if event.group:
            event.group.save()
        return event

    @staticmethod
    def create_full_event(group, event_id=b'a', **kwargs):
        payload = b'\n            {\n                "event_id": "f5dd88e612bc406ba89dfebd09120769",\n                "project": 11276,\n                "release": "e1b5d1900526feaf20fe2bc9cad83d392136030a",\n                "platform": "javascript",\n                "culprit": "app/components/events/eventEntries in map",\n                "logentry": {"formatted": "TypeError: Cannot read property \'1\' of null"},\n                "tags": [\n                    ["environment", "prod"],\n                    ["sentry_version", "e1b5d1900526feaf20fe2bc9cad83d392136030a"],\n                    ["level", "error"],\n                    ["logger", "javascript"],\n                    ["sentry:release", "e1b5d1900526feaf20fe2bc9cad83d392136030a"],\n                    ["browser", "Chrome 48.0"],\n                    ["device", "Other"],\n                    ["os", "Windows 10"],\n                    ["url", "https://sentry.io/katon-direct/localhost/issues/112734598/"],\n                    ["sentry:user", "id:41656"]\n                ],\n                "errors": [{\n                    "url": "<anonymous>",\n                    "type": "js_no_source"\n                }],\n                "extra": {\n                    "session:duration": 40364\n                },\n                "exception": {\n                    "exc_omitted": null,\n                    "values": [{\n                        "stacktrace": {\n                            "frames": [{\n                                "function": "batchedUpdates",\n                                "abs_path": "webpack:////usr/src/getsentry/src/sentry/~/react/lib/ReactUpdates.js",\n                                "pre_context": ["  // verify that that\'s the case. (This is called by each top-level update", "  // function, like setProps, setState, forceUpdate, etc.; creation and", "  // destruction of top-level components is guarded in ReactMount.)", "", "  if (!batchingStrategy.isBatchingUpdates) {"],\n                                "post_context": ["    return;", "  }", "", "  dirtyComponents.push(component);", "}"],\n                                "filename": "~/react/lib/ReactUpdates.js",\n                                "module": "react/lib/ReactUpdates",\n                                "colno": 0,\n                                "in_app": false,\n                                "data": {\n                                    "orig_filename": "/_static/29e365f8b0d923bc123e8afa38d890c3/sentry/dist/vendor.js",\n                                    "orig_abs_path": "https://media.sentry.io/_static/29e365f8b0d923bc123e8afa38d890c3/sentry/dist/vendor.js",\n                                    "sourcemap": "https://media.sentry.io/_static/29e365f8b0d923bc123e8afa38d890c3/sentry/dist/vendor.js.map",\n                                    "orig_lineno": 37,\n                                    "orig_function": "Object.s [as enqueueUpdate]",\n                                    "orig_colno": 16101\n                                },\n                                "context_line": "    batchingStrategy.batchedUpdates(enqueueUpdate, component);",\n                                "lineno": 176\n                            }],\n                            "frames_omitted": null\n                        },\n                        "type": "TypeError",\n                        "value": "Cannot read property \'1\' of null",\n                        "module": null\n                    }]\n                },\n                "request": {\n                    "url": "https://sentry.io/katon-direct/localhost/issues/112734598/",\n                    "headers": [\n                        ["Referer", "https://sentry.io/welcome/"],\n                        ["User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36"]\n                    ]\n                },\n                "user": {\n                    "ip_address": "0.0.0.0",\n                    "id": "41656",\n                    "email": "test@example.com"\n                },\n                "version": "7",\n                "breadcrumbs": {\n                    "values": [\n                        {\n                            "category": "xhr",\n                            "timestamp": 1496395011.63,\n                            "type": "http",\n                            "data": {\n                                "url": "/api/path/here",\n                                "status_code": "500",\n                                "method": "POST"\n                            }\n                        }\n                    ]\n                }\n            }'
        event = Factories.create_event(group=group, event_id=event_id, platform=b'javascript', data=json.loads(payload), normalize=False)
        return event

    @staticmethod
    def create_group(project, checksum=None, **kwargs):
        if checksum:
            warnings.warn(b'Checksum passed to create_group', DeprecationWarning)
        kwargs.setdefault(b'message', b'Hello world')
        kwargs.setdefault(b'data', {})
        if b'type' not in kwargs[b'data']:
            kwargs[b'data'].update({b'type': b'default', b'metadata': {b'title': kwargs[b'message']}})
        if b'short_id' not in kwargs:
            kwargs[b'short_id'] = project.next_short_id()
        return Group.objects.create(project=project, **kwargs)

    @staticmethod
    def create_file(**kwargs):
        return File.objects.create(**kwargs)

    @staticmethod
    def create_file_from_path(path, name=None, **kwargs):
        if name is None:
            name = os.path.basename(path)
        file = Factories.create_file(name=name, **kwargs)
        with open(path) as (f):
            file.putfile(f)
        return file

    @staticmethod
    def create_event_attachment(event, file=None, **kwargs):
        if file is None:
            file = Factories.create_file(name=b'log.txt', size=32, headers={b'Content-Type': b'text/plain'}, checksum=b'dc1e3f3e411979d336c3057cce64294f3420f93a')
        return EventAttachment.objects.create(project_id=event.project_id, event_id=event.event_id, file=file, **kwargs)

    @staticmethod
    def create_dif_file(project, debug_id=None, object_name=None, features=None, data=None, file=None, cpu_name=None, code_id=None, **kwargs):
        if debug_id is None:
            debug_id = six.text_type(uuid4())
        if object_name is None:
            object_name = b'%s.dSYM' % debug_id
        if features is not None:
            if data is None:
                data = {}
            data[b'features'] = features
        if file is None:
            file = Factories.create_file(name=object_name, size=42, headers={b'Content-Type': b'application/x-mach-binary'}, checksum=b'dc1e3f3e411979d336c3057cce64294f3420f93a')
        return ProjectDebugFile.objects.create(debug_id=debug_id, code_id=code_id, project=project, object_name=object_name, cpu_name=(cpu_name or b'x86_64'), file=file, data=data, **kwargs)

    @staticmethod
    def create_dif_from_path(path, object_name=None, **kwargs):
        if object_name is None:
            object_name = os.path.basename(path)
        headers = {b'Content-Type': b'application/x-mach-binary'}
        file = Factories.create_file_from_path(path, name=object_name, headers=headers)
        return Factories.create_dif_file(file=file, object_name=object_name, **kwargs)

    @staticmethod
    def add_user_permission(user, permission):
        UserPermission.objects.create(user=user, permission=permission)

    @staticmethod
    def create_sentry_app(**kwargs):
        app = sentry_apps.Creator.run(**Factories._sentry_app_kwargs(**kwargs))
        if kwargs.get(b'published'):
            app.update(status=SentryAppStatus.PUBLISHED)
        return app

    @staticmethod
    def create_internal_integration(**kwargs):
        return sentry_apps.InternalCreator.run(**Factories._sentry_app_kwargs(**kwargs))

    @staticmethod
    def create_internal_integration_token(install, **kwargs):
        return sentry_app_installation_tokens.Creator.run(sentry_app_installation=install, **kwargs)

    @staticmethod
    def _sentry_app_kwargs(**kwargs):
        _kwargs = {b'user': kwargs.get(b'user', Factories.create_user()), 
           b'name': kwargs.get(b'name', petname.Generate(2, b' ', letters=10).title()), 
           b'organization': kwargs.get(b'organization', Factories.create_organization()), 
           b'author': kwargs.get(b'author', b'A Company'), 
           b'scopes': kwargs.get(b'scopes', ()), 
           b'verify_install': kwargs.get(b'verify_install', True), 
           b'webhook_url': kwargs.get(b'webhook_url', b'https://example.com/webhook'), 
           b'events': [], b'schema': {}}
        _kwargs.update(**kwargs)
        return _kwargs

    @staticmethod
    def create_sentry_app_installation(organization=None, slug=None, user=None):
        if not organization:
            organization = Factories.create_organization()
        Factories.create_project(organization=organization)
        return sentry_app_installations.Creator.run(slug=slug or Factories.create_sentry_app().slug, organization=organization, user=user or Factories.create_user())

    @staticmethod
    def create_issue_link_schema():
        return {b'type': b'issue-link', 
           b'link': {b'uri': b'/sentry/issues/link', 
                     b'required_fields': [
                                        {b'type': b'select', 
                                           b'name': b'assignee', 
                                           b'label': b'Assignee', 
                                           b'uri': b'/sentry/members'}]}, 
           b'create': {b'uri': b'/sentry/issues/create', 
                       b'required_fields': [{b'type': b'text', b'name': b'title', b'label': b'Title'}, {b'type': b'text', b'name': b'summary', b'label': b'Summary'}], b'optional_fields': [
                                          {b'type': b'select', 
                                             b'name': b'points', 
                                             b'label': b'Points', 
                                             b'options': [
                                                        [
                                                         b'1', b'1'], [b'2', b'2'], [b'3', b'3'], [b'5', b'5'], [b'8', b'8']]},
                                          {b'type': b'select', 
                                             b'name': b'assignee', 
                                             b'label': b'Assignee', 
                                             b'uri': b'/sentry/members'}]}}

    @staticmethod
    def create_alert_rule_action_schema():
        return {b'type': b'alert-rule-action', 
           b'required_fields': [{b'type': b'text', b'name': b'channel', b'label': b'Channel'}]}

    @staticmethod
    def create_service_hook(actor=None, org=None, project=None, events=None, url=None, **kwargs):
        if not actor:
            actor = Factories.create_user()
        if not org:
            org = Factories.create_organization(owner=actor)
        if not project:
            project = Factories.create_project(organization=org)
        if events is None:
            events = ('event.created', )
        if not url:
            url = b'https://example.com/sentry/webhook'
        _kwargs = {b'actor': actor, 
           b'projects': [
                       project], 
           b'organization': org, 
           b'events': events, 
           b'url': url}
        _kwargs.update(kwargs)
        return service_hooks.Creator.run(**_kwargs)

    @staticmethod
    def create_sentry_app_feature(feature=None, sentry_app=None, description=None):
        if not sentry_app:
            sentry_app = Factories.create_sentry_app()
        integration_feature = IntegrationFeature.objects.create(sentry_app=sentry_app, feature=feature or Feature.API)
        if description:
            integration_feature.update(user_description=description)
        return integration_feature

    @staticmethod
    def create_userreport(group, project=None, event_id=None, **kwargs):
        return UserReport.objects.create(group=group, event_id=(event_id or b'a' * 32), project=(project or group.project), name=b'Jane Doe', email=b'jane@example.com', comments=b'the application crashed', **kwargs)

    @staticmethod
    def create_session():
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore()
        session.save()
        return session

    @staticmethod
    def create_platform_external_issue(group=None, service_type=None, display_name=None, web_url=None):
        return PlatformExternalIssue.objects.create(group_id=group.id, service_type=service_type, display_name=display_name, web_url=web_url)

    @staticmethod
    def create_incident(organization, projects, detection_uuid=None, status=1, title=None, query=b'test query', date_started=None, date_detected=None, date_closed=None, groups=None, seen_by=None):
        if not title:
            title = petname.Generate(2, b' ', letters=10).title()
        incident = Incident.objects.create(organization=organization, detection_uuid=detection_uuid, status=status, title=title, query=query, date_started=date_started or timezone.now(), date_detected=date_detected or timezone.now(), date_closed=date_closed or timezone.now())
        for project in projects:
            IncidentProject.objects.create(incident=incident, project=project)

        if groups:
            for group in groups:
                IncidentGroup.objects.create(incident=incident, group=group)

        if seen_by:
            for user in seen_by:
                IncidentSeen.objects.create(incident=incident, user=user, last_seen=timezone.now())

        return incident

    @staticmethod
    def create_incident_activity(incident, type, comment=None, user=None):
        return IncidentActivity.objects.create(incident=incident, type=type, comment=comment, user=user)