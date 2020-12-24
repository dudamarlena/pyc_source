from distutils.core import setup,Extension


# 关于点线面操作的打包

setup(
    name="ThreeDControl",
    version="1.3",
    url="https://github.com/bigpangl/algorithm", # 无用
    description="Just some count about point,line,and plane ,easy for myself to use",
    long_description=open("README","r",encoding="utf-8").read(),
    author="LanHao",
    author_email="bigpangl@163.com",
    packages=["ThreeDControl"],
    maintainer="LanHao",
    license="MIT"
)

