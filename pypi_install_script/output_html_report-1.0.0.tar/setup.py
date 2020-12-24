#! /usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools

# 需要将那些包导入
packages = ["output_html_report", "output_html_report.kernel_module", "output_html_report.original_data"]

# 导入静态文件
file_data = [
    ("output_html_report/templates", ["output_html_report/templates/extent_report_template.html"]),
    ("output_html_report/original_data", ["output_html_report/original_data/yaml_template"]),
]

# 第三方依赖
requires = [
    "Jinja2==2.9.5",
    "PyYAML==3.12"
]

setup(
    name="output_html_report",  # 包名称
    version="1.0.0",  # 包版本
    description="自动化生成报告",  # 包详细描述
    long_description="通过导入测试数据自动化生成html测试报告",  # 长描述，通常是readme，打包到PiPy需要
    author="张晓平",  # 作者名称
    author_email="zhangxiaoping@dianchu.com",  # 作者邮箱
    url="https://gitlab.dianchu.cc/2018248/output_html_report_py",  # 项目官网
    packages=packages,  # 项目需要的包
    data_files=file_data,  # 打包时需要打包的数据文件，如图片，配置文件等
    include_package_data=True,  # 是否需要导入静态数据文件
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3*",  # Python版本依赖
    install_requires=requires,  # 第三方库依赖
    zip_safe=False,  # 此项需要，否则卸载时报windows error
    classifiers=[  # 程序的所属分类列表
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
