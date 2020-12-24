import setuptools

setuptools.setup(
    name="trollformatter",
    version="1.0.1",
    author="Vincent Wang",
    author_email="vwangsf@gmail.com",
    description="A troll code formatter for C, C++ and Java to make your compsci teacher angry.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/bbworld1/trollformatter",
    download_url="https://gitlab.com/bbworld1/trollformatter/-/archive/v1.0.1/trollformatter-v1.0.1.tar.gz",
    packages=setuptools.find_packages(),
    scripts=["bin/trollformatter"],
    keywords="troll code-formatter formatter c c++ java",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3'
    ],
)
