# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qoaladep/aws/textract/textract.py
# Compiled at: 2020-03-10 06:22:57
# Size of source mod 2**32: 820 bytes
import boto3, base64

def textract_image(image_b64, region_name, aws_access_key_id, aws_secret_access_key, feature_types=[
 'TABLES', 'FORMS']):
    """[Function for character extraction from image using textract]
    
    Arguments:
        image_b64 {[string]} -- [String base64 of image]
    
    Keyword Arguments:
        feature_types {list} -- [Type of document wants to extract] (default: {["TABLES","FORMS"]})
    
    Returns:
        response [dict] -- [Dict of extraction image]
    """
    image_binary = base64.b64decode(image_b64)
    client = boto3.client('textract', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    response = client.analyze_document(Document={'Bytes': image_binary}, FeatureTypes=feature_types)
    return response