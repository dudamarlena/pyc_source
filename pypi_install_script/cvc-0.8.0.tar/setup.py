import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cvc",
    version="0.8.0",
    author="Alston Trevelyan",
    author_email="2841563908@qq.com",
    maintainer="Alston Trevelyan",
    maintainer_email="2841563908@qq.com",
    description="Convert video to character art animation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alston-Trevelyan/cvc",
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=setuptools.find_packages(),
    install_requires=['moviepy', 'numpy', 'pillow', 'click', 'requests', 'imageio-ffmpeg'],

    package_data={
        "cvc": ['DroidSansMono.ttf'],
    },

    entry_points={  # Optional
        'console_scripts': [
            'cvc=cvc:convert',
        ],
    },
)
