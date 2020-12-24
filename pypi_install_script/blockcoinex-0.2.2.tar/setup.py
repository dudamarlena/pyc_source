from setuptools import setup

setup(
    name="blockcoinex",
    version = "0.2.2",
    packages = ["blockcoinex"],
    description = "Exchange information STEEM, BTC, LTC, TRY etc with exchange platforms.",
    author = "Hakan Çelik",
    author_email = "hakancelik96@outlook.com",
    url = "https://github.com/hakancelik96/blockcoinex",
    python_requires='>=3.5.0',
    py_modules=['blockcoinex'],
    include_package_data = True,
    install_requires = ["requests"],
    keywords = ["Exchange","STEEM","BTC","Blocktrades","Koinim","LTC","SBD","TRY"],
    license = "MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
