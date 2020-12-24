# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/skemper/workspace/hotcidr/venv/lib/python2.7/site-packages/hotcidr/util.py
# Compiled at: 2014-09-11 23:30:12
from __future__ import print_function
from shutil import rmtree
from hotcidr import state
import boto.ec2, boto.vpc, contextlib, git, hashlib, json, os, requests, shutil, sys, tempfile, time, yaml

def isint(n):
    try:
        int(n)
        return True
    except:
        return False


def is_cidr(s):
    if hasattr(s, 'split'):
        n = s.split('.', 4)
        if isint(n[0]) and isint(n[1]) and isint(n[2]):
            n3 = n[3].split('/', 1)
            if isint(n3[0]) and (len(n3) == 1 or isint(n3[1])):
                return True
    return False


def is_valid_vpc(vpc):
    valid_regions = set([
     'ap-northeast-1',
     'ap-southeast-1',
     'ap-southeast-2',
     'eu-west-1',
     'sa-east-1',
     'us-east-1',
     'us-west-1',
     'us-west-2'])
    return vpc in valid_regions


expected_rule_fields = [
 'direction', 'protocol', 'location']

def load_boxes(d):
    return state.load(open(os.path.join(d, 'boxes.yaml')))


def load_groups(d, ext='.yaml'):
    groups_dir = os.path.join(d, 'groups')
    assert os.path.isdir(groups_dir)
    r = {}
    for group in os.listdir(groups_dir):
        if group.endswith(ext):
            f = os.path.join(groups_dir, group)
            group_name = group[:-len(ext)]
            r[group_name] = state.load(open(f))

    return r


def get_hash_from_rule(rule_orig):
    rule = rule_orig.copy()
    for field in expected_rule_fields:
        if field not in rule:
            rule[field] = ''

    if 'justification' not in rule:
        justification = ''
    else:
        justification = rule['justification']
    if 'expiration' not in rule:
        expiration = ''
    else:
        expiration = rule['expiration']
    if 'ports' in rule:
        identifier = str(rule['direction']) + str(rule['protocol']) + str(rule['location']) + str(rule['ports']) + str(justification) + str(expiration)
    else:
        identifier = str(rule['direction']) + str(rule['protocol']) + str(rule['location']) + str(justification) + str(expiration)
    hash = hashlib.md5()
    hash.update(identifier)
    return str(hash.digest())


def get_groups_dict(repo_path):
    groups_dict = {}
    for dirname, dirnames, filenames in os.walk(os.path.join(repo_path, 'groups')):
        for filename in filenames:
            if filename.endswith('.yaml'):
                groups_dict[filename.rsplit('.', 1)[0]] = 'groups/' + filename

    return groups_dict


def create_remote_repo(git_api_url, vpc, repo_name, auth):
    if not is_valid_vpc(vpc):
        print('ERROR: Remote repo could not be created: ' + vpc + ' is not a valid vpc-region-code.')
        return
    else:
        auth_header = {'Authorization': 'token ' + auth}
        try:
            repo_user = json.loads(requests.get(git_api_url + 'user', headers=auth_header).content)['login']
        except ValueError:
            print('ERROR: ' + git_api_url + ' did not respond. URL is invalid or inaccessible.')
            return

        repos = {}
        repos_response_url = json.loads(requests.get(git_api_url + 'user', headers=auth_header).content)['repos_url']
        repos_response = json.loads(requests.get(repos_response_url, headers=auth_header).content)
        for r in repos_response:
            repos[r['name'].encode('utf-8')] = r['ssh_url'].encode('utf-8')

        if repo_name in repos.keys():
            desired_repo_url = repos[repo_name]
            var = raw_input('Warning: ' + desired_repo_url + ' already exists. Delete it? (y/n) ')
        else:
            var = 'n'
        if var == 'y':
            r = requests.delete(git_api_url + 'repos/' + repo_user + '/' + repo_name, headers=auth_header)
            print('Deleted ' + desired_repo_url)
            print('Waiting 5 seconds for delete request to be processed')
            time.sleep(5)
        r = requests.post(git_api_url + 'user/repos', json.dumps({'name': repo_name}), headers=auth_header)
        repos = {}
        repos_response_url = json.loads(requests.get(git_api_url + 'user', headers=auth_header).content)['repos_url']
        repos_response = json.loads(requests.get(repos_response_url, headers=auth_header).content)
        for r in repos_response:
            repos[r['name'].encode('utf-8')] = r['ssh_url'].encode('utf-8')

        if repo_name in repos.keys():
            desired_repo_url = repos[repo_name]
        else:
            desired_repo_url = ''
        print('Added ' + desired_repo_url)
        return desired_repo_url


def get_valid_repo(repo):
    if repo == None:
        print('ERROR: git repo is specified as "None". Please enter in a valid repo or clone url.', file=sys.stderr)
        return (None, None)
    else:
        if not os.path.isdir(repo):
            is_git_repo = True
            if not repo.endswith('.git'):
                print('Error: ' + repo + ' is not a directory nor a valid git clone URL.', file=sys.stderr)
                return (None, None)
            try:
                git.Git().ls_remote(repo)
            except:
                print('Error: ' + repo + ' is not a valid git clone URL.', file=sys.stderr)

            gitrepo_location = tempfile.mkdtemp()
            new_repo_path = os.path.join(gitrepo_location, repo.rsplit('/', 1)[1].rsplit('.', 1)[0])
            new_full_path = os.path.join(gitrepo_location, new_repo_path)
            if os.path.exists(new_full_path):
                rmtree(new_full_path)
            git.Repo.clone_from(repo, new_full_path)
            repo = new_repo_path
        else:
            is_git_repo = False
            try:
                git.Git(repo).status()
            except:
                print('ERROR: ' + repo + " is not a valid git repo. Try 'git init' in that directory before continuing.", file=sys.stderr)
                return (None, None)

            try:
                git.Git(repo).log()
            except:
                print('ERROR: ' + repo + ' has no commits. Commit before continuing.', file=sys.stderr)
                return (None, None)

            try:
                git.Git(repo).pull()
            except:
                pass

        return (
         repo, is_git_repo)


def get_init_commit(git_dir, yamlfile):
    init_commit = git.Git(git_dir).log('--format="%an;%at;%H"', yamlfile).split('\n')[(-1)][1:-1].rsplit(';', 2)
    init_commit[2] = init_commit[2].rsplit('\n', 1)[0]
    return init_commit


def get_git_commit(hexsha, git_dir, yamlfile):
    init_commit = get_init_commit(git_dir, yamlfile)
    if init_commit[2] == hexsha:
        commit_message = git.Git(git_dir).log(hexsha, '--format="%B"').replace('\n', ' ')[1:-1].rstrip()
        return commit_message
    else:
        commit_message = git.Git(git_dir).log('--ancestry-path', hexsha + '^..' + hexsha, '--format="%B"').replace('\n', ' ')[1:-1].rstrip()
        return commit_message


def get_commit_approved_authdate(commit_hexsha, git_dir, yamlfile):
    init_commit = get_init_commit(git_dir, yamlfile)
    if commit_hexsha == init_commit[2]:
        return {'author': init_commit[0], 'date': init_commit[1]}
    next_commits = git.Git(git_dir).log('--reverse', '--ancestry-path', commit_hexsha + '^..master', '--format="%an;%at;%P"').split('\n')
    for l in range(0, len(next_commits)):
        next_commits[l] = next_commits[l][1:-1]

    if len(next_commits) > 0:
        if len(next_commits) > 1:
            next_commit = next_commits[1].rsplit(';', 2)
            if len(next_commit) == 3:
                auth, date, hexsha = next_commit
                if len(hexsha.split(' ')) == 2:
                    if commit_hexsha == hexsha.split(' ')[0] or commit_hexsha == hexsha.split(' ')[1]:
                        return {'author': auth, 'date': date}
        curr_ad = git.Git(git_dir).log('--reverse', '--ancestry-path', commit_hexsha + '^..' + commit_hexsha, '--format="%an;%at"')
        curr_ad = curr_ad[1:-1].rsplit(';', 1)
        if len(curr_ad) == 2:
            auth, date = curr_ad
            return {'author': auth, 'date': date}
    return {'author': 'n/a', 'date': 'n/a'}


def get_added_deleted_rules(git_dir, yamlfile):
    added_deleted_rules = {'added': [], 'deleted': [], 'added_previously': []}
    commits_rules_list = []
    adh_list = git.Git(git_dir).log('--format="%an;%at;%H"', '--follow', yamlfile).split('\n')
    for l in range(0, len(adh_list)):
        adh_list[l] = adh_list[l][1:-1]

    for adh in adh_list:
        if len(adh):
            author = adh.split(';', 2)[0]
            date = adh.split(';', 2)[1]
            commit_hexsha = adh.split(';', 2)[2]
            try:
                yamlfile_data = git.Git(git_dir).show(commit_hexsha + ':' + yamlfile)
            except git.exc.GitCommandError:
                continue

            if len(yamlfile_data) == 0:
                continue
            try:
                rules = state.load(yamlfile_data)
            except yaml.scanner.ScannerError:
                continue
            except TypeError:
                continue

            if 'rules' in rules:
                rules = rules['rules']
            rules_dict = {}
            if len(rules) == 0:
                rules = [{}]
            if type(rules) is dict:
                rules = [
                 rules]
            for rule in rules:
                rule['hexsha'] = commit_hexsha
                rule['author'] = author
                rule['date'] = date
                rules_dict[get_hash_from_rule(rule)] = rule

            commits_rules_list.append(rules_dict)

    commits_rules_list.reverse()
    if len(commits_rules_list) > 0:
        for rule_hash in commits_rules_list[0]:
            init_added_rule = commits_rules_list[0][rule_hash].copy()
            added_deleted_rules['added'].append(init_added_rule)

    if len(commits_rules_list) > 1 and len(commits_rules_list[0].values()) > 0:
        for i in range(0, len(commits_rules_list) - 1):
            commit = commits_rules_list[i]
            commit_next = commits_rules_list[(i + 1)]
            for rule_hash in commit_next:
                if rule_hash not in commit:
                    added_rule = commit_next[rule_hash].copy()
                    added_deleted_rules['added'].append(added_rule)

            for rule_hash in commit:
                if rule_hash not in commit_next:
                    deleted_rule = commit[rule_hash].copy()
                    deleted_rule['author'] = commit_next.values()[0]['author']
                    deleted_rule['date'] = commit_next.values()[0]['date']
                    deleted_rule['hexsha'] = commit_next.values()[0]['hexsha']
                    added_deleted_rules['deleted'].append(deleted_rule)
                    for ar in added_deleted_rules['added']:
                        if get_hash_from_rule(deleted_rule) == get_hash_from_rule(ar):
                            added_deleted_rules['added_previously'].append(added_deleted_rules['added'].pop(added_deleted_rules['added'].index(ar)))

    added_deleted_rules['added'].reverse()
    added_deleted_rules['deleted'].reverse()
    added_deleted_rules['added_previously'].reverse()
    return added_deleted_rules


@contextlib.contextmanager
def repo(repo, sha1=None):
    git_dir, is_clone_url = get_valid_repo(repo)
    if sha1:
        git.Git(git_dir).checkout(sha1)
    yield git_dir
    if is_clone_url:
        shutil.rmtree(git_dir)


def get_connection(vpc_id, region, **k):
    c = boto.vpc.connect_to_region(region, **k)
    if c:
        vpcs = dict((x.id, x) for x in c.get_all_vpcs())
        if vpc_id in vpcs:
            conn = vpcs[vpc_id].connection
            orig_get_only_instances = conn.get_only_instances
            orig_get_all_security_groups = conn.get_all_security_groups

            def get_only_instances(**k):
                k.setdefault('filters', {})
                k['filters'].setdefault('vpc-id', vpc_id)
                return orig_get_only_instances(**k)

            def get_all_security_groups(**k):
                k.setdefault('filters', {})
                k['filters'].setdefault('vpc-id', vpc_id)
                return orig_get_all_security_groups(**k)

            conn.get_only_instances = get_only_instances
            conn.get_all_security_groups = get_all_security_groups
            return conn


def get_id_for_group(conn, sgname):
    for sg in conn.get_all_security_groups(filters={'group-name': sgname}):
        return sg.id


def get_hexsha(repo):
    return git.Repo(repo).heads.master.commit.hexsha