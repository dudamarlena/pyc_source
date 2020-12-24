#from distutils.core import setup
from setuptools import setup, Extension

with open('README.md') as f:
    long_description = f.read()

setup(
    name="RequestClient",
    packages=["RequestClient"],
    version="0.5.0",
    license="MIT",
    description="Easy-to-use and convenient request wrapper that saves coding time. For Rest Request",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Randy Chang",
    author_email="randy@randy-chang.com",
    url="https://github.com/Randy341/RequestClient",
    download_url="https://github.com/Randy341/RequestClient/archive/0.5.0.tar.gz",
    keywords=["requests","HTTP","wrapper", "client", "REST"],
    install_requires=["requests","pydash"],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)