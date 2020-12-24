# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='django-licenses',
    version='0.2.5',
    description='A Django application that provides the ability to publish content under different licenses.',
    author='Bela Hausmann',
    author_email='post@belahausmann.name',
    maintainer='Jannis Leidel',
    maintainer_email='jannis@leidel.info',
    url='http://bitbucket.org/jezdez/django-licenses/',
    packages=[
        'licenses',
        'licenses.templatetags',
    ],
    package_dir={
        'licenses': 'licenses',
    },
    package_data={
        'licenses': [
            'templates/licenses/*.html',
            'fixtures/*.json'
        ]
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
