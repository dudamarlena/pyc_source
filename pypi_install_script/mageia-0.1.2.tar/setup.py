from setuptools import setup, find_packages

parse_requirements = ['SQLAlchemy', 'PyMySQL']

setup(
    name="mageia",
    version="0.1.2",
    description="DataBase engine for you",
    long_description="mageia by stefanlei",
    license="Apache",
    url="https://github.com/stefanlei",
    author="stefanlei",
    author_email="stefanlei@qq.com",
    packages=find_packages(),
    install_requires=parse_requirements,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
