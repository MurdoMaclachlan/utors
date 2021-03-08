from setuptools import setup, find_packages
from utorsmodules.main import version

def readme():
    return open('README.md', 'r').read()

setup(
    name="utors",
    version=version,
    scripts=["utors"],
    author="Murdo Maclachlan",
    author_email="murdo@maclachlans.org.uk",
    description="A utility to gather and analyse certain statistics from the Transcribers of Reddit.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/MurdoMaclachlan/utors",
    packages=find_packages(),
    install_requires=[
        "praw>=7.1.2",
        "alive_progress>=1.6.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
    ],
    license='MIT'
)
