from setuptools import setup

setup(
    name='django-timesince-shortener',
    version='2020.3.31',
    install_requires=[
        'Django',
        'setuptools',
    ],
    packages=[
        'django_timesince_shortener',
        'django_timesince_shortener.templatetags',
    ],
)
