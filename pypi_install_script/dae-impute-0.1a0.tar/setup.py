import os
from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='dae-impute',
    packages=find_packages(),
    version='0.1a',
    description='Denoising Autoencoder imputation method for pandas DataFrames',
    license='MIT License',
    author='Maksym Balatsko',
    author_email='mbalatsko@gmail.com',
    url='https://github.com/mbalatsko/dae-impute',
    download_url='https://github.com/mbalatsko/dae-impute/archive/0.1a.tar.gz',
    install_requires=[
          'tensorflow',
          'keras',
          'numpy',
          'pandas'
      ],
    keywords=['imputation', 'denoising autoecoder', 'missing values imputation'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
)