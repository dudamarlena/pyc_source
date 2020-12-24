# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/ec2nodes.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 12339 bytes
from __future__ import absolute_import
from six import iteritems
import requests, os, json, datetime, logging, textwrap
logger = logging.getLogger(__name__)
dirname = os.path.dirname(__file__)
EC2Regions = {'us-west-1':'US West (N. California)', 
 'us-west-2':'US West (Oregon)', 
 'us-east-1':'US East (N. Virginia)', 
 'us-east-2':'US East (Ohio)', 
 'us-gov-west-1':'AWS GovCloud (US)', 
 'ca-central-1':'Canada (Central)', 
 'ap-northeast-1':'Asia Pacific (Tokyo)', 
 'ap-northeast-2':'Asia Pacific (Seoul)', 
 'ap-northeast-3':'Asia Pacific (Osaka-Local)', 
 'ap-southeast-1':'Asia Pacific (Singapore)', 
 'ap-southeast-2':'Asia Pacific (Sydney)', 
 'ap-south-1':'Asia Pacific (Mumbai)', 
 'eu-west-1':'EU (Ireland)', 
 'eu-west-2':'EU (London)', 
 'eu-west-3':'EU (Paris)', 
 'eu-central-1':'EU (Frankfurt)', 
 'sa-east-1':'South America (Sao Paulo)'}

class InstanceType(object):
    __slots__ = ('name', 'cores', 'memory', 'disks', 'disk_capacity')

    def __init__(self, name, cores, memory, disks, disk_capacity):
        self.name = name
        self.cores = cores
        self.memory = memory
        self.disks = disks
        self.disk_capacity = disk_capacity

    def __str__(self):
        return 'Type: {}\nCores: {}\nDisks: {}\nMemory: {}\nDisk Capacity: {}\n'.format(self.name, self.cores, self.disks, self.memory, self.disk_capacity)

    def __eq__(self, other):
        if self.name == other.name:
            if self.cores == other.cores:
                if self.memory == other.memory:
                    if self.disks == other.disks:
                        if self.disk_capacity == other.disk_capacity:
                            return True
        return False


def isNumber(s):
    """
    Determines if a unicode string (that may include commas) is a number.

    :param s: Any unicode string.
    :return: True if s represents a number, False otherwise.
    """
    s = s.replace(',', '')
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError) as e:
        pass

    return False


def parseStorage(storageData):
    """
    Parses EC2 JSON storage param string into a number.

    Examples:
        "2 x 160 SSD"
        "3 x 2000 HDD"
        "EBS only"
        "1 x 410"
        "8 x 1.9 NVMe SSD"
        "900 GB NVMe SSD"

    :param str storageData: EC2 JSON storage param string.
    :return: Two floats representing: (# of disks), and (disk_capacity in GiB of each disk).
    """
    if storageData == 'EBS only':
        return [
         0, 0]
    else:
        specs = storageData.strip().split()
        if isNumber(specs[0]):
            if specs[1] == 'x':
                if isNumber(specs[2]):
                    return (
                     float(specs[0].replace(',', '')), float(specs[2].replace(',', '')))
        if isNumber(specs[0]):
            if specs[1] == 'GB':
                if specs[2] == 'NVMe':
                    if specs[3] == 'SSD':
                        return (
                         1, float(specs[0].replace(',', '')))
    raise RuntimeError('EC2 JSON format has likely changed.  Error parsing disk specs.')


def parseMemory(memAttribute):
    """
    Returns EC2 'memory' string as a float.

    Format should always be '#' GiB (example: '244 GiB' or '1,952 GiB').
    Amazon loves to put commas in their numbers, so we have to accommodate that.
    If the syntax ever changes, this will raise.

    :param memAttribute: EC2 JSON memory param string.
    :return: A float representing memory in GiB.
    """
    mem = memAttribute.replace(',', '').split()
    if mem[1] == 'GiB':
        return float(mem[0])
    raise RuntimeError('EC2 JSON format has likely changed.  Error parsing memory.')


def fetchEC2Index(filename):
    """Downloads and writes the AWS Billing JSON to a file using the AWS pricing API.

    See: https://aws.amazon.com/blogs/aws/new-aws-price-list-api/

    :return: A dict of InstanceType objects, where the key is the string:
             aws instance name (example: 't2.micro'), and the value is an
             InstanceType object representing that aws instance name.
    """
    print('Downloading ~1Gb AWS billing file to parse for information.\n')
    response = requests.get('https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json')
    if response.ok:
        with open(filename, 'w') as (f):
            f.write(str(json.dumps((json.loads(response.text)), indent=4)))
            print('Download completed successfully!\n')
    else:
        raise RuntimeError('Error: ' + str(response) + ' :: ' + str(response.text))


def fetchEC2InstanceDict(awsBillingJson, region):
    """
    Takes a JSON and returns a list of InstanceType objects representing EC2 instance params.

    :param region:
    :return:
    """
    ec2InstanceList = []
    for k, v in iteritems(awsBillingJson['products']):
        i = v['attributes']
        if i.get('location') == region:
            if i.get('tenancy') == 'Shared':
                if i.get('operatingSystem') == 'Linux':
                    if i.get('operation') == 'RunInstances':
                        normal_use = i.get('usagetype').endswith('BoxUsage:' + i['instanceType'])
                        if normal_use:
                            disks, disk_capacity = parseStorage(v['attributes']['storage'])
                            instance = InstanceType(name=(i['instanceType']), cores=(i['vcpu']),
                              memory=(parseMemory(i['memory'])),
                              disks=disks,
                              disk_capacity=disk_capacity)
                            if instance in ec2InstanceList:
                                raise RuntimeError('EC2 JSON format has likely changed.  Duplicate instance {} found.'.format(instance))
            ec2InstanceList.append(instance)

    print('Finished for ' + str(region) + '.  ' + str(len(ec2InstanceList)) + ' added.')
    return dict((_.name, _) for _ in ec2InstanceList)


def updateStaticEC2Instances():
    """
    Generates a new python file of fetchable EC2 Instances by region with current prices and specs.

    Takes a few (~3+) minutes to run (you'll need decent internet).

    :return: Nothing.  Writes a new 'generatedEC2Lists.py' file.
    """
    print("Updating Toil's EC2 lists to the most current version from AWS's bulk API.\nThis may take a while, depending on your internet connection (~1Gb file).\n")
    origFile = os.path.join(dirname, 'generatedEC2Lists.py')
    if not os.path.exists(origFile):
        raise AssertionError
    else:
        genFile = os.path.join(dirname, 'generatedEC2Lists_tmp.py')
        if os.path.exists(genFile):
            os.remove(genFile)
        awsJsonIndex = os.path.join(dirname, 'index.json')
        if not os.path.exists(awsJsonIndex):
            fetchEC2Index(filename=awsJsonIndex)
        else:
            print('Reusing previously downloaded json @: ' + awsJsonIndex)
    with open(awsJsonIndex, 'r') as (f):
        awsProductDict = json.loads(f.read())
    currentEC2List = []
    instancesByRegion = {}
    for regionNickname in EC2Regions:
        currentEC2Dict = fetchEC2InstanceDict(awsProductDict, region=(EC2Regions[regionNickname]))
        for instanceName, instanceTypeObj in iteritems(currentEC2Dict):
            if instanceTypeObj not in currentEC2List:
                currentEC2List.append(instanceTypeObj)
            instancesByRegion.setdefault(regionNickname, []).append(instanceName)

    with open(genFile, 'w') as (f):
        f.write(textwrap.dedent('\n        # !!! AUTOGENERATED FILE !!!\n        # Update with: src/toil/utils/toilUpdateEC2Instances.py\n        #\n        # Copyright (C) 2015-{year} UCSC Computational Genomics Lab\n        #\n        # Licensed under the Apache License, Version 2.0 (the "License");\n        # you may not use this file except in compliance with the License.\n        # You may obtain a copy of the License at\n        #\n        #     http://www.apache.org/licenses/LICENSE-2.0\n        #\n        # Unless required by applicable law or agreed to in writing, software\n        # distributed under the License is distributed on an "AS IS" BASIS,\n        # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n        # See the License for the specific language governing permissions and\n        # limitations under the License.\n        from six import iteritems\n        from toil.lib.ec2nodes import InstanceType\n\n\n').format(year=(datetime.date.today().strftime('%Y')))[1:])
    genString = '# {num} Instance Types.  Generated {date}.\n'.format(num=(str(len(currentEC2List))),
      date=(str(datetime.datetime.now())))
    genString = genString + 'E2Instances = {\n'
    sortedCurrentEC2List = sorted(currentEC2List, key=(lambda x: x.name))
    for i in sortedCurrentEC2List:
        z = "    '{name}': InstanceType(name='{name}', cores={cores}, memory={memory}, disks={disks}, disk_capacity={disk_capacity}),\n".format(name=(i.name),
          cores=(i.cores),
          memory=(i.memory),
          disks=(i.disks),
          disk_capacity=(i.disk_capacity))
        genString = genString + z

    genString = genString + '}\n\n'
    genString = genString + 'regionDict = {\n'
    for regionName, instanceList in iteritems(instancesByRegion):
        genString = genString + "              '{regionName}': [".format(regionName=regionName)
        for instance in sorted(instanceList):
            genString = genString + "'{instance}', ".format(instance=instance)

        if genString.endswith(', '):
            genString = genString[:-2]
        genString = genString + '],\n'

    if genString.endswith(',\n'):
        genString = genString[:-len(',\n')]
    genString = genString + '}\n'
    with open(genFile, 'a+') as (f):
        f.write(genString)
    regionKey = '\nec2InstancesByRegion = dict((region, [E2Instances[i] for i in instances]) for region, instances in iteritems(regionDict))\n'
    with open(genFile, 'a+') as (f):
        f.write(regionKey)
    if os.path.exists(origFile):
        os.remove(origFile)
    os.rename(genFile, origFile)
    if os.path.exists(awsJsonIndex):
        os.remove(awsJsonIndex)