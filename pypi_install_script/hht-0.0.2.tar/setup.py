from setuptools import setup, find_packages
import hht

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hht',
    version=hht.__version__,
    description="A Python implementation of Hilbert-Huang Transform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Feng Zhu",
    author_email='fengzhu@usc.edu',
    url='https://github.com/fzhu2e/hht',
    packages=find_packages(),
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords='hht',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
