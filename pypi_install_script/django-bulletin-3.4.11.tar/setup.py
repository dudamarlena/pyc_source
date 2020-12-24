#!/usr/bin/env python
from setuptools import find_packages, setup
import os

# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='django-bulletin',
      version='3.4.11',
      description="A simple newsletter application.",
      author='Bob Erb',
      author_email='bob.erb@aashe.org',
      url='https://github.com/aashe/django-bulletin',
      long_description=read("README.rst"),
      packages=find_packages(exclude=('tests',)),
      include_package_data=True,
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Framework :: Django',
      ],
      test_suite='tests.main',
      install_requires=[
          "Django==1.9.13",
          "Pillow<5",
          "django-bootstrap-pagination==1.5.0",
          "django-bootstrap3==7.0.0",
          "django-braces==1.4.0",
          "django-constant-contact==1.5",
          "django-cors-headers==1.1.0",
          "django-datetime-widget==0.9.3",
          "django-form-utils==1.0.2",
          "django-haystack==2.5.1",
          "django-jsonfield==0.9.15",
          "django-mathfilters==0.3.0",
          "django-polymorphic==1.1",
          "django-positions==0.5.1",
          "djangorestframework==3.3.1",
          "python-constantcontact",
          "pytz==2014.7",
          "sorl-thumbnail==12.3",
          "wsgiref==0.1.2"],
      zip_safe=False)
