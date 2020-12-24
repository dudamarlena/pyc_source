try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='django-next-view',
    version='2020.4.28',
    packages=[
        'django_next_view',
    ],
)
