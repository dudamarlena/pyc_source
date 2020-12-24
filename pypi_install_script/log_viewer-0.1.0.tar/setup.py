from os import path
from setuptools import find_packages, setup

PATH = path.abspath(path.dirname(__file__))
with open(path.join(PATH, 'README.md'), encoding='utf-8') as f:
    README = f.read()


setup(
    name='log_viewer',
    version='0.1.0',
    license='MIT',
    description='Project that exposes the logs.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='moonrollersoft',
    author_email='moonrollersoft@gmail.com',
    url='https://github.com/moonrollersoft/log-viewer/',
    download_url='https://github.com/moonrollersoft/log-viewer/archive/v0.1.0.tar.gz',
    packages=find_packages(exclude=['tests', 'docs']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'Flask == 1.*'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            "log-viewer = log_viewer.main:main",
        ],
    },
    zip_safe=False
)
