try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name="sangjee",
    packages=["hello"],
    version="0.1",
    description="A collection of python utils and classes",
    author="Sangjee Dondrub",
    author_email="sangjeedondrub@live.com",
    url="http://banzhida.com",
    license='MIT',
    download_url="http://banzhida.com/downloads",
    keywords=["python", "utils", "lumuporjects"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    include_package_data=True,
    zip_safe=True,
    long_description="""
    python package的长描述
    """
)
