# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import about_us


setup(
    name='ahlev-django-about-us',
    version=about_us.__version__,
    description='django about us application',
    long_description='django about us application',
    long_description_content_type='text/x-rst',
    author='ahlev',
    author_email='ohahlev@gmail.com',
    include_package_data=True,
    url='https://github.com/ohahlev/ahlev-django-about-us/tree/%s' % about_us.__version__,
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'django-tinymce',
        'django-imagekit',
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
