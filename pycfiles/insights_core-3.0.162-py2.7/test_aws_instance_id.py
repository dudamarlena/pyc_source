# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_aws_instance_id.py
# Compiled at: 2020-03-25 13:10:41
import pytest, doctest
from insights.parsers import aws_instance_id
from insights.parsers.aws_instance_id import AWSInstanceIdDoc, AWSInstanceIdPkcs7
from insights.tests import context_wrap
from insights.parsers import SkipException, ParseException
AWS_CURL_ERROR = "\ncurl: (7) couldn't connect to host\n"
AWS_ID_DOC = '\n{\n    "devpayProductCodes" : null,\n    "marketplaceProductCodes" : [ "1abc2defghijklm3nopqrs4tu" ],\n    "availabilityZone" : "us-west-2b",\n    "privateIp" : "10.158.112.84",\n    "version" : "2017-09-30",\n    "instanceId" : "i-1234567890abcdef0",\n    "billingProducts" : [ "bp-6ba54002" ],\n    "instanceType" : "t2.micro",\n    "accountId" : "123456789012",\n    "imageId" : "ami-5fb8c835",\n    "pendingTime" : "2016-11-19T16:32:11Z",\n    "architecture" : "x86_64",\n    "kernelId" : null,\n    "ramdiskId" : null,\n    "region" : "us-west-2"\n}'
AWS_ID_DOC_CURL_STATS = '\n% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current\n                                 Dload  Upload   Total   Spent    Left  Speed\n\n  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0\n100   483  100   483    0     0   607k      0 --:--:-- --:--:-- --:--:--  471k\n{\n    "devpayProductCodes" : null,\n    "marketplaceProductCodes" : [ "1abc2defghijklm3nopqrs4tu" ],\n    "availabilityZone" : "us-west-2b",\n    "privateIp" : "10.158.112.84",\n    "version" : "2017-09-30",\n    "instanceId" : "i-1234567890abcdef0",\n    "billingProducts" : [ "bp-6ba54002" ],\n    "instanceType" : "t2.micro",\n    "accountId" : "123456789012",\n    "imageId" : "ami-5fb8c835",\n    "pendingTime" : "2016-11-19T16:32:11Z",\n    "architecture" : "x86_64",\n    "kernelId" : null,\n    "ramdiskId" : null,\n    "region" : "us-west-2"\n}'
AWS_ID_DOC_ERROR = '\nInvalid json\n'
AWS_NO_DOC = ''
AWS_ID_PKCS7 = '\nMIICiTCCAfICCQD6m7oRw0uXOjANBgkqhkiG9w0BAQUFADCBiDELMAkGA1UEBhMC\nVVMxCzAJBgNVBAgTAldBMRAwDgYDVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6\nb24xFDASBgNVBAsTC0lBTSBDb25zb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAd\nBgkqhkiG9w0BCQEWEG5vb25lQGFtYXpvbi5jb20wHhcNMTEwNDI1MjA0NTIxWhcN\nMTIwNDI0MjA0NTIxWjCBiDELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAldBMRAwDgYD\nVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6b24xFDASBgNVBAsTC0lBTSBDb25z\nb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAdBgkqhkiG9w0BCQEWEG5vb25lQGFt\nYXpvbi5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMaK0dn+a4GmWIWJ\n21uUSfwfEvySWtC2XADZ4nB+BLYgVIk60CpiwsZ3G93vUEIO3IyNoH/f0wYK8m9T\nrDHudUZg3qX4waLG5M43q7Wgc/MbQITxOUSQv7c7ugFFDzQGBzZswY6786m86gpE\nIbb3OhjZnzcvQAaRHhdlQWIMm2nrAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAtCu4\nnUhVVxYUntneD9+h8Mg9q6q+auNKyExzyLwaxlAoo7TJHidbtS4J5iNmZgXL0Fkb\nFFBjvSfpJIlJ00zbhNYS5f6GuoEDmFJl0ZxBHjJnyp378OD8uTs7fLvjx79LjSTb\nNYiytVbZPQUQ5Yaxu2jXnimvw3rrszlaEXAMPLE'
AWS_ID_PKCS7_CURL_STATS = '\n % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current\n                                  Dload  Upload   Total   Spent    Left  Speed\n\n   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0\n 100  1126  100  1126    0     0  1374k      0 --:--:-- --:--:-- --:--:-- 1099k\nMIICiTCCAfICCQD6m7oRw0uXOjANBgkqhkiG9w0BAQUFADCBiDELMAkGA1UEBhMC\nVVMxCzAJBgNVBAgTAldBMRAwDgYDVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6\nb24xFDASBgNVBAsTC0lBTSBDb25zb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAd\nBgkqhkiG9w0BCQEWEG5vb25lQGFtYXpvbi5jb20wHhcNMTEwNDI1MjA0NTIxWhcN\nMTIwNDI0MjA0NTIxWjCBiDELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAldBMRAwDgYD\nVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6b24xFDASBgNVBAsTC0lBTSBDb25z\nb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAdBgkqhkiG9w0BCQEWEG5vb25lQGFt\nYXpvbi5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMaK0dn+a4GmWIWJ\n21uUSfwfEvySWtC2XADZ4nB+BLYgVIk60CpiwsZ3G93vUEIO3IyNoH/f0wYK8m9T\nrDHudUZg3qX4waLG5M43q7Wgc/MbQITxOUSQv7c7ugFFDzQGBzZswY6786m86gpE\nIbb3OhjZnzcvQAaRHhdlQWIMm2nrAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAtCu4\nnUhVVxYUntneD9+h8Mg9q6q+auNKyExzyLwaxlAoo7TJHidbtS4J5iNmZgXL0Fkb\nFFBjvSfpJIlJ00zbhNYS5f6GuoEDmFJl0ZxBHjJnyp378OD8uTs7fLvjx79LjSTb\nNYiytVbZPQUQ5Yaxu2jXnimvw3rrszlaEXAMPLE'

def test_aws_instance_id_doc():
    with pytest.raises(SkipException):
        AWSInstanceIdDoc(context_wrap(AWS_CURL_ERROR))
    with pytest.raises(SkipException):
        AWSInstanceIdDoc(context_wrap(AWS_NO_DOC))
    with pytest.raises(ParseException) as (pe):
        AWSInstanceIdDoc(context_wrap(AWS_ID_DOC_ERROR))
        assert 'Failed to parse json' in str(pe)
    doc = AWSInstanceIdDoc(context_wrap(AWS_ID_DOC))
    assert doc is not None
    assert doc == {'devpayProductCodes': None, 
       'marketplaceProductCodes': [
                                 '1abc2defghijklm3nopqrs4tu'], 
       'availabilityZone': 'us-west-2b', 
       'privateIp': '10.158.112.84', 
       'version': '2017-09-30', 
       'instanceId': 'i-1234567890abcdef0', 
       'billingProducts': [
                         'bp-6ba54002'], 
       'instanceType': 't2.micro', 
       'accountId': '123456789012', 
       'imageId': 'ami-5fb8c835', 
       'pendingTime': '2016-11-19T16:32:11Z', 
       'architecture': 'x86_64', 
       'kernelId': None, 
       'ramdiskId': None, 
       'region': 'us-west-2'}
    assert 'whatchamacallit' not in doc
    doc = AWSInstanceIdDoc(context_wrap(AWS_ID_DOC_CURL_STATS))
    assert doc is not None
    assert doc == {'devpayProductCodes': None, 
       'marketplaceProductCodes': [
                                 '1abc2defghijklm3nopqrs4tu'], 
       'availabilityZone': 'us-west-2b', 
       'privateIp': '10.158.112.84', 
       'version': '2017-09-30', 
       'instanceId': 'i-1234567890abcdef0', 
       'billingProducts': [
                         'bp-6ba54002'], 
       'instanceType': 't2.micro', 
       'accountId': '123456789012', 
       'imageId': 'ami-5fb8c835', 
       'pendingTime': '2016-11-19T16:32:11Z', 
       'architecture': 'x86_64', 
       'kernelId': None, 
       'ramdiskId': None, 
       'region': 'us-west-2'}
    assert 'whatchamacallit' not in doc
    return


def test_aws_instance_id_pkcs7():
    with pytest.raises(SkipException):
        AWSInstanceIdDoc(context_wrap(AWS_CURL_ERROR))
    with pytest.raises(SkipException):
        AWSInstanceIdDoc(context_wrap(AWS_NO_DOC))
    pkcs7 = AWSInstanceIdPkcs7(context_wrap(AWS_ID_PKCS7))
    assert pkcs7 is not None
    assert pkcs7.signature == ('\n-----BEGIN PKCS7-----\nMIICiTCCAfICCQD6m7oRw0uXOjANBgkqhkiG9w0BAQUFADCBiDELMAkGA1UEBhMC\nVVMxCzAJBgNVBAgTAldBMRAwDgYDVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6\nb24xFDASBgNVBAsTC0lBTSBDb25zb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAd\nBgkqhkiG9w0BCQEWEG5vb25lQGFtYXpvbi5jb20wHhcNMTEwNDI1MjA0NTIxWhcN\nMTIwNDI0MjA0NTIxWjCBiDELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAldBMRAwDgYD\nVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6b24xFDASBgNVBAsTC0lBTSBDb25z\nb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAdBgkqhkiG9w0BCQEWEG5vb25lQGFt\nYXpvbi5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMaK0dn+a4GmWIWJ\n21uUSfwfEvySWtC2XADZ4nB+BLYgVIk60CpiwsZ3G93vUEIO3IyNoH/f0wYK8m9T\nrDHudUZg3qX4waLG5M43q7Wgc/MbQITxOUSQv7c7ugFFDzQGBzZswY6786m86gpE\nIbb3OhjZnzcvQAaRHhdlQWIMm2nrAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAtCu4\nnUhVVxYUntneD9+h8Mg9q6q+auNKyExzyLwaxlAoo7TJHidbtS4J5iNmZgXL0Fkb\nFFBjvSfpJIlJ00zbhNYS5f6GuoEDmFJl0ZxBHjJnyp378OD8uTs7fLvjx79LjSTb\nNYiytVbZPQUQ5Yaxu2jXnimvw3rrszlaEXAMPLE\n-----END PKCS7-----').strip()
    pkcs7 = AWSInstanceIdPkcs7(context_wrap(AWS_ID_PKCS7_CURL_STATS))
    assert pkcs7 is not None
    assert pkcs7.signature == ('\n-----BEGIN PKCS7-----\nMIICiTCCAfICCQD6m7oRw0uXOjANBgkqhkiG9w0BAQUFADCBiDELMAkGA1UEBhMC\nVVMxCzAJBgNVBAgTAldBMRAwDgYDVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6\nb24xFDASBgNVBAsTC0lBTSBDb25zb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAd\nBgkqhkiG9w0BCQEWEG5vb25lQGFtYXpvbi5jb20wHhcNMTEwNDI1MjA0NTIxWhcN\nMTIwNDI0MjA0NTIxWjCBiDELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAldBMRAwDgYD\nVQQHEwdTZWF0dGxlMQ8wDQYDVQQKEwZBbWF6b24xFDASBgNVBAsTC0lBTSBDb25z\nb2xlMRIwEAYDVQQDEwlUZXN0Q2lsYWMxHzAdBgkqhkiG9w0BCQEWEG5vb25lQGFt\nYXpvbi5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMaK0dn+a4GmWIWJ\n21uUSfwfEvySWtC2XADZ4nB+BLYgVIk60CpiwsZ3G93vUEIO3IyNoH/f0wYK8m9T\nrDHudUZg3qX4waLG5M43q7Wgc/MbQITxOUSQv7c7ugFFDzQGBzZswY6786m86gpE\nIbb3OhjZnzcvQAaRHhdlQWIMm2nrAgMBAAEwDQYJKoZIhvcNAQEFBQADgYEAtCu4\nnUhVVxYUntneD9+h8Mg9q6q+auNKyExzyLwaxlAoo7TJHidbtS4J5iNmZgXL0Fkb\nFFBjvSfpJIlJ00zbhNYS5f6GuoEDmFJl0ZxBHjJnyp378OD8uTs7fLvjx79LjSTb\nNYiytVbZPQUQ5Yaxu2jXnimvw3rrszlaEXAMPLE\n-----END PKCS7-----').strip()
    return


def test_doc_examples():
    env = {'aws_id_doc': AWSInstanceIdDoc(context_wrap(AWS_ID_DOC)), 
       'aws_id_sig': AWSInstanceIdPkcs7(context_wrap(AWS_ID_PKCS7))}
    failed, total = doctest.testmod(aws_instance_id, globs=env)
    assert failed == 0