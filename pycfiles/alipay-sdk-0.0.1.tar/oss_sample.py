# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\oss\oss_sample.py
# Compiled at: 2013-10-28 08:26:54
import time
try:
    from oss.oss_api import *
except:
    from oss_api import *

try:
    from oss.oss_xml_handler import *
except:
    from oss_xml_handler import *

HOST = 'oss.aliyuncs.com'
ACCESS_ID = ''
SECRET_ACCESS_KEY = ''
if __name__ == '__main__':
    if len(ACCESS_ID) == 0 or len(SECRET_ACCESS_KEY) == 0:
        print 'Please make sure ACCESS_ID and SECRET_ACCESS_KEY are correct in ', __file__, ', init are empty!'
        exit(0)
    oss = OssAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY)
    sep = '=============================='
    method = 'GET'
    bucket = 'test' + time.strftime('%Y-%b-%d%H-%M-%S').lower()
    object = 'test_object'
    url = 'http://' + HOST + '/oss/' + bucket + '/' + object
    headers = {}
    resource = '/' + bucket + '/' + object
    timeout = 60
    url_with_auth = oss.sign_url_auth_with_expire_time(method, url, headers, resource, timeout)
    print 'after signature url is: ', url_with_auth
    print sep
    acl = 'private'
    headers = {}
    res = oss.put_bucket(bucket, acl, headers)
    if res.status / 100 == 2:
        print 'put bucket ', bucket, 'OK'
    else:
        print 'put bucket ', bucket, 'ERROR'
    print sep
    res = oss.get_service()
    if res.status / 100 == 2:
        body = res.read()
        h = GetServiceXml(body)
        print 'bucket list size is: ', len(h.list())
        print 'bucket list is: '
        for i in h.list():
            print i

    else:
        print res.status
    print sep
    object = 'object_test'
    input_content = 'hello, OSS'
    content_type = 'text/HTML'
    headers = {}
    res = oss.put_object_from_string(bucket, object, input_content, content_type, headers)
    if res.status / 100 == 2:
        print 'put_object_from_string OK'
    else:
        print 'put_object_from_string ERROR'
    print sep
    object = 'object_test'
    filename = __file__
    content_type = 'text/HTML'
    headers = {}
    res = oss.put_object_from_file(bucket, object, filename, content_type, headers)
    if res.status / 100 == 2:
        print 'put_object_from_file OK'
    else:
        print 'put_object_from_file ERROR'
    print sep
    object = 'object_test'
    filename = __file__
    content_type = 'text/HTML'
    headers = {}
    fp = open(filename, 'rb')
    res = oss.put_object_from_fp(bucket, object, fp, content_type, headers)
    fp.close()
    if res.status / 100 == 2:
        print 'put_object_from_fp OK'
    else:
        print 'put_object_from_fp ERROR'
    print sep
    object = 'object_test'
    headers = {}
    res = oss.get_object(bucket, object, headers)
    if res.status / 100 == 2:
        print 'get_object OK'
    else:
        print 'get_object ERROR'
    print sep
    object = 'object_test'
    headers = {}
    filename = 'get_object_test_file'
    res = oss.get_object_to_file(bucket, object, filename, headers)
    if res.status / 100 == 2:
        print 'get_object_to_file OK'
    else:
        print 'get_object_to_file ERROR'
    print sep
    object = 'object_test'
    headers = {}
    res = oss.head_object(bucket, object, headers)
    if res.status / 100 == 2:
        print 'head_object OK'
        header_map = convert_header2map(res.getheaders())
        content_len = safe_get_element('content-length', header_map)
        etag = safe_get_element('etag', header_map).upper()
        print 'content length is:', content_len
        print 'ETag is: ', etag
    else:
        print 'head_object ERROR'
    print sep
    res = oss.get_bucket_acl(bucket)
    if res.status / 100 == 2:
        body = res.read()
        h = GetBucketAclXml(body)
        print 'bucket acl is:', h.grant
    else:
        print 'get bucket acl ERROR'
    print sep
    prefix = ''
    marker = ''
    delimiter = '/'
    maxkeys = '100'
    headers = {}
    res = oss.get_bucket(bucket, prefix, marker, delimiter, maxkeys, headers)
    if res.status / 100 == 2:
        body = res.read()
        h = GetBucketXml(body)
        file_list, common_list = h.list()
        print 'object list is:'
        for i in file_list:
            print i

        print 'common list is:'
        for i in common_list:
            print i

    print sep
    res = oss.upload_large_file(bucket, object, __file__)
    if res.status / 100 == 2:
        print 'upload_large_file OK'
    else:
        print 'upload_large_file ERROR'
    print sep
    res = oss.get_object_group_index(bucket, object)
    if res.status / 100 == 2:
        print 'get_object_group_index OK'
        body = res.read()
        h = GetObjectGroupIndexXml(body)
        for i in h.list():
            print 'object group part msg:', i

    else:
        print 'get_object_group_index ERROR'
    res = oss.get_object_group_index(bucket, object)
    if res.status == 200:
        body = res.read()
        h = GetObjectGroupIndexXml(body)
        object_group_index = h.list()
        for i in object_group_index:
            if len(i) == 4 and len(i[1]) > 0:
                part_name = i[1].strip()
                res = oss.delete_object(bucket, part_name)
                if res.status != 204:
                    print 'delete part ', part_name, ' in bucket:', bucket, ' failed!'
                else:
                    print 'delete part ', part_name, ' in bucket:', bucket, ' ok'

    print sep
    upload_id = ''
    res = oss.init_multi_upload(bucket, object, headers)
    if res.status == 200:
        body = res.read()
        h = GetInitUploadIdXml(body)
        upload_id = h.upload_id
    if len(upload_id) == 0:
        print 'init upload failed!'
    else:
        print 'init upload OK!'
        print 'upload id is: %s' % upload_id
    data = 'this is test content string.'
    part_number = '1'
    res = oss.upload_part_from_string(bucket, object, data, upload_id, part_number)
    if res.status / 100 == 2:
        print 'upload part OK'
    else:
        print 'upload part ERROR'
    part_msg_xml = get_part_xml(oss, bucket, object, upload_id)
    res = oss.complete_upload(bucket, object, upload_id, part_msg_xml)
    if res.status / 100 == 2:
        print 'complete upload OK'
    else:
        print 'complete upload ERROR'
    res = oss.get_object(bucket, object)
    if res.status / 100 == 2 and res.read() == data:
        print 'verify upload OK'
    else:
        print 'verify upload ERROR'
    print sep
    object = 'object_test'
    headers = {}
    res = oss.delete_object(bucket, object, headers)
    if res.status / 100 == 2:
        print 'delete_object OK'
    else:
        print 'delete_object ERROR'
    print sep
    res = oss.delete_bucket(bucket)
    if res.status / 100 == 2:
        print 'delete bucket ', bucket, 'OK'
    else:
        print 'delete bucket ', bucket, 'ERROR'
    print sep