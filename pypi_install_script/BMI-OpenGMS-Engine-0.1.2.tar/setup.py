from __future__ import print_function
from setuptools import setup, find_packages
from BMI_OpenGMS_Engine import BMIOpenGMSEngine
import sys

setup(
    name="BMI-OpenGMS-Engine",
    version="0.1.2",
    author="Fengyuan Zhang",
    author_email="zhangfengyuangis@163.com",
    description="Python Framework.",
    license="MIT",
    url="", 
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    data_files=[
        "BMI_OpenGMS_Engine/resource/template/init.pyt",
        "BMI_OpenGMS_Engine/resource/bmi/__init__.py",
        "BMI_OpenGMS_Engine/resource/bmi/base.py",
        "BMI_OpenGMS_Engine/resource/bmi/bmi.py",
        "BMI_OpenGMS_Engine/resource/bmi/getter_setter.py",
        "BMI_OpenGMS_Engine/resource/bmi/grid_rectilinear.py",
        "BMI_OpenGMS_Engine/resource/bmi/grid_structured_quad.py",
        "BMI_OpenGMS_Engine/resource/bmi/grid_uniform_rectilinear.py",
        "BMI_OpenGMS_Engine/resource/bmi/grid_unstructured.py",
        "BMI_OpenGMS_Engine/resource/bmi/grid.py",
        "BMI_OpenGMS_Engine/resource/bmi/info.py",
        "BMI_OpenGMS_Engine/resource/bmi/time.py",
        "BMI_OpenGMS_Engine/resource/bmi/vars.py",
        "BMI_OpenGMS_Engine/resource/license.txt",
        "BMI_OpenGMS_Engine/resource/modeldatahandler.py",
        "BMI_OpenGMS_Engine/resource/modelservicecontext.py",
    ],
    install_requires=[
        'numpy>=1.14.0'
    ],
    zip_safe=True,
)