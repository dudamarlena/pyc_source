import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="welllogs", # Replace with your own username
    version="v0.1.0.1",
    author="Santiago Cuervo",
    author_email="scuervo91@gmail.com",
    description="WellLogs is a package to visualize Oil And Gas Well logs in order to make interpretetion and petrophysics analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scuervo91/welllogs",
    download_url="https://github.com/scuervo91/welllogs/archive/v0.1.0.0.tar.gz",
    packages=setuptools.find_packages(),
    install_requires=[            
        'numpy',
        'pandas',
        'matplotlib',
        'scipy'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)