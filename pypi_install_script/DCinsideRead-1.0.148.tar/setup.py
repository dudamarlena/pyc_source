import setuptools

setuptools.setup(
    name = "DCinsideRead",
    version = "1.0.148",
    description = "디시인사이드를 비롯한 커뮤니티들을 크롤링합니다",
    # long_description = """
    # 디시인사이드를 중심으로 커뮤니티들을 크롤링합니다
    # """,
    long_description = open('README.md', encoding = "UTF8").read(),
    author = "Carl Jellinek",
    author_email = "car1jellinek@gmail.com",
    url = "https://github.com/FreelyReceivedFreelyGive/DCinsideRead",
    project_urls = {
        "Documentation": "https://freelyreceivedfreelygive.gitbook.io/dcinsideread/",
        "Source Code": "https://github.com/FreelyReceivedFreelyGive/DCinsideRead",
        "Bug Tracker": "https://github.com/FreelyReceivedFreelyGive/DCinsideRead/issues"
    },
    python_requires=">=3.6",
    license='GPLv3+',
    
    packages = setuptools.find_packages(),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3.7"
    ],
    keywords = ["디씨인사이드", "디시인사이드", "디시인사이드 갤러리", "디씨인사이드 갤러리",
    "DCinside", "dcinside", "DC", "dc", "gallery", "김유식", "유식", "횡령", "갤", "갤질", "개죽이"]
)