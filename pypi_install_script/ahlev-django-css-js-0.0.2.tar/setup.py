# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import css_js

setup(
    name='ahlev-django-css-js',
    version=css_js.__version__,
    description='static files',
    long_description='this django application is used to add the styles from [mdbootstrap.com](https://mdbootstrap.com) into both frontend and backend of any ahlev django project.',
    long_description_content_type='text/x-rst',
    author='ahlev',
    author_email='ohahlev@gmail.com',
    include_package_data=True,
    url='https://github.com/ohahlev/ahlev-django-css-js/tree/%s' % css_js.__version__,
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
