from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

install_requires = [
    'aiohttp'
]

redis_require = [
    'aioredis',
]

test_requires = [
    'pytest',
    'pytest-asyncio'
]


setup(
    name='toggler',
    version='0.0.6',
    description='Asyncio feature-toggle utility',
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='http://github.com/borisrozumnuk/aio-unleash',
    author='Boris Rozumniuk',
    author_email='borisrozumnuk@gmail.com',
    license='MIT',
    platforms='Any',
    install_requires=install_requires,
    extras_require={
        'redis': redis_require,
        'test': test_requires
    },
    keywords='asyncio toggler feature-toggle unleash',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
    zip_safe=False
)
