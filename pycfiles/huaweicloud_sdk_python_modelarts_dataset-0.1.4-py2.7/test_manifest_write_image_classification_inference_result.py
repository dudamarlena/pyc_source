# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_write_image_classification_inference_result.py
# Compiled at: 2019-06-14 07:01:24
import os, sys
from modelarts.manifest import Sample, DataSet, parse_manifest

def create_manifest():
    size = 0
    sample_list = []
    for i in range(19):
        size = size + 1
        source = 's3://obs-ma/test/classification/datafiles/1_1550650984970_' + str(i) + '.jpg'
        inference_loc = 's3://obs-ma/test/classification/datafiles/1_1550650984970_' + str(i) + '.txt'
        sample_list.append(Sample(source=source, inference_loc=inference_loc))

    return DataSet(sample=sample_list, size=size)


def validate(data_set):
    assert data_set.get_size() > 0
    data_objects = data_set.get_sample_list()
    for data_object in data_objects:
        assert 's3://obs-ma/test/classification/datafiles/' in data_object.get_source()
        assert '.jpg' in data_object.get_source()
        inference_loc = data_object.get_inference_loc()
        assert str(inference_loc).startswith('s3://obs-ma/test/classification/datafiles/1_1550650984970')


def main(argv):
    path = os.path.abspath('../../../') + '/resources/classification-xy-V201902220937263726_4.manifest'
    dataset = create_manifest()
    if len(argv) < 2:
        dataset.save(path)
        para = []
        para.append(path)
        data_set = parse_manifest(path)
        validate(data_set)
    else:
        path2 = argv[1]
        ak = argv[2]
        sk = argv[3]
        endpoint = argv[4]
        dataset.save(path2, ak, sk, endpoint)
        data_set = parse_manifest(path2, ak, sk, endpoint)
        validate(data_set)


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'