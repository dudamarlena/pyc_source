from setuptools import setup

setup(
    name="vkbottle-core",
    version="1.0",
    description="Plugin Management in vkbottle",
    long_description="Plugin Management in vkbottle",
    long_description_content_type="text/markdown",
    author="timoniq",
    author_email="tesseradecades@mail.ru",
    python_requires=">=3.7.0",
    url="https://github.com/timoniq/vkbottle-core",
    packages=["vkbottle_core"],
    entry_points={
        "console_scripts": ["vkbottle=vkbottle_core.__main__:main"]
    },
    install_requires=["click", "vkbottle", "contextvars", "requests", "loguru"],
    extras_require={},
    license="GNU GENERAL PUBLIC LICENSE",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)