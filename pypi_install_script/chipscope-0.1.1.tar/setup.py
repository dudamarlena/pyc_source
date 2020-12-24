import os

NOTICE = os.path.join(os.path.abspath(__file__), '..', '..', 'NOTICE.rst')
with open(NOTICE, 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup_cfg = dict(
    name='chipscope',
    version='0.1.1',
    description='This package name is reserved by Xilinx, Inc.',
    long_description=LONG_DESCRIPTION,
    author='Xilnx, Inc.',
    author_email='mdarnall@xilinx.com',
    url='https://www.xilinx.com',
    packages=[],
)

from distutils.core import setup
setup(**setup_cfg)
