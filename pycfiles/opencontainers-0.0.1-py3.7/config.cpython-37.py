# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/image/v1/config.py
# Compiled at: 2019-11-04 09:56:18
# Size of source mod 2**32: 6116 bytes
from opencontainers.struct import Struct
from opencontainers.digest import Digest
from datetime import datetime

class ImageConfig(Struct):
    __doc__ = 'ImageConfig defines the execution parameters which should be used as a\n       base when running a container using an image.\n    '

    def __init__(self, user=None, ports=None, env=None, entrypoint=None, cmd=None, volumes=None, workingDir=None, labels=None, stopSignal=None):
        super().__init__()
        self.newAttr(name='User', attType=str)
        self.newAttr(name='ExposedPorts', attType=dict)
        self.newAttr(name='Env', attType=[str], regexp='^(?P<var_name>.+?)=(?P<var_value>.+)')
        self.newAttr(name='Entrypoint', attType=list)
        self.newAttr(name='Cmd', attType=list)
        self.newAttr(name='Volumes', attType=dict)
        self.newAttr(name='WorkingDir', attType=str)
        self.newAttr(name='Labels', attType=dict)
        self.newAttr(name='StopSignal', attType=str)
        self.add('User', user)
        self.add('ExposedPorts', ports)
        self.add('Env', env)
        self.add('Entrypoint', entrypoint)
        self.add('Cmd', cmd)
        self.add('Volumes', volumes)
        self.add('WorkingDir', workingDir)
        self.add('Labels', labels)
        self.add('StopSignal', stopSignal)


class RootFS(Struct):
    __doc__ = ' RootFS describes a layer content addresses\n    '

    def __init__(self, rootfs_type=None, diff_ids=None):
        super().__init__()
        self.newAttr(name='RootFSType', attType=str, omitempty=False, jsonName='type')
        self.newAttr(name='DiffIDs', attType=[Digest], omitempty=False, jsonName='diff_ids')
        self.add('RootFSType', rootfs_type)
        self.add('DiffIDs', diff_ids)


class History(Struct):
    __doc__ = 'History describes the history of a layer.\n    '

    def __init__(self, created=None, created_by=None, author=None, comment=None, empty_layer=None):
        super().__init__()
        self.newAttr('Created', attType=datetime, jsonName='created')
        self.newAttr('CreatedBy', attType=str, jsonName='created_by')
        self.newAttr('Author', attType=str, jsonName='author')
        self.newAttr('Comment', attType=str, jsonName='comment')
        self.newAttr('EmptyLayer', attType=bool, jsonName='empty_layer')
        self.add('Created', created)
        self.add('CreatedBy', created_by)
        self.add('Author', author)
        self.add('Comment', comment)
        self.add('EmptyLayer', empty_layer)


class Image(Struct):
    __doc__ = 'Image is the JSON structure which describes some basic information about \n       the image. This provides the `application/vnd.oci.image.config.v1+json` \n       mediatype when marshalled to JSON.\n    '

    def __init__(self, created=None, author=None, arch=None, imageOS=None, imageConfig=None, rootfs=None, hist=None):
        super().__init__()
        self.newAttr('Created', attType=datetime, jsonName='created')
        self.newAttr('Author', attType=str, jsonName='author')
        self.newAttr(name='Architecture', attType=str, jsonName='architecture', required=True)
        self.newAttr('OS', attType=str, jsonName='os', required=True)
        self.newAttr('Config', attType=ImageConfig, jsonName='config')
        self.newAttr('RootFS', attType=RootFS, jsonName='rootfs', required=True)
        self.newAttr('History', attType=[History], jsonName='history')
        self.add('Created', created)
        self.add('Author', author)
        self.add('Architecture', arch)
        self.add('OS', imageOS)
        self.add('Config', imageConfig)
        self.add('RootFS', rootfs)
        self.add('History', hist)