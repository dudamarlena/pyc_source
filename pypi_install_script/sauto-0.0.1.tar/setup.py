#!/usr/bin/python

# from distutils.core import setup
from setuptools import setup, find_packages

setup(
      name='sauto',
      version='0.0.1',
      description='Simple auto task batching',
      author='Snile826',
      author_email='826245622@qq.com',
      url='https://github.com/Snile826/sauto.git',
      # 要打包的项目文件夹
      packages = find_packages('lib'),
      package_dir={"":"lib"},
      # 自动打包文件夹内所有数据
      include_package_data=True,
      # 设定项目包为安全，不用每次都检测其安全性
      zip_safe=True, 
      # 安装依赖的其他包（测试数据）
      install_requires = [
        "asn1crypto>=0.24.0",
        "bcrypt>=3.1.7",
        "cffi>=1.12.3",
        "cryptography>=2.7",
        "jinja2>=2.10.1",
        "markupsafe>=1.1.1",
        "paramiko>=2.6.0",
        "pexpect>=4.7.0",
        "psutil>=5.6.3",
        "ptyprocess>=0.6.0",
        "pycparser>=2.19",
        "pymysql>=0.9.3",
        "pynacl>=1.3.0",
        "pyyaml>=5.1.1",
        "six>=1.12.0",
      ],
      # 设置程序的入口
    # 安装后，命令行执行 `key` 相当于调用 `value`: 中的 :`value` 方法
    entry_points={
        'console_scripts':[
            'sauto = sauto.bin.Sauto:run'
        ]
    },
    python_requires='>=3.6'
)