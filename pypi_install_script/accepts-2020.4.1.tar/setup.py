try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='accepts',
    version='2020.4.1',
    packages=[
        'accepts',
    ],
)
