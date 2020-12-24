"""Setup script for pylodash"""

import os.path
from setuptools import setup

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md"), encoding='utf-8') as f:
    README = f.read()

# This call to setup() does all the work
setup(name='pylodash',
    version='0.4.4',
    description='A modern Python utility library delivering modularity, performance & extras.',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='python lodash utilities pylodash',
    url='https://gitlab.asoft-python.com/g-tuanluu/python-training',
    author='Tuan Luu',
    author_email='tuan.luu@asnet.com.vn',
    license='MIT',
    packages=['pylodash'],
    install_requires=[
        'markdown',
    ],
    test_suite='nose2.collector.collector',
    tests_require=['nose2'],
    include_package_data=True,
    zip_safe=False)