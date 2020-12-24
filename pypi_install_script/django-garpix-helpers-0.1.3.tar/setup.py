from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'PYPI_README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-garpix-helpers',
    version='0.1.3',
    description='Django helpers.',
    long_description=long_description,
    url='https://github.com/Garpix/django-garpix-helpers',
    author='garpix',
    author_email='support@garpix.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
    ],
    keywords='django garpix helpers',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=[
        "django",
        "django-uuslug",
    ],
    extras_require={
        'dev': ['twine', 'wheel'],
    },
)
