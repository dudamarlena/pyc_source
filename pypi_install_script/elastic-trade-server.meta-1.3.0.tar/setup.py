# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join, dirname
 
setup(
    name='elastic-trade-server.meta',
    version='1.3.0',
    url='http://www.elastic-trade-server.org',
    description='Сервер электронной коммерции Elastic',
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
        'elastic-trade-server.country==1.0.1',
        'elastic-trade-server.currency==1.0.0',
        'elastic-trade-server.address==1.2.0',
        'elastic-trade-server.party==1.1.1',
        'elastic-trade-server.product==1.2.4',
        'elastic-trade-server.stock==1.2.7',
        'elastic-trade-server.product_catalog==1.2.2',
        'elastic-trade-server.articles==1.0.0',
        'elastic-trade-server.delivery==1.0.0',
        'elastic-trade-server.organization==1.3.1',
        'elastic-trade-server.workflow==1.2.0',
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
