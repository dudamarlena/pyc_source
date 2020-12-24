# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/limnoria_github/config.py
# Compiled at: 2020-05-08 12:52:23
# Size of source mod 2**32: 8437 bytes
import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    from supybot.i18n import internationalizeDocstring
    _ = PluginInternationalization('GitHub')
except:
    _ = lambda x: x
    internationalizeDocstring = lambda x: x

def configure(advanced):
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('GitHub', True)


GitHub = conf.registerPlugin('GitHub')
conf.registerGroup(GitHub, 'api')
conf.registerGlobalValue(GitHub.api, 'url', registry.String('https://api.github.com', _("The URL of the\n        GitHub API to use. You probably don't need to edit it, but I let it\n        there, just in case.")))
conf.registerGlobalValue(GitHub, 'announces', registry.String('', _("You shouldn't edit this configuration\n        variable yourself, unless you know what you do. Use '@Github announce\n        add' or '@Github announce remove' instead.")))
conf.registerGlobalValue(GitHub.announces, 'secret', registry.SpaceSeparatedSetOfStrings((set()), (_('Set of space-separated\n        secret payloads used to authenticate GitHub.')),
  private=True))
conf.registerChannelValue(GitHub, 'max_announce_commits', registry.Integer(3, _('Determines the maximum number of commits that\n        will be announced for a single push. Note that if the number of commits\n        is only one over the limit, it will be announced anyway instead of\n        saying "1 more commit".')))
conf.registerGroup(GitHub, 'format')
conf.registerGroup(GitHub.format, 'before')
conf.registerChannelValue(GitHub.format.before, 'push', registry.String('', _('Format for an optional summary line before the individual commits\n        in the push event.')))
conf.registerChannelValue(GitHub.format, 'push', registry.String('echo ' + _('$repository__owner__name/\x02$repository__name\x02 (in \x02$ref__branch\x02): $__commit__author__name committed \x02$__commit__message__firstline\x02 $__commit__url__tiny').replace('\n        ', ' '), _('Format for push events.')))
conf.registerChannelValue(GitHub.format.push, 'hidden', registry.String('echo (+$__hidden_commits hidden commits)', _('Format for the hidden commits message for push events.')))
conf.registerChannelValue(GitHub.format, 'commit_comment', registry.String('echo ' + _('$repository__owner__login/\x02$repository__name\x02: $comment__user__login commented on commit \x02$comment__commit_id__short\x02 $comment__html_url__tiny').replace('\n        ', ' '), _('Format for commit comment events.')))
conf.registerChannelValue(GitHub.format, 'issues', registry.String('echo ' + _('$repository__owner__login/\x02$repository__name\x02: \x02$sender__login\x02 $action issue #$issue__number: \x02$issue__title\x02 $issue__html_url').replace('\n        ', ' '), _('Format for issue events.')))
conf.registerChannelValue(GitHub.format, 'issue_comment', registry.String('echo ' + _('$repository__owner__login/\x02$repository__name\x02: \x02$sender__login\x02 $action comment on issue #$issue__number: \x02$issue__title\x02 $issue__html_url__tiny').replace('\n        ', ' '), _('Format for issue comment events.')))
conf.registerChannelValue(GitHub.format, 'status', registry.String('echo ' + _('$repository__owner__login/\x02$repository__name\x02: Status for commit "\x02$commit__commit__message__firstline\x02" by \x02$commit__commit__committer__name\x02: \x02$description\x02 $target_url__tiny').replace('\n        ', ' '), _('Format for status events.')))
conf.registerChannelValue(GitHub.format, 'pull_request', registry.String('echo ' + _('$repository__owner__login/\x02$repository__name\x02: \x02$sender__login\x02 $action pull request #$number (to \x02$pull_request__base__ref\x02): \x02$pull_request__title\x02 $pull_request__html_url__tiny').replace('\n        ', ' '), _('Format for pull request events.')))
conf.registerChannelValue(GitHub.format, 'pull_request_review', registry.String('echo ' + _('$repository__owner__login/\x02$repository__name\x02: \x02$user__login\x02 reviewed pull request #$pull_request__number (to \x02$pull_request__base__ref\x02): \x02$pull_request__title\x02 $pull_request__html_url__tiny').replace('\n        ', ' '), _('Format for pull request review events. This is triggered when\n        a pull request review is finished. If you want to be notified about\n        individual comments during a review, use the\n        pull_request_review_comment event.')))
conf.registerChannelValue(GitHub.format, 'pull_request_review_comment', registry.String('', _('Format for pull request review comment events. This is for\n        individual review comments, you probably only want to use the\n        pull_request_review event to avoid clutter.')))
EVENT_TYPES = ('check_suite', 'content_reference', 'create', 'delete', 'deploy_key',
               'deployment', 'deployment_status', 'download', 'follow', 'fork', 'fork_apply',
               'github_app_authorization', 'gist', 'gollum', 'installation', 'installation_repositories',
               'label', 'member', 'membership', 'meta', 'milestone', 'organization',
               'org_block', 'page_build', 'project_card', 'project_column', 'project',
               'public', 'registry_package', 'release', 'repository_dispatch', 'repository',
               'repository_import', 'repository_vulnerability_alert', 'security_advisory',
               'star', 'team', 'team_add', 'watch')
for event_type in EVENT_TYPES:
    conf.registerChannelValue(GitHub.format, event_type, registry.String('', _('Format for %s events.') % event_type))