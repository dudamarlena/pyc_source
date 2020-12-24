try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='django-site-local-middleware',
    version='2020.3.31',
    packages=[
        'django_site_local_middleware',
    ],
)
