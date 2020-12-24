import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-rest-serializer-field-permissions',
    version='2.0.0',
    packages=['rest_framework_serializer_field_permissions'],
    include_package_data=True,
    license='GNU General Public License v3 (GPLv3)',
    description='Field-by-field serializer permissions for Django Rest Framework.',
    long_description=README,
    url='http://intersis.github.io/django-rest-serializer-field-permissions/',
    author='Joseph Schilz',
    author_email='joseph@schilz.org',
    install_requires=[
        'django>=1.11',
        'djangorestframework>=3.5',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
