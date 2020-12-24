#######################################################################
# Copyright (c) 2019, Quasar Astronomy Group.
#
# Produced at Lawrence Berkeley National Laboratory.
# Written by V. Dumont (vincentdumont11@gmail.com).
# All rights reserved.
#
# This file is part of the QSOTOOLS software.
# For details, see astroquasar.gitlab.io/programs/qsotools
# For details about use and distribution, please read QSOTOOLS/LICENSE.
#######################################################################
import os
from distutils.core import setup
from glob import glob

def get_data_names(root):
    '''
    Return list of all filenames (not directories) under root.
    '''
    temp = [root+'/*']
    for dirpath, dirnames, filenames in os.walk(root):
        temp.extend((os.path.join(dirpath, d, '*') for d in dirnames))
    names = []
    for path in temp:
        if any(os.path.isfile(f) for f in glob(path)):
            names.append(path.replace('qsotools/',''))
    return names

package_data = {'qsotools' : get_data_names('qsotools/data')}

setup(
    name="qsotools",
    version="0.3.0",
    author="Vincent Dumont",
    author_email="vincentdumont@gmail.com",
    packages=["qsotools"],
    package_data = package_data,
    include_package_data=True,
    scripts = glob('bin/*'),
    url="https://astroquasar.gitlab.io/programs/qsotools",
    description="Data analysis tools for quasar spectroscopy research",
    install_requires=["numpy","matplotlib","scipy","astropy"]
)
