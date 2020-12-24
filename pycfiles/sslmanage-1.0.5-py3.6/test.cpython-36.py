# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sslmanage/test.py
# Compiled at: 2019-07-05 04:04:18
# Size of source mod 2**32: 2573 bytes
import argparse
from sslmanage.qiniu_ssl import QnCertManager
from sslmanage.upyun_ssl import HTTPClient, UpLogin, UpCertManager

def _qiniu_ssl(cert_option):
    print(cert_option)
    access_key = 'xx'
    secret_key = 'xx'
    cmd = QnCertManager(cert_option['root_domain'], cert_option['domain']['qiniu'], cert_option['cert_file'], cert_option['key_file'], access_key, secret_key)
    cmd.handle()


def _upyun_ssl(cert_option):
    print(cert_option)
    req_session = HTTPClient()
    UpLogin(req_session, user='xx', passwd='xx')
    certManager = UpCertManager(req_session, domain=(cert_option['domain']['upyun']),
      cert_file=(cert_option['cert_file']),
      key_file=(cert_option['key_file']))
    certManager.set_cert()


def run_test(platform, cert_option):
    platform_task = {'upyun':_upyun_ssl, 
     'qiniu':_qiniu_ssl}
    platforms = platform.split(',')
    for task in platforms:
        taskcall = platform_task.get(task)
        taskcall and taskcall(cert_option)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', help='根域如invit.vip 不加二级域名', type=str)
    parser.add_argument('--cert_dir', help='证书目录', type=str)
    parser.add_argument('--platform', help='七牛｜又拍云', type=str)
    args = parser.parse_args()
    cert_task_map = {'hlsgl.top':{'root_domain':'hlsgl.top', 
      'domain':{'upyun':[
        'wwj.hlsgl.top'], 
       'qiniu':[
        'mt-avatar.hlsgl.top', 'mt-share.hlsgl.top', 'mt-card.hlsgl.top']}, 
      'cert_file':f"{args.cert_dir}fullchain.cer", 
      'key_file':f"{args.cert_dir}{args.domain}.key"}, 
     'invit.vip':{'root_domain':'invit.vip', 
      'domain':{'qiniu': 'img1.invit.vip'}, 
      'cert_file':f"{args.cert_dir}{args.domain}.crt", 
      'key_file':f"{args.cert_dir}{args.domain}.key"}}
    run_test(args.platform, cert_task_map[args.domain])