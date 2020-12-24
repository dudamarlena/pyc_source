import setuptools
import os.path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# # 获取依赖
# def read_requirements(f):
#     return [line.strip() for line in f.splitlines()
#             if not line.startswith('#')]


setuptools.setup(
    name='py_btcerscan_api',
    version='0.2.10',
    packages=['btcerscan', 'usdtscan'],
    url='https://github.com/lishulongVI/py-btcerscan-api.git',
    license='MIT',
    author='lishulongVI',
    author_email='lishulong.never@gmail.com',
    description='Python Bindings to omniexplorer.info | etherscan.io API',
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    install_requires=[
        'requests==2.22.0',
        'retrying==1.3.3'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
