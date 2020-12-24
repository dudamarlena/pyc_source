import os

from setuptools import setup, find_packages


def gen_data_files(*dirs):
    """打包不规则格式数据"""
    results = []

    for src_dir in dirs:
        for root,dirs,files in os.walk(src_dir):
            results.append((root, map(lambda f:root + "/" + f, files)))
    return results


setup(
    name="serverD",
    version="0.1.6",
    description="快速的服务器登录, 上传, 下载",
    long_description="快速的服务器登录, 上传, 下载",
    url="https://github.com/pansj66/serverD",
    author="shijiang Pan",
    author_email="1377161366@qq.com",
    license="MIT Licence",
    packages=find_packages(include=[
        "serverD", "serverD.*",

    ]),
    #
    # packages=find_packages(include=[
    #     "serverD", "serverD.*",
    #     "serverE", "serverE.*",
    # ]),
    include_package_data=True,

    data_files=gen_data_files("serverD/serverE"),
    platforms=["all"],

    entry_points={
        'console_scripts': [
            "go = serverD.main:main",
            "get = serverD.main:get",
            "put = serverD.main:put",
            "updateConf = serverD.main:update_conf",
        ]
    },

)

# print(gen_data_files("serverD/serverE"))
