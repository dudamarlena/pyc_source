import setuptools

setuptools.setup(
    name="alfons_hbmqtt_auth",
    version="1.0.0",
    description="HBMQTT Authentication for Alfons",
    author="Anton Lindroth",
    url="https://github.com/ntoonio/alfons-hbmqtt-auth",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
		"hbmqtt==0.9.5",
        "passlib==1.7.1"
    ],
    classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License"
    ],
    entry_points={
        "hbmqtt.broker.plugins": [
            "auth_alfons = alfons_hbmqtt_auth:AlfonsHBMQTTAuthPlugin"
        ]
    }
)