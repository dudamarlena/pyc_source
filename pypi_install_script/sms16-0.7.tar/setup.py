import os
from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='sms16',
    packages=['sms16'],
    version='0.7',
    license='Apache Software License',
    description='The library implements sending SMS messages via sms16.ru service.',
    long_description=README,
    author='pixel365',
    author_email='pixel.365.24@gmail.com',
    url='https://github.com/pixel365/sms16',
    download_url='https://github.com/pixel365/sms16/archive/master.zip',
    keywords=['sms', 'sms16.ru'],
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only'
    ],
)
