from setuptools import setup
import datetime

v = "1"
ver = "1.0.0"
dt = datetime.datetime.now()
yy = dt.strftime("%y")
mmdd = dt.strftime("%m%d")
HHMM = dt.strftime("%H%M")


setup(
    name="IutyLib",
    version= v + "." + yy + "." + mmdd + "." + HHMM,
    #version = ver,
    packages=[
        #"IutyLib",
        "IutyLib.commonutil",
        "IutyLib.database",
        "IutyLib.file",
        "IutyLib.stock",
        "IutyLib.tensor",
        "IutyLib.monitor",
        ]
)