import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="android-strings-file-converter",
    version="1.0.3",
    author="ar-arvind",
    author_email="ar-arvind@protonmail.com",
    description="A simple python tool to convert android strings.xml file to xlsx and vice versa.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ar-arvind/AndroidStringsFileConverter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing",
        "Topic :: Text Editors",
    ],
    python_requires='>=3',
    keywords='android-strings xml-to-xlsx xlsx-to-xml',
    install_requires=['openpyxl'],
    entry_points={
        'console_scripts': [
            'android-strings-file-converter = android_strings_file_converter.android_strings_file_converter:main',
        ],
    }
)
