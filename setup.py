#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import app

from os import path as p

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


def read(filename, parent=None):
    parent = (parent or __file__)

    try:
        with open(p.join(p.dirname(parent), filename)) as f:
            return f.read()
    except IOError:
        return ''


def parse_requirements(filename, parent=None, dep=False):
    parent = (parent or __file__)
    filepath = p.join(p.dirname(parent), filename)
    content = read(filename, parent)

    for line_number, line in enumerate(content.splitlines(), 1):
        candidate = line.strip()

        if candidate.startswith('-r'):
            args = [candidate[2:].strip(), filepath, dep]

            for item in parse_requirements(*args):
                yield item
        elif not dep and '#egg=' in candidate:
            yield re.sub('.*#egg=(.*)-(.*)', r'\1==\2', candidate)
        elif dep and '#egg=' in candidate:
            yield candidate.replace('-e ', '')
        elif not dep:
            yield candidate

# [metadata]
# classifier = Development Status :: 1 - Planning
# classifier = Development Status :: 2 - Pre-Alpha
# classifier = Development Status :: 3 - Alpha
# classifier = Development Status :: 4 - Beta
# classifier = Development Status :: 5 - Production/Stable
# classifier = Development Status :: 6 - Mature
# classifier = Development Status :: 7 - Inactive
# classifier = Environment :: Console
# classifier = Environment :: Web Environment
# classifier = Intended Audience :: End Users/Desktop
# classifier = Intended Audience :: Developers
# classifier = Intended Audience :: System Administrators
# classifier = Operating System :: MacOS :: MacOS X
# classifier = Operating System :: Microsoft :: Windows
# classifier = Operating System :: POSIX

# Avoid byte-compiling the shipped template
sys.dont_write_bytecode = True

requirements = parse_requirements('requirements.txt')
dependencies = list(parse_requirements('requirements.txt', dep=True))
readme = read('README.rst')
changes = read('CHANGES.rst').replace('.. :changelog:', '')
license = app.__license__
version = app.__version__
title = app.__title__
url = 'https://github.com/reubano/%s' % title

classifier = {
    'GPL': 'GNU General Public License (GPL)',
    'MIT': 'MIT License',
    'BSD': 'BSD License'
}

setup(
    name=title,
    version=version,
    description=app.__description__,
    long_description=readme + '\n\n' + changes,
    author=app.__author__,
    author_email=app.__email__,
    url=url,
    download_url='%s/archive/v%s/%s*.tar.gz' % (url, version, title),
    packages=find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
    dependency_links=dependencies,
    tests_require=['nose'],
    test_suite='tests',
    license=license,
    zip_safe=False,
    keywords=app.__title__,
    package_data={},
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: %s' % classifier[license],
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Environment :: Web',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
    platforms=['MacOS X', 'Windows', 'Linux'],
)
