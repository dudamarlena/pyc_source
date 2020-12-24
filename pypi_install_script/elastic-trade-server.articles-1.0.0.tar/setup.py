# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname
 
setup(
    name='elastic-trade-server.articles',
    version='1.0.0',
    description='Компонент "Каталогизатор статей" сервера электронной торговли Elastic',
    long_description=open(join(dirname(__file__), 'README')).read(),
    author='Igor S. Kovalenko',
    author_email='kovalenko@sb-soft.biz',
    namespace_packages=['elastic'],
    packages=find_packages(),
    platforms='any',
    zip_safe=False,
    include_package_data=True,
    dependency_links=[],
    install_requires=[
        'django >=1.8.3, <1.9.0',
        'django-autocomplete-light==2.2.10',
        'django-tastypie==0.13.0',
        'lxml==3.5.0',
        'defusedxml==0.4.1',
        'django-mptt==0.8.0',
        'django-taggit==0.18.0',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django :: 1.8',
    ],
)
