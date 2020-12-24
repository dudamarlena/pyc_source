# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_aws_instance_type.py
# Compiled at: 2020-03-25 13:10:41
import pytest, doctest
from insights.parsers import aws_instance_type
from insights.parsers.aws_instance_type import AWSInstanceType
from insights.tests import context_wrap
from insights.parsers import SkipException, ParseException
from insights.core.plugins import ContentException
AWS_TYPE = 'r3.xlarge'
AWS_TYPE_CURL_STATS = '\n % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current\n                                  Dload  Upload   Total   Spent    Left  Speed\n\n   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0\n 100  1126  100  1126    0     0  1374k      0 --:--:-- --:--:-- --:--:-- 1099k\nr3.xlarge'
AWS_TYPE_AB_1 = ('\ncurl: (7) Failed to connect to 169.254.169.254 port 80: Connection timed out\n').strip()
AWS_TYPE_AB_2 = ("\ncurl: (7) couldn't connect to host\n").strip()
AWS_TYPE_AB_3 = ('\ncurl: (28) connect() timed out!\n').strip()
AWS_TYPE_AB_4 = ('\n.micro\n').strip()
AWS_TYPE_AB_5 = ('\nNo module named insights.tools\n').strip()

def test_aws_instance_type_ab_other():
    with pytest.raises(SkipException):
        AWSInstanceType(context_wrap(AWS_TYPE_AB_1))
    with pytest.raises(SkipException):
        AWSInstanceType(context_wrap(AWS_TYPE_AB_2))
    with pytest.raises(SkipException):
        AWSInstanceType(context_wrap(AWS_TYPE_AB_3))
    with pytest.raises(ParseException) as (pe):
        AWSInstanceType(context_wrap(AWS_TYPE_AB_4))
        assert 'Unrecognized type' in str(pe)
    with pytest.raises(ContentException) as (pe):
        AWSInstanceType(context_wrap(AWS_TYPE_AB_5))


def test_aws_instance_type_ab_empty():
    with pytest.raises(SkipException):
        AWSInstanceType(context_wrap(''))


def test_aws_instance_type():
    aws = AWSInstanceType(context_wrap(AWS_TYPE))
    assert aws.type == 'R3'
    assert aws.raw == 'r3.xlarge'
    assert 'large' in str(aws)


def test_aws_instance_type_stats():
    aws = AWSInstanceType(context_wrap(AWS_TYPE_CURL_STATS))
    assert aws.type == 'R3'
    assert aws.raw == 'r3.xlarge'
    assert 'large' in str(aws)


def test_doc_examples():
    env = {'aws_inst': AWSInstanceType(context_wrap(AWS_TYPE))}
    failed, total = doctest.testmod(aws_instance_type, globs=env)
    assert failed == 0