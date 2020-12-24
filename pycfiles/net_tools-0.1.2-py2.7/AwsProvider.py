# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nettools/provider/AwsProvider.py
# Compiled at: 2017-04-04 02:22:55
import boto3, logging, sys, traceback, ConfigParser
from nettools.provider.Provider import Provider
logger = logging.getLogger('net-tools')
DEFAULT_REGION = 'us-east-1'

class AwsProvider(Provider):

    def __init__(self):
        Provider.__init__(self)
        self.aws_regions = {}

    def verifyCredential(self, credential):
        """
        (aki, sak) = credential
        """
        try:
            aki, sak = credential
            self.aki = aki
            self.sak = sak
            client = boto3.client('ec2', region_name='us-east-1', aws_access_key_id=aki, aws_secret_access_key=sak)
            client.describe_regions()
        except:
            logger.error('Fail to verify AWS credential')
            print '\n\n#########################################\nAWS Credential looks like inaccurate.\nRestart with accurate AWS credentials\nCheck\n  ~/.aws/credentials\n  ./credentials\n#########################################\n'
            sys.exit(1)

    @staticmethod
    def loadCredential(fp):
        config = ConfigParser.RawConfigParser()
        config.read(fp)
        sections = config.sections()
        if len(sections) == 0:
            logger.error('There is no profile')
            return (
             False, None)
        else:
            wanted = 'default'
            if len(sections) > 1:
                logger.warn('There are %s sections' % sections)
                wanted = raw_input('Choose one profile %s? ')
            if not config.has_section(wanted):
                logger.error('Profile %s does not exist' % wanted)
                return (
                 False, None)
            logger.debug('Load section:%s' % wanted)
            if not config.has_option(wanted, 'aws_access_key_id'):
                logger.error('Access Key ID does not exist')
                return (
                 False, None)
            aki = config.get(wanted, 'aws_access_key_id')
            if not config.has_option(wanted, 'aws_secret_access_key'):
                logger.error('Secret Access Key does not exist')
                return (
                 False, None)
            sak = config.get(wanted, 'aws_secret_access_key')
            return (
             True, (aki, sak))

    def getClient(self, region_name=DEFAULT_REGION):
        """
        @param: region_name
        @return: Client Connection object
        """
        if not self.aki:
            logger.error('AWS Access Key ID does not exist!')
            sys.exit(1)
        if not self.sak:
            logger.error('AWS Secret Access Key does not exist!')
            sys.exit(1)
        try:
            client = boto3.client('ec2', region_name=region_name, aws_access_key_id=self.aki, aws_secret_access_key=self.sak)
            return client
        except:
            logger.error('Cannot create client object')
            logger.error('Region name: %s' % region_name)
            logger.error('Access Key ID    : %s' % self.aki)
            logger.error('Secret Access Key: %s' % self.sak)
            sys.exit(1)

    def discover(self, region_names=None):
        region_names = self.discoverRegions(region_names)
        for R in region_names:
            vpcs = self.discoverVpcs(R)
            logger.debug('%s <- Add Vpcs:%s' % (R, vpcs))
            self.regions[R].update({'VpcId': vpcs})

    def discoverRegions(self, region_names=None):
        output = []
        try:
            client = self.getClient()
            if region_names:
                response = client.describe_regions(RegionNames=region_names)
            else:
                response = client.describe_regions()
            regions = self.getValue(response, 'Regions')
            for R in regions:
                if self.regions.has_key(R['RegionName']) == False:
                    self.regions[R['RegionName']] = {'EndPoint': R['Endpoint']}
                else:
                    logger.warn('AWS Region(%s) already exist' % R['RegionName'])
                output.append(R['RegionName'])

        except:
            traceback.print_exc()

        return output

    def discoverVpcs(self, region_name):
        output = []
        try:
            client = self.getClient(region_name)
            response = client.describe_vpcs()
            vpcs = self.getValue(response, 'Vpcs')
            for V in vpcs:
                vpcid = V['VpcId']
                if self.vpcs.has_key(vpcid) == False:
                    subnets = self.discoverSubnets(region_name, vpcid)
                    V['SubnetId'] = subnets
                    self.vpcs[vpcid] = V
                else:
                    logger.warn('AWS VPC(%s) already exist' % vpcid)
                output.append(vpcid)

        except:
            traceback.print_exc()

        return output

    def getCidrByVpcId(self, vpcid):
        if self.vpcs.has_key(vpcid) == False:
            return None
        else:
            V = self.vpcs[vpcid]
            if V.has_key('CidrBlock') == False:
                logger.error('VPC exists, but CidrBlock does not exist')
                logger.error(V)
                return None
            return V['CidrBlock']

    def formatVpcs(self, region_names=None):
        rlist = []
        if region_names:
            for r_name in region_names:
                if self.regions.has_key(r_name):
                    rlist.append(r_name)

        else:
            rlist = self.regions.keys()
        rlist.sort()
        logger.debug('Region list:%s' % rlist)
        output = []
        for R in rlist:
            logger.debug('Region:%s' % R)
            if self.regions[R].has_key('VpcId') == False:
                logger.error('Region does not have VpcId')
                logger.error(self.regions[R])
                continue
            VpcIds = self.regions[R]['VpcId']
            for VpcId in VpcIds:
                logger.debug('VpcID:%s' % VpcId)
                if self.vpcs.has_key(VpcId) == False:
                    logger.error('VpcId(%s) does not exist' % VpcId)
                    logger.error('VpcId list:%s' % self.vpcs.keys())
                    continue
                V = self.vpcs[VpcId]
                v_name = self.getName(V)
                SubnetIds = V['SubnetId']
                for SubnetId in SubnetIds:
                    S = self.subnets[SubnetId]
                    az = S['AvailabilityZone']
                    s_name = self.getName(S)
                    item = [
                     R, VpcId, v_name, V['CidrBlock'], az, SubnetId, s_name, S['CidrBlock']]
                    output.append(item)

        return output

    def discoverSubnets(self, region_name, VpcId):
        output = []
        try:
            client = self.getClient(region_name)
            my_filter = [{'Name': 'vpc-id', 'Values': [VpcId]}]
            response = client.describe_subnets(Filters=my_filter)
            subnets = self.getValue(response, 'Subnets')
            logger.debug('Found %s subnets at %s' % (len(subnets), region_name))
            for S in subnets:
                subnetid = S['SubnetId']
                if self.subnets.has_key(subnetid) == False:
                    self.subnets[subnetid] = S
                else:
                    logger.warn('AWS Subnet(%s) already exist' % subnetid)
                output.append(subnetid)

        except:
            traceback.print_exc()

        return output

    def getCidrBySubnetId(self, subnetid):
        if self.subnets.has_key(subnetid) == False:
            return None
        else:
            S = self.subnets[subnetid]
            if S.has_key('CidrBlock') == False:
                logger.error('Subnet exists, but CIDR is not exist')
                logger.error(S)
                return None
            return S['CidrBlock']

    def getName(self, dic):
        name = '-'
        if dic.has_key('Tags') == False:
            return name
        tags = dic['Tags']
        logger.debug('Tags:%s' % tags)
        for tag in tags:
            if tag.has_key('Key'):
                if tag['Key'] == 'Name':
                    return tag['Value']

        return name


if __name__ == '__main__':
    test = AwsProvider()