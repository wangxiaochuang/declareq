# Standard library imports
import os
from setuptools import setup, find_packages


def read(filename):
    with open(filename) as stream:
        return stream.read()


# Read package metadata from __about__.py, to avoid importing the whole
# package prior to installation.
about = dict()
with open(os.path.join("declareq", "__about__.py")) as fp:
    exec(fp.read(), about)
    about = dict((k.strip("_"), about[k]) for k in about)

install_requires = ["requests>=2.18.0",
                    "uritemplate>=3.0.0", "retrying>=1.3.4"]

extras_require = {
    "typing": ["typing>=3.6.4"],
}

metadata = {
    "author": "wangxiaochuang",
    "author_email": "jackstrawxiaoxin@gmail.com",
    "url": "https://github.com/wangxiaochuang/declareq",
    "project_urls": {
        "Source": "https://github.com/wangxiaochuang/declareq",
    },
    "license": "MIT",
    "description": "A Declarative HTTP Client for Python.",
    "long_description": read("README.md"),
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    "keywords": "http api rest client retrofit",
    "packages": find_packages(exclude=("tests", "tests.*", "test.py")),
    "install_requires": install_requires,
    "extras_require": extras_require,
}
metadata = dict(metadata, **about)

if __name__ == "__main__":
    setup(name="declareq", **metadata)
