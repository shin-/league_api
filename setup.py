#!/usr/bin/env python
import os
from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

test_requirements = []
with open('./requirements.txt') as requirements_txt:
    requirements = [line for line in requirements_txt]

setup(
    name="league_api",
    version='0.0.1',
    description="Python client for League of Legends API.",
    packages=['api'],
    install_requires=requirements + test_requirements,
    zip_safe=False
)
