import setuptools

setuptools.setup(
    name="adlib27",
    packages=["adlib27"],
    version="1.0.2",
    license="MIT",
    description="A library for automatic differentiation.",
    author="Camille Bean, Jerri Zhang, Mark Gakman, Rodrigo Daboin Sanchez",
    author_email="ideal1031@gmail.com",
    url="https://github.com/ad-lib27/cs207-FinalProject",
    download_url="https://github.com/ad-lib27/cs207-FinalProject/archive/1.0.2.tar.gz",
    keywords=["automatic differentiation", "derivative", "forward mode"],
    install_requires=["numpy", "pytest", "mock"],
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
    )
