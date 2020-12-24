from setuptools import setup, find_packages

requirements = [
    'bayesian-optimization==1.0.1',
    'catboost==0.18.1',
    'lightgbm==2.3.0',
    'numpy==1.17.4',
    'openpyxl==3.0.0',
    'pandas==0.25.3',
    'PyContracts==1.8.12',
    'scikit-learn==0.22.1',
    'shap==0.31.0',
    'sklearn==0.0',
    'teradata==15.10.0.21',
    'teradatasql==16.20.0.59',
    'tqdm==4.41.1',
    'xgboost==0.90',
    'XlsxWriter==1.2.6']

setup(
    name="dspl",
    packages=["dspl"],
    version="0.0.14",
    include_package_data=True,
    install_requires=requirements,
    author="Nikita Varganov",
    author_email="nikita.varganov.ml@gmail.com",
    license="MIT",
    description="Library for using in DS-Platform",
    url="https://github.com/NV-27/dspl",
    download_url="https://github.com/NV-27/dspl/archive/0.0.14.tar.gz",
    keywords=["dspl", "ds_platform", "ds_template"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent"
    ]
)