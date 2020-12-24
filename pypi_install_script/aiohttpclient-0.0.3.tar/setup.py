# -*- coding: utf-8 -*-
from setuptools import setup, find_packages, Extension

setup(
    name='aiohttpclient',
    version="0.0.3",
    keywords=("request client", "asyncio", "python3.6"),
    description='',
    long_description="",
    author='caowenbin',
    author_email='cwb201314@qq.com',
    url='https://github.com/caowenbin/aioclient',
    download_url='https://github.com/caowenbin/aioclient',
    license='BSD',
    packages=["aioclient"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
       'Programming Language :: Python :: 3.6',
    ],
    ext_modules=[
        Extension(
            "aioclient.parsers.parser",
            [
                "aioclient/parsers/parser.c",
                "vendor/http-parser-2.8.1/http_parser.c",
            ],
            extra_compile_args=['-O3'],
            include_dirs=['.']
        ),
        Extension(
            "aioclient.parsers.response",
            [
                "aioclient/parsers/response.c",
                "vendor/http-parser-2.8.1/http_parser.c"
            ],
            extra_compile_args=['-O3'],
            include_dirs=['.']
        ),
        Extension(
            "aioclient.headers.headers",
            ["aioclient/headers/headers.c"],
            extra_compile_args=['-O3'],
            include_dirs=['.']
        )
    ],
    install_requires=[
        "uvloop>=0.10.2",
        "ujson>=1.35"
    ]
)
