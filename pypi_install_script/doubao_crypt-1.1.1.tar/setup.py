try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name='doubao_crypt',
    version='1.1.1',
    author='biao.xu',
    author_email='biao.xu@baodanyun-inc.com',
    description='doubao crypt python library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.5.3",
    install_requires=['eciespy', 'requests', 'redis'],
    packages=['doubao_crypt'],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
