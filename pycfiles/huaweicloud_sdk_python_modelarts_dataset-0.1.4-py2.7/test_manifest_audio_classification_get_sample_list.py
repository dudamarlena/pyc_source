# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_audio_classification_get_sample_list.py
# Compiled at: 2019-06-14 07:01:24
import os, sys
from modelarts import manifest, field_name
from modelarts.field_name import audio_classification, sound_classification

def check_data(sample_list):
    assert len(sample_list) == 6 or len(sample_list) == 7
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset1/')
        for label in label_list:
            assert 'speech' in label or '1' in label or 'program' in label

        assert len(label_list) >= 0


def check_data_without_label(sample_list):
    assert len(sample_list) == 0
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset1/')
        assert len(label_list) == 0


def test_single_default(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_classification, False, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_single_default_usage(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_classification, False, usage='train', *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_single_default_usage_inference(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_classification, False, usage='inference', *args)
    assert label_type == field_name.single_lable
    assert len(sample_list) == 0
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset1/')
        for label in label_list:
            assert 'label' in label

        assert len(label_list) >= 0

    print 'Success: test_single_default_usage_inference'


def test_multi_default(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_classification, False, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_default'


def test_multi_default_usage(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_classification, False, usage='train', *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_default'


def test_multi_default_usage_inference(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, audio_classification, False, usage='inference', *args)
    assert label_type == field_name.single_lable
    assert len(sample_list) == 1
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset1/')
        for label in label_list:
            assert 'speech' in label or '1' in label or 'program' in label

        assert len(label_list) == 1

    print 'Success: test_multi_default'


def test_single_exactly_match_type(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, ('modelarts/' + audio_classification), True, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_exactly_match_type'


def test_multi_exactly_match_type(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, ('modelarts/' + audio_classification), True, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_exactly_match_type'


def test_multi_exactly_match_type_error(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'modelarts/object_detection', True, *args)
    assert label_type == field_name.multi_lable
    check_data_without_label(sample_list)
    print 'Success: test_multi_exactly_match_type_error'


def test_single_default_sound_classification(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, sound_classification, False, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_single_default_usage_sound_classification(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, sound_classification, False, usage='train', *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_default'


def test_single_default_usage_inference_sound_classification(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, sound_classification, False, usage='inference', *args)
    assert label_type == field_name.single_lable
    assert len(sample_list) == 0
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset1/')
        for label in label_list:
            assert 'label' in label

        assert len(label_list) >= 0

    print 'Success: test_single_default_usage_inference'


def test_multi_default_sound_classification(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, sound_classification, False, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_default'


def test_multi_default_usage_sound_classification(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, sound_classification, False, usage='train', *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_default'


def test_multi_default_usage_inference_sound_classification(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, sound_classification, False, usage='inference', *args)
    assert label_type == field_name.single_lable
    assert len(sample_list) == 1
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://modelartscarbon/audio/dataset1/')
        for label in label_list:
            assert 'speech' in label or '1' in label or 'program' in label

        assert len(label_list) == 1

    print 'Success: test_multi_default'


def test_single_exactly_match_type_sound_classification(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, ('modelarts/' + sound_classification), True, *args)
    assert label_type == field_name.single_lable
    check_data(sample_list)
    print 'Success: test_single_exactly_match_type'


def test_multi_exactly_match_type_sound_classification(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, ('modelarts/' + sound_classification), True, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_exactly_match_type'


def test_multi_exactly_match_type_error_sound_classification(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'modelarts/object_detection', True, *args)
    assert label_type == field_name.multi_lable
    check_data_without_label(sample_list)
    print 'Success: test_multi_exactly_match_type_error'


def main(argv):
    if len(argv) < 2:
        path1 = os.path.abspath('../../../') + '/resources/audio_classification.manifest'
        path2 = os.path.abspath('../../../') + '/resources/audio_classification_mutiple_label.manifest'
        test_single_default(path1)
        test_multi_default(path2)
        test_single_exactly_match_type(path1)
        test_multi_exactly_match_type(path2)
        test_single_default_usage(path1)
        test_single_default_usage_inference(path1)
        test_multi_default_usage(path2)
        test_multi_default_usage_inference(path2)
        test_multi_exactly_match_type_error(path2)
        test_single_default_sound_classification(path1)
        test_multi_default_sound_classification(path2)
        test_single_exactly_match_type_sound_classification(path1)
        test_multi_exactly_match_type_sound_classification(path2)
        test_single_default_usage_sound_classification(path1)
        test_single_default_usage_inference_sound_classification(path1)
        test_multi_default_usage_sound_classification(path2)
        test_multi_default_usage_inference_sound_classification(path2)
        test_multi_exactly_match_type_error_sound_classification(path2)
        print 'test local Success'
    else:
        path1 = 's3://carbonsouth/manifest/audio_classification.manifest'
        path2 = 'S3://carbonsouth/manifest/audio_classification_mutiple_label.manifest'
        ak = argv[1]
        sk = argv[2]
        endpoint = argv[3]
        test_single_default(path1, ak, sk, endpoint)
        test_multi_default(path2, ak, sk, endpoint)
        test_single_exactly_match_type(path1, ak, sk, endpoint)
        test_multi_exactly_match_type(path2, ak, sk, endpoint)
        test_single_default_sound_classification(path1, ak, sk, endpoint)
        test_multi_default_sound_classification(path2, ak, sk, endpoint)
        test_single_exactly_match_type_sound_classification(path1, ak, sk, endpoint)
        test_multi_exactly_match_type_sound_classification(path2, ak, sk, endpoint)
        print 'test OBS Success'


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'