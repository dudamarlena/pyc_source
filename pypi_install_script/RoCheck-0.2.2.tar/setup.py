from setuptools import setup

setup(
    name='RoCheck',
    version='0.2.2',
    packages=['RoCheck'],
    install_requires=[    # 依赖列表
        'requests'
    ],
    author_email = 'kwok6140@outlook.com',
    author = "Kwok6140",
    license='MIT',
    long_description='''
# RoCheck

# RoCheck

This is a modules originally ported from grilme99's RoCheck which is written in node.js

But now it's become something different from his version

[Link to his github](https://github.com/grilme99/RoCheck)

# How to install

pip install RoCheck

# Get started

```Python
import RoCheck

Checks = RoCheck.auth("your bot cookie")

print(Checks.get_ip('place_id', 'job_id'))

print(Checks.verify_ip('4038727744',str(Checks.get_ip('place_id', 'job_id'))))

print(Checks.get_job('4038727744',str(Checks.get_ip('place_id', 'job_id'))))
```

> Output: 128.116.6.27 (Different depend on the server the game is running on)

> Output: True (Return true if the ip was from roblox and that place.)

> Output: 00000000-0000-0000-0000-000000000000 (Different depend what you inputted)

# Support

> If you would like support with this module then message me on Discord (Kwok6140#2416)

> The project will soon be discontinue once I got bored on this project

> -Kwok6140


# Future update

We are probably gonna get more function than the original one.
Current planning:
> Verify if ip is from Roblox Server (Done)

> Verify Job Id is valid (Done)


(check grilme99 or jacob out he's cool

''',
    long_description_content_type='text/markdown'
)
