# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_dataset.py
# Compiled at: 2020-03-28 01:52:01
# Size of source mod 2**32: 2600 bytes
import unittest, jittor as jt
from jittor.dataset.dataset import ImageFolder
import jittor.transform as transform
import jittor as jt, unittest, os, numpy as np, random
pass_this_test = False
msg = ''
mid = 0
if os.uname()[1] == 'jittor-ce':
    mid = 1
try:
    traindir = [
     '/data1/cjld/imagenet/train/', '/home/cjld/imagenet/train/'][mid]
    assert os.path.isdir(traindir)
except Exception as e:
    try:
        pass_this_test = True
        msg = str(e)
    finally:
        e = None
        del e

@unittest.skipIf(pass_this_test, f"can not run imagenet dataset test: {msg}")
class TestDataset(unittest.TestCase):

    def test_multi_workers(self):
        check_num_batch = 10
        tc_data = []

        def get_dataset():
            dataset = ImageFolder(traindir).set_attrs(batch_size=256, shuffle=False)
            dataset.set_attrs(transform=(transform.Compose([
             transform.Resize(224),
             transform.ImageNormalize(mean=[0.485, 0.456, 0.406], std=[
              0.229, 0.224, 0.225])])),
              num_workers=0)
            return dataset

        dataset = get_dataset()
        for i, data in enumerate(dataset):
            print('get batch', i)
            tc_data.append(data)
            if i == check_num_batch:
                break

        def check(num_workers, epoch=1):
            dataset = get_dataset().set_attrs(num_workers=num_workers)
            random.seed(0)
            for _ in range(epoch):
                for i, (images, labels) in enumerate(dataset):
                    print('compare', i)
                    assert np.allclose(images.data, tc_data[i][0].data), (
                     images.sum(), tc_data[i][0].sum(), images.shape,
                     tc_data[i][0].shape)
                    assert np.allclose(labels.data, tc_data[i][1].data)
                    if i == check_num_batch:
                        break

        check(1)
        check(2)
        check(4, 2)

    def test_collate_batch(self):
        from jittor.dataset.utils import collate_batch
        batch = collate_batch([(1, 1), (1, 2), (1, 3)])
        assert isinstance(batch[0], np.ndarray)
        assert isinstance(batch[1], np.ndarray)


if __name__ == '__main__':
    unittest.main()