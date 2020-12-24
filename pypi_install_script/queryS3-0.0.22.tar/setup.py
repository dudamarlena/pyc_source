import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="queryS3", # Replace with your own username
    version="0.0.22",
    author="Qiao Liu, Everette Li",
    author_email="qiao.liu01@sjsu.edu, everetteli12@gmail.com",
    description="Minimum version of query s3 by label",
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8; variant=CommonMark",
    url="https://github.com/eugenechang2002/AITestResourceLibrary",
    install_requires=[
          'pandas',
          'nltk'
      ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.0',
)
