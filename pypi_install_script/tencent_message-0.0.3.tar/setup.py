from setuptools import setup, find_packages  

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setup(  
    name = 'tencent_message',  
    version = '0.0.2',
    # keywords = ('chinesename',),  
    description = 'send message tencent message',  
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'MIT tencent_message',  
    install_requires = ["qcloudsms_py"],  
    packages = ['tencent_message'],  # 要打包的项目文件夹
    include_package_data=True,   # 自动打包文件夹内所有数据
    author = 'evanyang',  
    author_email = 'lightyiyi@qq.com',
    url = 'https://www.cnblogs.com/Evan-fanfan/',
    # packages = find_packages(include=("*"),),  
)  
