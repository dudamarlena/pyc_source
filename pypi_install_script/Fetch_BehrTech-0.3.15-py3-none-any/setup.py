import setuptools

with open("gateway_package/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Fetch_BehrTech",
    version="0.3.15",
    license="MIT",
    author="Matthew Ashley",
    author_email="matthewashley@verntechnologies.com",
    description="A package to interface with BehrTech's gateway computer API for requesting and parsing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matthewashley1/Fetch_BehrTech",
    packages=setuptools.find_packages(),
    install_requires=[
      'bokeh',
      'requests',
      'wiotp-sdk'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
