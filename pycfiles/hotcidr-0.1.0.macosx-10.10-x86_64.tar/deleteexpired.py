# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/skemper/workspace/hotcidr/venv/lib/python2.7/site-packages/hotcidr/deleteexpired.py
# Compiled at: 2014-09-11 23:30:12
from __future__ import print_function
import os, sys, time, git, hotcidr.state
from hotcidr import util
from util import isint
import yaml

def main(repo=None, dont_push=None, silence=None):
    repo, is_git_repo = util.get_valid_repo(repo)
    groups = util.get_groups_dict(repo)
    try:
        expirationsyaml = file(os.path.join(repo, 'expirations.yaml'), 'r')
        expirations = hotcidr.state.load(expirationsyaml)
    except IOError:
        print('Error: ' + os.path.join(repo, 'expirations.yaml') + ' is missing, and is necessary for expiration checking.', file=sys.stderr)
        return 1
    except yaml.scanner.ScannerError as e:
        print('Error: expirations.yaml is not properly formatted:\n' + str(e), file=sys.stderr)
        print('expirations.yaml is necessary for expiration checking.', file=sys.stderr)
        return 1

    if expirations:
        if 'rules' in expirations:
            expirations = expirations['rules']
        else:
            print("Error: expirations.yaml is not properly formatted. Rules must be under a 'rules:' tag.", file=sys.stderr)
    groups_num = len(groups)
    if groups_num == 0:
        print('ERROR: No groups loaded.', file=sys.stderr)
        return 1
    if not silence:
        i = 0
    any_rules_removed = False
    for group in groups:
        if not silence:
            print('Processing ' + groups[group], file=sys.stderr)
            sys.stderr.flush()
        try:
            rulesyaml = file(os.path.join(repo, groups[group]), 'r')
            rules = hotcidr.state.load(rulesyaml)
        except IOError:
            print('Warning: ' + os.path.join(repo, groups[group]) + ' is missing. It will be skipped.', file=sys.stderr)
            continue
        except yaml.scanner.ScannerError as e:
            print('Warning: ' + os.path.join(repo, groups[group]) + ' is not properly formatted and will be skipped:\n' + str(e), file=sys.stderr)
            continue

        added_rules = util.get_added_deleted_rules(repo, groups[group])['added']
        rules_removed = False
        for added_rule in added_rules:
            if expirations:
                for expired_rule in expirations:
                    if 'expiration' in expired_rule and isint(expired_rule['expiration']):
                        if len(expired_rule.keys()) >= 2:
                            rule_is_expired = True
                            for field in util.expected_rule_fields:
                                if field not in added_rule or field not in expired_rule:
                                    continue
                                if not added_rule[field] == expired_rule[field]:
                                    rule_is_expired = False
                                    break

                            if rule_is_expired:
                                added_rule['expiration'] = int(expired_rule['expiration'])
                        else:
                            print('Warning: rule in expirations.yaml has no fields to match: ' + expired_rule)
                    else:
                        print('Warning: rule in expirations.yaml is missing a valid expiration field: ' + expired_rule)

            if 'expiration' in added_rule and isint(added_rule['expiration']):
                if int(added_rule['expiration']) < int(time.time()) - int(added_rule['date']):
                    if not silence:
                        print('Removed rule: ' + str(added_rule))
                    added_rules.remove(added_rule)
                    rules_removed = True

        for added_rule in added_rules:
            del added_rule['hexsha']
            del added_rule['author']
            del added_rule['date']

        if rules_removed:
            any_rules_removed = True
            rules['rules'] = added_rules
            f = open(os.path.join(repo, groups[group]), 'w')
            f.write(hotcidr.state.dump(rules, default_flow_style=False))
            f.close()
        if not silence:
            i += 1
            print('Progress: ' + str(int(100 * i / groups_num)), file=sys.stderr)

    if any_rules_removed:
        git.Git(repo).add(groups[group])
        git.Git(repo).commit('-m', 'Automatically removed expired rule')
        if not dont_push:
            try:
                git.Git(repo).push()
            except git.exc.GitCommandError:
                print('Error: ' + repo + ' cannot be pushed: no remote exists? Try specifying the --dont-push argument.')
                return 1

    if is_git_repo:
        rmtree(repo)
    return 0