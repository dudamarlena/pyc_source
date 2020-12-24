# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_file_info.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1FileInfo(Model):
    """Represents file information.

    :param comment: Gets or sets a comment associated with the file.
    :type comment: str
    :param extension_type: Gets or sets file extension.
    :type extension_type: str
    :param file_name_without_extension: Gets or sets file name.
    :type file_name_without_extension: str
    :param file_size: Gets or sets file size in bytes.
    :type file_size: long
    :param id: Gets or sets the file identifier.
    :type id: str
    :param location: Gets or sets the file URI.
    :type location: str
    """
    _attribute_map = {'comment': {'key': 'comment', 'type': 'str'}, 'extension_type': {'key': 'extensionType', 'type': 'str'}, 'file_name_without_extension': {'key': 'fileNameWithoutExtension', 'type': 'str'}, 'file_size': {'key': 'fileSize', 'type': 'long'}, 'id': {'key': 'id', 'type': 'str'}, 'location': {'key': 'location', 'type': 'str'}}

    def __init__(self, comment=None, extension_type=None, file_name_without_extension=None, file_size=None, id=None, location=None):
        super(MicrosoftPartnerSdkContractsV1FileInfo, self).__init__()
        self.comment = comment
        self.extension_type = extension_type
        self.file_name_without_extension = file_name_without_extension
        self.file_size = file_size
        self.id = id
        self.location = location