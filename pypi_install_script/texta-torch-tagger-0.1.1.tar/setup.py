import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "texta-torch-tagger",
    version = read("VERSION"),
    author = "TEXTA",
    author_email = "info@texta.ee",
    description = ("texta-tagger"),
    license = "GPLv3",
    packages = [
        "texta_torch_tagger",
        "texta_torch_tagger.models.fasttext",
        "texta_torch_tagger.models.rcnn",
        "texta_torch_tagger.models.text_rnn"
    ],
    data_files = ["VERSION", "requirements.txt", "README.md"],
    long_description = read("README.md"),
    long_description_content_type="text/markdown",
    url="https://git.texta.ee/texta/texta-torch-tagger-python",
    install_requires = read("requirements.txt").split("\n"),
    include_package_data = True
)
