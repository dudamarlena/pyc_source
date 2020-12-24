# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_member_unreleased_commits.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from django.db import connections
from itertools import izip
from sentry.api.bases import OrganizationMemberEndpoint
from sentry.api.serializers import serialize
from sentry.models import Commit, Repository, UserEmail
query = '\nselect c1.*\nfrom sentry_commit c1\njoin (\n    select max(c2.date_added) as date_added, c2.repository_id\n    from sentry_commit as c2\n    join (\n        select distinct commit_id from sentry_releasecommit\n        where organization_id = %%s\n    ) as rc2\n    on c2.id = rc2.commit_id\n    group by c2.repository_id\n) as cmax\non c1.repository_id = cmax.repository_id\nwhere c1.date_added > cmax.date_added\nand c1.author_id IN (\n    select id\n    from sentry_commitauthor\n    where organization_id = %%s\n    and upper(email) IN (%s)\n)\norder by c1.date_added desc\n'
quote_name = connections['default'].ops.quote_name

class OrganizationMemberUnreleasedCommitsEndpoint(OrganizationMemberEndpoint):

    def get(self, request, organization, member):
        email_list = list(UserEmail.objects.filter(user=member.user_id, is_verified=True).values_list('email', flat=True))
        if not email_list:
            return self.respond({'commits': [], 'repositories': {}, 'errors': {'missing_emails': True}})
        params = [
         organization.id, organization.id]
        for e in email_list:
            params.append(e.upper())

        queryset = Commit.objects.raw(query % ((', ').join('%s' for _ in email_list),), params)
        results = list(queryset)
        if results:
            repos = list(Repository.objects.filter(id__in=set([ r.repository_id for r in results ])))
        else:
            repos = []
        return self.respond({'commits': [ {'id': c.key, 'message': c.message, 'dateCreated': c.date_added, 'repositoryID': six.text_type(c.repository_id)} for c in results
                    ], 
           'repositories': {six.text_type(r.id):d for r, d in izip(repos, serialize(repos, request.user))}})