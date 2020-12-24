# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/samples/wrappers_initialization.py
# Compiled at: 2019-09-05 09:49:59
import taco.logger.logger
from taco.boto3.boto_config import Regions
import taco.aws_wrappers.ssm_wrapper.ssm_wrapper as ssm_wrapper, taco.aws_wrappers.sqs_wrapper.sqs_wrapper as sqs_wrapper, taco.aws_wrappers.s3_wrapper.s3_wrapper as s3_wrapper, taco.aws_wrappers.dynamodb_wrapper.dynamodb_wrapper as dynamodb_wrapper, taco.aws_wrappers.auto_scaler_wrapper.auto_scaler_wrapper as auto_scaler_wrapper

def initialize_wrappers(aws_access_key=None, aws_secret_key=None, region_name=Regions.n_virginia.value):
    logger = taco.logger.logger.get_logger(name='initialize_wrappers_samples')
    ssm = ssm_wrapper.SSMWrapper(logger=logger)
    if aws_secret_key is None:
        aws_secret_key = ssm.aws_secret_key
    if aws_access_key is None:
        aws_access_key = ssm.aws_access_key
    wrappers_default_kwargs = {'logger': logger, 
       'aws_access_key': aws_access_key, 
       'aws_secret_key': aws_secret_key, 
       'region_name': region_name}
    sqs = sqs_wrapper.SQSWrapper(**wrappers_default_kwargs)
    s3 = s3_wrapper.S3Wrapper(**wrappers_default_kwargs)
    auto_scaler = auto_scaler_wrapper.AutoScalerWrapper(**wrappers_default_kwargs)
    dynamodb = dynamodb_wrapper.DynamoDBWrapper(**wrappers_default_kwargs)
    dynamodb_with_auto_scaler = dynamodb_wrapper.DynamoDBWrapper(auto_scaler=auto_scaler, **wrappers_default_kwargs)
    return


def main():
    initialize_wrappers()


if __name__ == '__main__':
    main()