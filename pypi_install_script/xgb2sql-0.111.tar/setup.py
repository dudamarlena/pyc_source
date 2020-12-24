from distutils.core import setup

setup(
    name="xgb2sql",
    packages=["xgb2sql"],
    version="0.111",
    license="MIT",
    description="A simple library for converting the output of an XGB model to a SQL statement.",
    author="Benjamin Jiang",
    author_email="benjaminyjiang@gmail.com",
    url="https://github.com/Chryzanthemum/xgb2sql",
    download_url="https://github.com/Chryzanthemum/xgb2sql/archive/v_011.tar.gz",
    keywords=["xgb", "xgboost", "sql", "xgb to sql", "xgboost to sql", "xgb2sql"],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
