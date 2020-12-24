from setuptools import setup, find_packages
from os import path

DIR = path.dirname(path.abspath(__file__))

DESCRIPTION = "mysql file elasticsearch utils"

AUTHORS = 'sam'

URL = 'https://gitee.com/sanmubird/sam_utils'

EMAIL = 'sanmubird@qq.com'

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

setup(
    name='samutils',
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=[
        "openpyxl>=2.6.2"
        , "pandas>=0.24.2"
        , "PyMySQL>=0.9.3"
        , "xlrd>=1.2.0"
        , "elasticsearch>=7.0.0"
    ],
    version='0.0.0.3',
    url=URL,
    author=AUTHORS,
    author_email=EMAIL,
    keywords=['mysql', 'file', 'elasticsearch'],
    tests_require=[
        'pytest'
    ],
    package_data={
        # include json and pkl files
    },
    include_package_data=True,
    python_requires='>=3'
)
