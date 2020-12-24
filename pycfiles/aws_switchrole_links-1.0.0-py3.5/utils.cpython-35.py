# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/aws_switchrole_links/utils.py
# Compiled at: 2018-07-05 05:31:36
# Size of source mod 2**32: 385 bytes


def parse_arn(arn):
    """
    Parses an ARN (Amazon Resource Identififier).

    :param arn: The arn as a string
    :returns: A dictionary with all as entries
    """
    parts = arn.split(':')
    sections = {'owner': parts[1], 
     'service': parts[2], 
     'region': parts[3], 
     'account_id': parts[4], 
     'resource': parts[5]}
    return sections