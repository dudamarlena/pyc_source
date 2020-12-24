import os
from setuptools import setup, find_packages, Extension

path = os.path.abspath(os.path.dirname(__file__))

# try:
#     with open(os.path.join(path, 'README.md')) as f:
#         long_description = f.read()
# except Exception as e:
#     long_description = "customize okta cli"
REQUIRED = [
    'future',
    'numpy',
    'protobuf>=3.5.0',
    'grpcio'
]

# if os.name == 'nt':
#     platform_package_data = ['crequest.dll', 'request.dll']
# else:
#     platform_package_data = ['libcrequest.so', 'librequest.so', 'libcshm.so']
#     if bool(os.environ.get('CUDA_VERSION', 0)):
#         platform_package_data += ['libccudashm.so']



setup(
    name="trtbertclient",
    version="0.1.1",
    keywords=["pip", "trt", "tensorrt", "client", "bert", "Jiangping"],
    description="",
    # long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3.5.0",
    license="MIT Licence",

    # url="https://github.com/stevenQiang/okta-cmd",
    author="Jiangping",
    author_email="jiangping.lei@shopee.com",

    packages=find_packages(),
    include_package_data=True,
    install_requires=REQUIRED,
    platforms="any",

    scripts=[],
    package_data={
        "":['libcrequest.so', 'librequest.so', "vocab.txt"]
    }
    # entry_points={
    #     'console_scripts': [
    #         'okta-cmd=oktacmd:main_cli'
    #     ]
    # }
)

