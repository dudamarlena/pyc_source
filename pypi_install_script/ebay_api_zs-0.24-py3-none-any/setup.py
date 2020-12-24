from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='etsy_oauth_zs',
    version='0.03',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    url='https://github.com/kambag/etsy_api_oauth_zonesmart',
    author='Kamil Bagaviev',
    author_email='kbagaviev@mail.ru',
    install_requires=[
        'urllib3==1.25.7',
        'oauth2',
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={},
    test_suite='tests',
)
