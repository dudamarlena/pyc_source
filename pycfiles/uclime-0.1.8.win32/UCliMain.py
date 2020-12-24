# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python27\Lib\site-packages\ucli\UCliMain.py
# Compiled at: 2016-10-14 03:57:04
import sys, json, argparse
from UCloudApiClient import *
from UCloudApiConfig import *

class UCliMain(object):
    """命令行执行的主程序"""

    def __init__(self, apiConf=None, apiClient=None):
        if apiConf is None:
            apiConf = UCloudApiConfig()
        self.apiConf = apiConf
        self.apiClient = apiClient
        return

    def main(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('product', nargs='?', help='provide product that you want to operation', default=None)
        parser.add_argument('action', nargs='?', help='provide action that you want to operation', default=None)
        parser.add_argument('options', nargs='*', help='use name=value style get parameters', default=None)
        args = parser.parse_args()
        parameters = dict(item.split('=')[:2] for item in args.options)
        if args.product == 'configure':
            public_key = raw_input('Please enter the public_key: ')
            private_key = raw_input('Please enter the private_key: ')
            project_id = raw_input('Please enter the project_id: ')
            if public_key and private_key and project_id:
                self.apiConf.newCredentials()
                self.apiConf.updateCreadentialsUseValue(private_key, public_key, project_id)
            else:
                print 'credentials will not change'
        elif args.product == 'uhost':
            parameters['Action'] = args.action
            url = self.apiConf.getCredentialsValueByKey('base_url')
            parameters['PublicKey'] = self.apiConf.getCredentialsValueByKey('public_key')
            parameters['ProjectId'] = self.apiConf.getCredentialsValueByKey('project_id')
            pk = self.apiConf.getCredentialsValueByKey('private_key')
            if url and parameters['PublicKey'] and parameters['ProjectId'] and pk:
                self.apiClient = UCloudApiClient(url, parameters['PublicKey'], pk, parameters['ProjectId'])
                response = self.apiClient.get('/', parameters)
                print json.dumps(response, sort_keys=True, indent=4, separators=(',',
                                                                                 ': '))
            else:
                print 'credentials is not set yet, Please set first'
        elif args.product == 'ufile':
            pass
        else:
            parser.print_help()
        return


def main():
    ucli = UCliMain()
    ucli.main()


if __name__ == '__main__':
    main()