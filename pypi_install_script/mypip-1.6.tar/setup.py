from setuptools import setup,find_packages

setup(
        name="mypip",
        version = "1.6",
        description = "just a test",
        long_description = "just a a a test",
        author = "davew",
        author_email = "eyaswoo@163.com",
        license = "GPLv3",
        classifiers = [
            "Development Status :: 3 - Alpha",

            "Intended Audience :: End Users/Desktop",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",

            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            ],
        packages = find_packages(),
        entry_points = {
            "console_scripts":[
                "mypip = mypip.mypip:main",
                ],
            },
       )




