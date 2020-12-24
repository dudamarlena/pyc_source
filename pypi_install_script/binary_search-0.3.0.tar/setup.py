from setuptools import setup, find_packages


def read(fpath, encoding='utf-8'):
    with open(fpath, encoding=encoding) as f:
        return f.read()


setup(
    name='binary_search',
    description='Binary search on python sorted sequences',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    version='0.3.0',
    url='https://github.com/LemonPi/python_binary_search',
    author='Sheng Zhong',
    author_email='zhsh@umich.edu',
    # typing
    python_requires='>=3.5.*',
    packages=find_packages(),
    test_suite='pytest',
    tests_require=[
        'pytest',
    ],
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
    ],
)
