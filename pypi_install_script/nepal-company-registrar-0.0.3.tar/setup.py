import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nepal-company-registrar",
    version="0.0.3",
    author="Bishnu Sharma",
    author_email="sbishnu019@gmail.com",
    description="A package for nepal company registrar",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sbishnu019/nepal-company-registrar.git",
    download_url='https://github.com/sbishnu019/nepal-company-registrar/archive/v0.0.3.tar.gz',
    install_requires=[
          'requests',
          'beautifulsoup4',
      ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
