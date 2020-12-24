# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/setup.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 898 bytes
from setuptools import setup, find_packages
import sys
if sys.version_info.major != 3:
    print('This Python is only compatible with Python 3, but you are running Python {}. The installation will likely fail.'.format(sys.version_info.major))
setup(name='baselines', packages=[package for package in find_packages() if package.startswith('baselines')], install_requires=[
 'gym[mujoco,atari,classic_control]',
 'scipy',
 'tqdm',
 'joblib',
 'zmq',
 'dill',
 'azure==1.0.3',
 'progressbar2',
 'mpi4py',
 'cloudpickle'], description='OpenAI baselines: high quality implementations of reinforcement learning algorithms', author='OpenAI', url='https://github.com/openai/baselines', author_email='gym@openai.com', version='0.1.4')