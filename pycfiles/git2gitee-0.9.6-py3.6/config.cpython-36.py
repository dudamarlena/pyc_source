# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/git2gitee/config.py
# Compiled at: 2020-05-07 23:16:08
# Size of source mod 2**32: 1192 bytes
"""
Configs
"""
user_agents = [
 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0']
headers = {'User-Agent':user_agents[0], 
 'Accept-Language':'en-US,en;q=0.7,zh-CN;q=0.3', 
 'Accept-Encoding':'gzip, deflate, br', 
 'Upgrade-Insecure-Requests':'1', 
 'DNT':'1'}
gitee_base_url = 'https://gitee.com/'
project_url = gitee_base_url + 'projects/'
url_check_project_private = project_url + 'check_project_private'
url_check_project_duplicate = project_url + 'check_project_duplicate'
duplicate_response = {'is_duplicate': 'false'}
private_response = {'check_success': 'true'}

def params(repo_name, username, token, import_url):
    """
    :params repo_name: https://github.com/{username}/{repo_name}
    :params token: csrf-token in https://gitee.com/projects/import/url
    :params import_url: the github repo url
    """
    return {'utf8':'✓', 
     'authenticity_token':token, 
     'project[name]':repo_name, 
     'project[namespace_path]':username, 
     'project[path]':repo_name, 
     'project[public]':'0', 
     'project[description]':'', 
     'project[import_url]':import_url}