"""
    Set up the sdc_personalize_helpers package
"""
from setuptools import setup

setup(
    name='sdc-personalize-helpers',
    packages=[
        'sdc_personalize_helpers.maintenance',
        'sdc_personalize_helpers.event',
        'sdc_personalize_helpers.recommendations'
    ],
    install_requires=[
        'pymysql',
        'redis',
        'boto3',
        'sdc-helpers'
    ],
    description='AWS Personalize Helpers',
    version='0.3',
    url='http://github.com/RingierIMU/sdc-recommend-personalize-helpers',
    author='Ringier South Africa',
    author_email='tools@ringier.co.za',
    keywords=['pip', 'helpers', 'personalize'],
    download_url='https://github.com/RingierIMU/sdc-recommend-personalize-helpers/archive/v0.3.zip'
)
