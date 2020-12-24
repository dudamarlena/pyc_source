import setuptools
import os

with open("README.md", "r") as desc:
    long_description = desc.read()

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setuptools.setup(
    name='dmelon',
    version=version,
    scripts=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    author="Gerardo Rivera",
    author_email="gerardoriveratello@gmail.com",
    description="An ocean data analysis and processing utility package",
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/DangoMelon/melon_pkg",
    packages=setuptools.find_packages(),
    zip_safe=False
        )