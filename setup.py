#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import os
import re
import uuid
from glob import glob
from os.path import basename, splitext

try:  # for pip >= 10
    # noinspection PyProtectedMember,PyPackageRequirements
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    # noinspection PyPackageRequirements
    from pip.req import parse_requirements

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def requirements(path):
    items = parse_requirements(path, session=uuid.uuid1())
    return [";".join((str(r.req), str(r.markers))) if r.markers else str(r.req) for r in items]


tests_require = requirements(os.path.join(os.path.dirname(__file__), "requirements-dev.txt"))
install_requires = requirements(os.path.join(os.path.dirname(__file__), "requirements-dev.txt"))


def get_version(*file_paths):
    """Retrieves the version from path"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    print("Looking for version in: {}".format(filename))
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("src", "subscription", "__init__.py")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='subscription',
    version=version,
    description="""Programming test task written in Python 3 using TDD""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nuno Diogo da Silva",
    author_email='diogosilva.nuno@gmail.com',
    packages=find_packages('src', exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    exclude_package_data={
        '': ['test*.py', 'tests/*.env', '**/tests.py'],
    },
    python_requires='>=3.7',
    install_requires=install_requires,
    license="MIT",
    zip_safe=False,
    keywords='subscription',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # test_suite='runtests.run_tests',
    # test_suite='nose.collector',
    tests_require=tests_require,
    # https://docs.pytest.org/en/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner
    setup_requires=['pytest-runner'],
    url='http://github.com/nffdiogosilva/subscription'
)
