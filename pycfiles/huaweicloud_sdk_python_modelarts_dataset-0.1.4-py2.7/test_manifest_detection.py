# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_detection.py
# Compiled at: 2019-06-14 07:01:24
import os, sys
from modelarts import manifest

def validate(data_set):
    assert data_set.get_size() > 7
    data_objects = data_set.get_sample_list()
    for data_object in data_objects:
        source = data_object.get_source()
        assert 's3://obs-ma/test/label-0220/datafiles/' in source
        assert '.jpg' in source
        usage = data_object.get_usage()
        assert usage == 'TRAIN'
        annotations = data_object.get_annotations()
        for annotation in annotations:
            annotation_type = annotation.get_type()
            assert annotation_type == 'modelarts/object_detection'
            annotation_name = annotation.get_name()
            assert annotation_name is None
            annotation_loc = annotation.get_loc()
            assert 's3://path/manifest/data/2007_000027' in annotation_loc
            annotation_property = annotation.get_property()
            assert None == annotation_property
            annotation_create_time = annotation.get_creation_time()
            assert '2019-02-20 03:16' in annotation_create_time

        assert annotation.get_annotation_format() == 'PASCAL VOC'
        annotation_annotated_by = annotation.get_annotated_by()
        assert annotation_annotated_by == 'human'
        print str(annotation_type) + '\t' + str(annotation_name) + '\t' + str(annotation_loc) + '\t' + str(annotation_property) + '\t' + str(annotation_create_time) + '\t' + str(annotation_annotated_by)

    return


def main(argv):
    if len(argv) < 2:
        if str(argv[0]).endswith('.manifest'):
            path = argv[0]
        else:
            path = os.path.abspath('../../../') + '/resources/detect-test-xy-V201902220951335133.manifest'
        data_set = manifest.parse_manifest(path)
        validate(data_set)
    elif len(argv) < 3:
        data_set = manifest.parse_manifest(argv[1])
        validate(data_set)
    else:
        path = argv[1]
        ak = argv[2]
        sk = argv[3]
        endpoint = argv[4]
        data_set = manifest.parse_manifest(path, ak, sk, endpoint)
        validate(data_set)


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'