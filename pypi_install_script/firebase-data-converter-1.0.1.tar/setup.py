import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="firebase-data-converter",
    version="1.0.1",
    author="ar-arvind",
    author_email="ar-arvind@protonmail.com",
    description="A simple python tool to convert xlsx file (excel) to json and vice versa.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ar-arvind/FirebaseDataConverter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.0",
        "Topic :: Database",
        "Topic :: Utilities",
        "Topic :: Text Processing",
        "Topic :: Text Editors",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.0',
    keywords='firebase-database excel-to-json json-to-excel',
    install_requires=['openpyxl'],
    entry_points={
    'console_scripts': [
        'firebase-data-converter = firebase_data_converter.firebase_data_converter:main',
        ],
    },
    
)
