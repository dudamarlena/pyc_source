from setuptools import find_packages, setup

with open("README.md", "r") as in_file:
    long_description = in_file.read()

setup(
    name='log_splitter',
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/thibaultdelor/pyLogSplitter',
    license='LGPLv3',
    author='Tibo Delor',
    author_email='delor.thibault@gmail.com',
    description='A Python Logging Handler that splits output between two other handlers.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    keywords="logging handler",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: System :: Logging",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    ],
)