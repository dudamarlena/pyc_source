from setuptools import setup, find_packages

version_parts = (4, 1, 1)
version = '.'.join(map(str, version_parts))

setup(
    name='tek',
    version=version,
    author='Torsten Schmits',
    author_email='torstenschmits@gmail.com',
    license='MIT',
    long_description='helper lib',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'crystalmethod',
        'amino>=8.0.0',
        'golgi>=1.2.0',
    ],
)
