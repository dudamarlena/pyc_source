from setuptools import find_packages, setup

setup(
    name='pyxt',
    version='1.1.1',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'requests',
    ],
)
