"""Setuptools script."""

import codecs

import setuptools

with codecs.open('README.md', encoding='utf-8') as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
    name='siphash-lite',
    version='0.1.5',
    author='Azat Kurbanov',
    author_email='cordalace@gmail.com',
    description='Siphash calculation',
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    license='MIT',
    url='https://github.com/cordalace/siphash-lite',
    ext_modules=[
        setuptools.Extension(
            name='siphash',
            sources=['siphash.c', 'py.c'],
        ),
    ],
    zip_safe=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
