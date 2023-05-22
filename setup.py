from setuptools import setup, find_packages

setup(
    name="myviews",
    version="0.1.0",
    author="Mohammad saadtai",
    python_requires=">=3.8",
    install_requires=[
        "jdatetime==4.1.0",
        "mysql-connector-python==8.0.31",
        "PyQt5==5.15.7",
        "pyserial==3.5",
        "playsound==1.2.2",
    ],
    packages=find_packages(),
)
