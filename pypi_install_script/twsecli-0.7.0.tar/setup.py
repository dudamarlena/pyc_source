from setuptools import setup, find_packages

packages = [package for package in find_packages()]

requires = [
    'requests>=2.22.0',
    'click>=6'
]

setup(
    name='twsecli',
    packages=packages,
    version='0.7.0',
    description='TWSE unofficial command-line interface',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Hans Liu',
    author_email='hansliu.tw@gmail.com',
    url='https://github.com/hansliu/twsecli',
    keywords=['twse'],
    python_requires='>=3',
    install_requires=requires,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'twsecli=twsecli.cli:main',
        ],
    }
)
