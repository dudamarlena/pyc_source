# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import tag

setup(
    name='ahlev-django-tag',
    version=tag.__version__,
    description='tag app using django framework',
    long_description='tag app using django framework',
    long_description_content_type='text/x-rst',
    author='ahlev',
    author_email='ohahlev@gmail.com',
    include_package_data=True,
    url='https://github.com/ohahlev/ahlev-django-tag/tree/%s' % tag.__version__,
    packages=find_packages(),
    install_requires=[
        'django-tinymce',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)

# Usage of setup.py:
# $> python setup.py register             # registering package on PYPI
# $> python setup.py build sdist upload   # build, make source dist and upload to PYPI
