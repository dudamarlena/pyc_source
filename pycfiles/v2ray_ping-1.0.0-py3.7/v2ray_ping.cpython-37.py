# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/v2ray/v2ray_ping.py
# Compiled at: 2018-10-12 04:55:53
# Size of source mod 2**32: 2020 bytes
import requests, json, os, sys
json_file = os.getcwd() + '/vpn.json'

def auth(user_name, password):
    url = 'https://v2rayapi.com/client/api.php?s=user.auth'
    response = requests.post(url, data={'username':user_name,  'password':password, 
     'getToken':'1'},
      timeout=15)
    data = json.loads(response.text)
    print(response.text)
    token = data['data']
    print(token)
    return token


def get_vpn_list(token):
    url = 'https://v2rayapi.com/client/api.php?s=whmcs.hosting&token=' + token
    response = requests.get(url, timeout=15)
    data = json.loads(response.text)
    nodes = data['data'][0]['node']
    print(nodes)
    dict = {}
    tsl_list = []
    for node in nodes:
        print(node)
        name = node['name']
        server = node['server']
        print(name)
        dict[name] = server
        if node['tls'] == 1:
            tsl_list.append(name)

    print(dict)
    with open(json_file, 'w') as (f):
        json.dump(dict, f)
    return (
     json_file, tsl_list)


def ping_vpn(vpn_json):
    os.system('mping -p ' + vpn_json)
    os.system('rm ' + json_file)


def main():
    user_name = sys.argv[1]
    password = sys.argv[2]
    print(user_name + ' ' + password)
    token = auth(user_name, password)
    if token is None:
        print('获取授权失败')
        return
    vpn_json, tsl_list = get_vpn_list(token)
    print(vpn_json)
    if vpn_json is None:
        print('获取vpn列表失败')
        return
    ping_vpn(vpn_json)
    print('支持 tsl 的服务器：')
    print(tsl_list)


if __name__ == '__main__':
    main()