import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="OSRSQuestTool",

    version="0.0.3",
    author="James Cerniglia",
    author_email="cerniglj1@hawkmail.newpaltz.edu",
    description="A package to help developers access a structured form of runescape quests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "runescape",
        "osrs",
        "old school runescape",
        "osrs quest",
        "osrs quest api",
        "osrs-quest-api",
        "osrs quest tool",
        "osrs-quest-tool",
        "osrs-quest-api",
        "OSRS QuestTool",
        
        "Quest Tool osrs"
    ],
    download_url='https://github.com/cerniglj1/OSRSQuestTool/archive/master.zip',
    url="https://github.com/cerniglj1/OSRSQuestTool",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
