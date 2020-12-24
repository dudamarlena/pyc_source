# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_image_classification_get_sample_list.py
# Compiled at: 2019-06-14 07:01:24
import os, sys
from modelarts import manifest, field_name

def check_data(sample_list):
    assert len(sample_list) == 19
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://obs-ma/test/classification/datafiles')
        assert len(label_list) > 0


def check_data_without_label(sample_list):
    assert len(sample_list) == 0
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://obs-ma/test/classification/datafiles')
        assert len(label_list) == 0


def test_single_default(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'image_classification', False, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_single_default_usage(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'image_classification', False, usage='train', *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_multi_default(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'image_classification', False, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_default'


def test_multi_default_usage(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'image_classification', False, usage='train', *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_default'


def test_single_exactly_match_type(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'modelarts/image_classification', True, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_exactly_match_type'


def test_multi_exactly_match_type(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'modelarts/image_classification', True, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_exactly_match_type'


def test_multi_exactly_match_type_error(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'modelarts/object_detection', True, *args)
    assert label_type == field_name.multi_lable
    check_data_without_label(sample_list)
    print 'Success: test_multi_exactly_match_type_error'


def main(argv):
    if len(argv) < 2:
        path1 = os.path.abspath('../../../') + '/resources/classification-xy-V201902220937263726.manifest'
        path2 = os.path.abspath('../../../') + '/resources/classification-multi-xy-V201902220937263726.manifest'
        test_single_default(path1)
        test_multi_default(path2)
        test_single_exactly_match_type(path1)
        test_multi_exactly_match_type(path2)
        test_single_default_usage(path1)
        test_multi_default_usage(path2)
        test_multi_exactly_match_type_error(path2)
        print 'test local Success'
    else:
        path1 = 's3://carbonsouth/manifest/classification-xy-V201902220937263726.manifest'
        path2 = 'S3://carbonsouth/manifest/classification-multi-xy-V201902220937263726.manifest'
        ak = argv[1]
        sk = argv[2]
        endpoint = argv[3]
        test_single_default(path1, ak, sk, endpoint)
        test_multi_default(path2, ak, sk, endpoint)
        test_single_exactly_match_type(path1, ak, sk, endpoint)
        test_multi_exactly_match_type(path2, ak, sk, endpoint)
        print 'test OBS Success'


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'