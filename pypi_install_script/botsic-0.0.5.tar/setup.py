import os
from distutils.core import setup

version = os.getenv('VERSION')


setup(
    name='botsic',
    version=version,
    description='Creates bots',
    url='https://github.com/ifosch/botsic',
    download_url=f'https://github.com/ifosch/botsic/archive/{version}.tar.gz',
    author='Ignasi Fosch',
    author_email='natx@y10k.ws',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['botsic'],
    include_package_data=True,
    install_requires=['python-telegram-bot', ],
    scripts=['bin/botsic'],
)
