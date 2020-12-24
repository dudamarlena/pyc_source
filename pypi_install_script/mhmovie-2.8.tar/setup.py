import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='mhmovie',  # How you named your package folder (MyLib)
    version='2.8',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='library for add music to video in very simple code',  # Give a short description about your library
    author='matan h',  # Type in your name
    author_email='matan.honig2@gmail.com',  # Type in your E-Mail
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/mhmovie",
    packages=['mhmovie'],
    install_requires = ["youtube-dl","pydub","moviepy","imageio_ffmpeg"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)