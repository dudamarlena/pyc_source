from distutils.core import setup
import os, re
from os.path import join as pjoin


def find_packages(path):
    ret = []
    for root, dirs, files in os.walk(path):
        if '__init__.py' in files:
            ret.append(re.sub('^[^A-z0-9_]+', '', root.replace('/', '.')))
    return ret

readme = open('README.md').read()

requirements = [
    'numpy',
    'torch >= 0.4.0',
    'torchvision',
    'easydict',
    'massedit',
    'tensorboard-pytorch',
    'tensorflow-tensorboard',
]


setup(
    name='objdect',
    version='0.0.3.2',
    author='duinodu',
    author_email='472365351duino@gmail.com',
    url='https://github.com/duinodu',
    license='MIT',
    description='Unified tool for objdect detection',
    long_description=readme,

    packages=find_packages('objdect'),
    scripts=['bin/objdect-new'],
    package_data={'': ['_template/*', 
                       '_template/model/*',
                       '_template/model/layers/*',
                       '_template/model/utils/*']},

    zip_safe=True,
    install_requires=requirements,
)
