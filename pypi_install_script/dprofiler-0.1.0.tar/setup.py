from setuptools import setup


setup(
    name='dprofiler',
    version='0.1.0',
    description='decorator profiling tool',
    author='Daisuke Tanaka',
    author_email='duaipp@gmail.com',
    url='https://github.com/disktnk/dprofiler',
    packages=['dprofiler'],
    install_requires=[
        'six',
    ],
    test_require=[
        'pytest',
    ],
)
