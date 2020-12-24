# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_text_entity_get_sample_list.py
# Compiled at: 2019-06-14 07:01:24
import os, sys
from modelarts import manifest, field_name
from modelarts.field_name import text_entity, label_separator

def check_data(sample_list):
    assert len(sample_list) == 6 or len(sample_list) == 7
    for raw_data, label_list in sample_list:
        assert 'is from' in str(raw_data)
        assert 1 == len(label_list)
        for label in label_list:
            label, start_index, end_index = str.split(label, label_separator)
            assert 'name' in label
            assert start_index in '0'
            assert 2 < int(end_index) < 9

        assert len(label_list) >= 0


def check_data_duplicate_label(sample_list):
    assert len(sample_list) == 8 or len(sample_list) == 7
    for raw_data, label_list in sample_list:
        assert 'is from' in str(raw_data)
        assert 2 == len(label_list) or 4 == len(label_list)
        for label in label_list:
            label, start_index, end_index = str.split(label, label_separator)
            if 'name' == label:
                assert start_index in '0' or start_index in '22'
                assert 2 < int(end_index) < 9 or int(end_index) == 26
            elif not ('location' == label and 12 <= int(start_index) <= 17 or 35 == int(start_index)):
                raise AssertionError
                assert 20 <= int(end_index) <= 25 or 44 == int(end_index)
            elif not False:
                raise AssertionError

        assert len(label_list) >= 0


def check_data_without_label(sample_list):
    assert len(sample_list) == 0
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('content://raw data')
        assert len(label_list) == 0


def test_single_default(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, text_entity, False, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_single_default_usage(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, text_entity, False, usage='train', *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_single_default_usage_inference(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, text_entity, False, usage='inference', *args)
    assert label_type == field_name.single_lable
    assert len(sample_list) == 0
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('raw data')
        assert len(label_list) == 0

    print 'Success: test_single_default_usage_inference'


def test_multi_default(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, text_entity, False, *args)
    assert label_type == field_name.multi_lable
    check_data_duplicate_label(sample_list)
    print 'Success: test_multi_default'


def test_multi_default_usage(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, text_entity, False, usage='train', *args)
    assert label_type == field_name.multi_lable
    check_data_duplicate_label(sample_list)
    print 'Success: test_multi_default'


def test_multi_default_usage_inference(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, text_entity, False, usage='inference', *args)
    assert label_type == field_name.multi_lable
    assert len(sample_list) == 1
    for raw_data, label_list in sample_list:
        assert 'is from' in str(raw_data)
        assert 2 == len(label_list)
        for label in label_list:
            label, start_index, end_index = str.split(label, label_separator)
            if 'name' == label:
                assert start_index in '0' or start_index in '22'
                assert 2 < int(end_index) < 9 or int(end_index) == 26
            elif not ('location' == label and 12 <= int(start_index) <= 17 or 35 == int(start_index)):
                raise AssertionError
                assert 20 <= int(end_index) <= 25 or 44 == int(end_index)
            elif not False:
                raise AssertionError

        assert len(label_list) == 2

    print 'Success: test_multi_default'


def test_single_exactly_match_type(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, ('modelarts/' + text_entity), True, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_exactly_match_type'


def test_multi_exactly_match_type(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, ('modelarts/' + text_entity), True, *args)
    assert label_type == field_name.multi_lable
    check_data_duplicate_label(sample_list)
    print 'Success: test_multi_exactly_match_type'


def test_multi_exactly_match_type_error(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'modelarts/object_detection', True, *args)
    assert label_type == field_name.multi_lable
    check_data_without_label(sample_list)
    print 'Success: test_multi_exactly_match_type_error'


def main(argv):
    if len(argv) < 2:
        path1 = os.path.abspath('../../../') + '/resources/text_entity.manifest'
        path2 = os.path.abspath('../../../') + '/resources/text_entity_duplicate_label.manifest'
        test_single_default(path1)
        test_multi_default(path2)
        test_single_exactly_match_type(path1)
        test_multi_exactly_match_type(path2)
        test_single_default_usage(path1)
        test_single_default_usage_inference(path1)
        test_multi_default_usage(path2)
        test_multi_default_usage_inference(path2)
        test_multi_exactly_match_type_error(path2)
        print 'test local Success'
    else:
        path1 = 's3://carbonsouth/manifest/text_entity.manifest'
        path2 = 'S3://carbonsouth/manifest/text_entity_duplicate_label.manifest'
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