# coding=utf-8

from setuptools import setup, find_packages

# with open("README.md", "r",encoding='utf8') as fh:
#     long_description = fh.read()

setup(
    name='pikav1',  #
    version="1.0.1b",
    description=(
        'pika version 1.0.1'
    ),
    # long_description=open('README.md', 'r',encoding='utf8').read(),
    long_description='pika version 1.0.1',
    long_description_content_type="text/markdown",
    author='bfzs',
    author_email='909686719@qq.com',
    maintainer='ydf',
    maintainer_email='909686719@qq.com',
    license='BSD License',
    # packages=['douban'], #
    packages=find_packages(),
    # packages=['pikav1'], # 这样内层级文件夹的没有打包进去。
    include_package_data=True,
    platforms=["all"],
    url='https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=python%20pika%200.1.2&oq=pika%25200.1.2&rsv_pq=b7e4a335000036b4&rsv_t=02311V%2B0g%2Ff7n6nprJQs3bEupSVKUaT%2B7hMuLJIJ3EuFqL860ugAQCeuf6Q&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=8&rsv_sug2=0&rsv_btype=t&inputT=1899&rsv_sug4=2779',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'tornado',
        'twisted',
    ]
)
"""
打包上传
python setup_pikav1.py sdist upload -r pypi
"""
