# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/aws/resources/ec2/ami.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 721 bytes
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.providers.aws.facade.base import AWSFacade

class AmazonMachineImages(AWSResources):

    def __init__(self, facade, region):
        super(AmazonMachineImages, self).__init__(facade)
        self.region = region

    async def fetch_all(self):
        raw_images = await self.facade.ec2.get_images(self.region)
        for raw_image in raw_images:
            name, resource = self._parse_image(raw_image)
            self[name] = resource

    def _parse_image(self, raw_image):
        raw_image['id'] = raw_image.get('ImageId')
        raw_image['name'] = raw_image.get('Name')
        return (raw_image['id'], raw_image)