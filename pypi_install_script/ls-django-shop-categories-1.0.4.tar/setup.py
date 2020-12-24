from setuptools import setup, find_packages
import os

import shop_categories

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

version = shop_categories.get_version()

CLASSIFIERS = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
]

setup(
    name='ls-django-shop-categories',
    version=version,
    description='A extendable category app using django-mptt for django-shop',
    long_description=(read('README.rst') + '\n\n' +
                      read('HISTORY.rst')),
    author='Scott Sharkey',
    author_email='ssharkey@lanshark.com',
    url='http://github.com/lanshark/ls-django-shop-categories/',
    download_url =
    'https://github.com/lanshark/ls-django-shop-categories/tarball/' + version,
    license='BSD',
    packages=find_packages(),
    package_data={
        'shop_categories': [
            'templates/shop_categories/*',
            'locale/*/LC_MESSAGES/*',
        ]
    },
    classifiers=CLASSIFIERS,
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django-shop',
        'django-mptt',
        'ls-django-treeadmin',
        'ls-django-easytests',
    ],
)
