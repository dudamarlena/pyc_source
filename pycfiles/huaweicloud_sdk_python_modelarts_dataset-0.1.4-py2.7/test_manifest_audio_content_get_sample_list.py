# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_audio_content_get_sample_list.py
# Compiled at: 2019-06-14 07:01:24
import os, sys
from modelarts import manifest, field_name
from modelarts.field_name import audio_content

def check_data(sample_list):
    assert len(sample_list) == 4
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset3/')
        for label in label_list:
            assert 'music, di da di da' in label or 'Hello world' in label or 'every word' in label or 'Hello manifest' in label

        assert 1 == len(label_list)


def check_data_without_label(sample_list):
    assert len(sample_list) == 1
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset3/')
        assert len(label_list) == 1


def test_single_default(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_content, False, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_single_default_usage(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_content, False, usage='train', *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_single_default_usage_inference(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_content, False, usage='inference', *args)
    assert label_type == field_name.single_lable
    assert len(sample_list) == 0
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset1/')
        for label in label_list:
            assert 'label' in label

        assert len(label_list) >= 0

    print 'Success: test_single_default_usage_inference'


def test_multi_default(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_content, False, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_default'


def test_multi_default_usage(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_content, False, usage='train', *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_default'


def test_multi_default_usage_inference(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_content, False, usage='inference', *args)
    assert label_type == field_name.single_lable
    assert len(sample_list) == 1
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset3/')
        for label in label_list:
            assert 'music，di da di da' in label or 'Hello world' in label or 'every word' in label or 'Hello manifest' in label

        assert len(label_list) == 1

    print 'Success: test_multi_default'


def test_single_exactly_match_type(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, ('modelarts/' + audio_content), True, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_exactly_match_type'


def test_multi_exactly_match_type(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, ('modelarts/' + audio_content), True, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_exactly_match_type'


def test_multi_exactly_match_type_error(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'modelarts/audio_classification', True, *args)
    assert label_type == field_name.single_lable
    check_data_without_label(sample_list)
    print 'Success: test_multi_exactly_match_type_error'


def main(argv):
    if len(argv) < 2:
        path1 = os.path.abspath('../../../') + '/resources/audio_content.manifest'
        path2 = os.path.abspath('../../../') + '/resources/audio_content_inference.manifest'
        test_single_default(path1)
        test_single_exactly_match_type(path1)
        test_single_default_usage(path1)
        test_single_default_usage_inference(path1)
        test_multi_default_usage_inference(path2)
        test_multi_exactly_match_type_error(path2)
        print 'test local Success'
    else:
        path1 = 's3://carbonsouth/manifest/audio_content.manifest'
        path2 = 's3://carbonsouth/manifest/audio_content_inference.manifest'
        ak = argv[1]
        sk = argv[2]
        endpoint = argv[3]
        test_single_default(path1, ak, sk, endpoint)
        test_single_exactly_match_type(path1, ak, sk, endpoint)
        test_multi_default_usage_inference(path2, ak, sk, endpoint)
        test_multi_exactly_match_type_error(path2, ak, sk, endpoint)
        print 'test OBS Success'


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'