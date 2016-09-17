#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2016, Florian Brucker (www.florianbrucker.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import io
import os.path
import re
import sys

from setuptools import find_packages, setup

HERE = os.path.dirname(__file__)
SOURCE_FILE = os.path.join(HERE, 'ifttt_logging_handler', '__init__.py')
REQUIREMENTS_FILE = os.path.join(HERE, 'requirements.txt')

version = None
with io.open(SOURCE_FILE, encoding='utf8') as f:
    for line in f:
        s = line.strip()
        m = re.match(r"""__version__\s*=\s*['"](.*)['"]""", line)
        if m:
            version = m.groups()[0]
            break
if not version:
    raise RuntimeError('Could not extract version from "%s".' % SOURCE_FILE)

with io.open(REQUIREMENTS_FILE, encoding='utf8') as f:
    requirements = f.readlines()

long_description = """
IFTTT.com is a platform that allows you to setup automatic reactions to
a wide range of events. This module provides a logging handler that
forwards log messages to IFTTT so that you can automatically react to
them (for example to get an e-mail if that cron job on some remote
server you keep forgetting about logs an error).
""".strip()

setup(
    name='ifttt-logging-handler',
    description='Logging handler that forwards messages to IFTTT.com',
    long_description=long_description,
    url='https://github.com/torfsen/ifttt-logging-handler',
    version=version,
    license='MIT',
    keywords='log logging ifttt'.split(),
    classifiers=[
        # Reference: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    author='Florian Brucker',
    author_email='mail@florianbrucker.de',
    packages=find_packages(),
    install_requires=requirements,
)

