# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taco/samples/hello_world.py
# Compiled at: 2019-09-05 09:49:59
import uuid, taco.logger.logger
from taco.boto3.boto_config import Regions
import taco.aws_wrappers.ssm_wrapper.ssm_wrapper as ssm_wrapper, taco.aws_wrappers.sqs_wrapper.sqs_wrapper as sqs_wrapper, taco.aws_wrappers.sqs_wrapper.configs as sqs_configs, taco.aws_wrappers.s3_wrapper.s3_wrapper as s3_wrapper, taco.aws_wrappers.dynamodb_wrapper.dynamodb_wrapper as dynamodb_wrapper, taco.aws_wrappers.dynamodb_wrapper.table_creation_config as table_creation_config, taco.aws_wrappers.dynamodb_wrapper.consts as dynamodb_consts

def hello_world(aws_access_key=None, aws_secret_key=None, region_name=Regions.n_virginia.value):
    logger = taco.logger.logger.get_logger(name='hello_world')
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
    dynamo = dynamodb_wrapper.DynamoDBWrapper(**wrappers_default_kwargs)
    queue_name = 'queue_name'
    creating_sqs_config = sqs_configs.SQSCreationConfig(queue_name, enable_dead_letter_queue=True, force_clean_queue=False)
    sqs.create_queue(creating_sqs_config)
    sqs.send_message(queue_name, data="with all this romantic atmosphere Disaster's in the air")
    read_message = sqs.read_message(queue_name=queue_name, delete_after_receive=True)
    bucket_name = str(uuid.uuid1().hex)
    s3.create_bucket(bucket_name, region_name=Regions.ohio.value)
    file_path = 'hello_world'
    s3.upload_data_to_file(bucket_name=bucket_name, file_path=file_path, data=read_message.data)
    new_metadata = {'a': 'b'}
    s3.update_file_metadata(bucket_name=bucket_name, file_path=file_path, new_metadata=new_metadata)
    print s3.get_file_data(bucket_name=bucket_name, file_path=file_path)
    print s3.get_file_metadata(bucket_name=bucket_name, file_path=file_path)
    table_name = 'table_name'
    primary_key_name = 'primary_key_name'
    attribute_definitions = [
     dynamodb_consts.property_schema(primary_key_name, dynamodb_consts.AttributeTypes.string_type.value)]
    primary_keys = [
     dynamodb_consts.property_schema(primary_key_name, dynamodb_consts.PrimaryKeyTypes.hash_type.value)]
    table_config = table_creation_config.TableCreationConfig(table_name=table_name, primary_keys=primary_keys, attribute_definitions=attribute_definitions)
    dynamo.create_table(table_config)
    primary_key_value = 'primary_key_value'
    item_to_put = {primary_key_name: primary_key_value, 
       'another random key': 25}
    dynamo.put_item(table_name, item_to_put)
    get_requests = dynamodb_consts.batch_get_config(table_name, primary_key_name, [primary_key_value])
    print dynamo.batch_get(get_requests)
    s3.delete_bucket(bucket_name=bucket_name, delete_non_empty_bucket=True)
    sqs.delete_queue(queue_name=queue_name)
    dynamo.delete_table(table_name=table_name)
    return


def main():
    hello_world()


if __name__ == '__main__':
    main()