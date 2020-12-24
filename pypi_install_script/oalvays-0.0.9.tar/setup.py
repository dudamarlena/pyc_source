import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oalvays", # Replace with your own username
    version="0.0.9",
    author="Yang Lin",
    author_email="a1072424579@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oalvay/oalvays",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
      'pandas', 'numpy', 'requests'
    ],
    python_requires='>=3.6',
)