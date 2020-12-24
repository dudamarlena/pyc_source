import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gaframework",
    version="0.0.3",
    license='MIT',
    author="John Newcombe",
    author_email="jnewcombeuk@gmail.com",
    description="Simple to use genetic algorithm library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnnewcombe/gaframework",
    download_url="https://github.com/johnnewcombe/gaframework/archive/0.0.2.tar.gz",
    keywords=['genetic', 'algorithm', 'ai', 'chromosome', 'crossover', 'mutation', 'gene'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering ",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        # Common values
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
    ],
    python_requires='>=3.6',
)

