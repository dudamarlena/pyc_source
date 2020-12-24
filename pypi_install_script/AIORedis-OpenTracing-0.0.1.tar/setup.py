from setuptools import setup

'''
AIORedis-OpenTracing
-----------------

This extension provides OpenTracing instrumentation for the asyncio Redis library.
'''
setup(
    name='AIORedis-OpenTracing',
    version='0.0.1',
    url='https://github.com/Creativelair/AIORedis-Opentracing',
    download_url='https://github.com/Creativelair/AIORedis-Opentracing/archive/v0.0.1.tar.gz',
    license='BSD',
    author='Daniel Jimenez',
    author_email='danijimenez010@gmail.com',
    description='OpenTracing instrumentation for the asyncio Redis library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['aioredis_opentracing'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'asyncio',
        'opentracing>=2.0,<3',
    ],
    extras_require={
        'tests': [
            'flake8',
            'flake8-quotes',
            'mock',
            'pytest',
            'pytest-cov',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)