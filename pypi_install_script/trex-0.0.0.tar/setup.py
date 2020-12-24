from setuptools import setup, find_packages
from trex import __version__


setup(
    author="Anthony Almarza",
    author_email="anthony@reeliolabs.com",
    name="trex",
    packages=find_packages(exclude=["tests*", "trex/tests*"]),
    version=__version__,
    url="https://github.com/anthonyalmarza/trex-py",
    download_url=(
        "https://github.com/anthonyalmarza/trex-py/tarball/"
        "v" + __version__
    ),
    license="MIT",
    description="twisted redis",
    long_description="This is a test description",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
    keywords=["twisted", "redis"],
    install_requires=[
        'twisted',
        'hiredis',
    ],
    extras_require={
        'dev': ['ipdb', 'factory-boy', 'mock', 'sphinx', 'sphinx_rtd_theme'],
    }
)
