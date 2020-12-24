# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_write_detection.py
# Compiled at: 2019-06-14 07:01:24
import os, sys
from modelarts.test import test_manifest_detection
from modelarts.manifest import Annotation, Sample, DataSet

def create_manifest():
    size = 0
    sample_list = []
    for i in range(8):
        size = size + 1
        source = 's3://obs-ma/test/label-0220/datafiles/1 (15)_1550632618199' + str(i) + '.jpg'
        usage = 'TRAIN'
        inference_loc = 's3://obs-ma/test/label-0220/datafiles/1 (15)_1550632618199' + str(i) + '.txt'
        annotations_list = []
        for j in range(1):
            annotation_type = 'modelarts/object_detection'
            annotation_loc = 's3://path/manifest/data/2007_000027_' + str(i) + '.xml'
            annotation_creation_time = '2019-02-20 03:16:58'
            annotation_format = 'PASCAL VOC'
            annotated_by = 'human'
            annotations_list.append(Annotation(type=annotation_type, loc=annotation_loc, creation_time=annotation_creation_time, annotated_by=annotated_by, annotation_format=annotation_format))

        sample_list.append(Sample(source=source, usage=usage, annotations=annotations_list, inference_loc=inference_loc))

    return DataSet(sample=sample_list, size=size)


def main(argv):
    path = os.path.abspath('../../../') + '/resources/detect-test-xy-V201902220951335133_2.manifest'
    dataset = create_manifest()
    if len(argv) < 2:
        dataset.save(path)
        para = []
        para.append(path)
        test_manifest_detection.main(para)
    else:
        path2 = argv[1]
        ak = argv[2]
        sk = argv[3]
        endpoint = argv[4]
        dataset.save(path2, ak, sk, endpoint)


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'