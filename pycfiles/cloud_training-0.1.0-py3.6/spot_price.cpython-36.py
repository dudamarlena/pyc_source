# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\cloud_training\commands\spot_price.py
# Compiled at: 2017-10-29 22:01:51
# Size of source mod 2**32: 1136 bytes
from cloud_training import configure
from cloud_training.aws import Aws
from cloud_training.abstract_command import AbstractCommand

class SpotPriceCommand(AbstractCommand):

    def run(self) -> bool:
        regions = ['us-east-2', 'us-east-1', 'us-west-1', 'us-west-2', 'ap-south-1', 'ap-northeast-2', 'ap-southeast-1',
         'ap-southeast-2', 'ap-northeast-1', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2',
         'sa-east-1']
        if not self._args.all_regions:
            region = self._args.region if self._args.region else self._settings['region']
            if not region:
                raise ValueError('Region is not specified.')
            regions = [region]
        instance_type = self._args.instance_type if self._args.instance_type else self._settings['instance_type']
        self._print('Getting prices for a "%s" instance...' % instance_type)
        for region in regions:
            prices = Aws(configure.get_aws_profile_name(self._args.profile), region).spot_price(instance_type)
            self._print(prices)

        return True