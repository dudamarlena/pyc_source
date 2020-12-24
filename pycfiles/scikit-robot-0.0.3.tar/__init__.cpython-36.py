# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iory/src/github.com/develop/scikit-robot/skrobot/data/__init__.py
# Compiled at: 2020-02-22 09:05:06
# Size of source mod 2**32: 1327 bytes
import os.path as osp, gdown
download_dir = osp.expanduser('~/.skrobot')
data_dir = osp.abspath(osp.dirname(__file__))

def fetch_urdfpath():
    gdown.cached_download(url='https://drive.google.com/uc?id=1y7Jc3QoVW6J072CrSNupfKpyLp4NNxuH',
      path=(osp.join(download_dir, 'fetch_description.tar.gz')),
      md5='fbe29ab5f3d029d165a625175b43a265',
      postprocess=(gdown.extractall),
      quiet=True)
    return osp.join(download_dir, 'fetch_description/fetch.urdf')


def kuka_urdfpath():
    return osp.join(data_dir, 'kuka_description/kuka.urdf')


def panda_urdfpath():
    gdown.cached_download(url='https://drive.google.com/uc?id=1h6ib9jpEUNa1xB2DNrnRQtqpSD2Rj9bz',
      path=(osp.join(download_dir, 'franka_description.tar.gz')),
      md5='3de5bd15262b519e3beb88f1422032ac',
      postprocess=(gdown.extractall),
      quiet=True)
    return osp.join(download_dir, 'franka_description/panda.urdf')


def pr2_urdfpath():
    gdown.cached_download(url='https://drive.google.com/uc?id=1zy4C665o6efPko7eMk4XBdHbvgFfdC-6',
      path=(osp.join(download_dir, 'pr2_description.tar.gz')),
      md5='e4fb915accdb3568a5524c92e9c35c9a',
      postprocess=(gdown.extractall),
      quiet=True)
    return osp.join(download_dir, 'pr2_description/pr2.urdf')