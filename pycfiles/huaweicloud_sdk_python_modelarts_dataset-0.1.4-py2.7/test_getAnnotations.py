# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_getAnnotations.py
# Compiled at: 2019-06-28 22:50:33
import sys
from modelarts import manifest

def main(argv):
    line = '{"annotation":[{"name":"cat","type":"modelarts/image_classification","creation-time":"2019-06-28 16:07:52","annotated-by":"human/ei_modelarts_y00218826_01/ei_modelarts_y00218826_01"}],"usage":"train","source":"s3://obs-lzy/train_data/data05/data0509/data4/input/猫/CAT_04/00000990_004.jpg","id":"0001842d9eb2a3078d835f0d18cf58c1"}'
    annotation_list = manifest.getAnnotations(line)
    assert 1 == len(annotation_list)
    for annotation in annotation_list:
        assert 'cat' == annotation.get_name()
        assert 'modelarts/image_classification' == annotation.get_type()
        assert '2019-06-28 16:07:52' == annotation.get_creation_time()
        assert 'human/ei_modelarts_y00218826_01/ei_modelarts_y00218826_01' == annotation.get_annotated_by()


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'