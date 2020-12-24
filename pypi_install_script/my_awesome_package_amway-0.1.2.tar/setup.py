from setuptools import setup
import os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ['CI_JOB_ID']

setup(
    name='my_awesome_package_amway',
    version=version,
    description='My awesome package',
    author='Me',
    author_email='uni2k11@gmail.com',
    license='MIT',
    packages=['my_awesome_package_amway'],
    url='https://gitlab.com/pypri/pypri-gitlab-ci',
    zip_safe=False
)