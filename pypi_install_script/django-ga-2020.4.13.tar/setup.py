from setuptools import setup

setup(
    name='django-ga',
    version='2020.4.13',
    install_requires=[
        'Django>1.0',
        'setuptools',
    ],
    packages=[
        'django_ga',
        'django_ga.templatetags',
    ],
)
