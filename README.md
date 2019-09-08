# Subscription System

[![Build Status](https://travis-ci.org/nffdiogosilva/subscription.svg?branch=master)](https://travis-ci.org/nffdiogosilva/subscription) [![Coverage Status](https://coveralls.io/repos/github/nffdiogosilva/subscription/badge.svg)](https://coveralls.io/github/nffdiogosilva/subscription) [![Updates](https://pyup.io/repos/github/nffdiogosilva/subscription/shield.svg)](https://pyup.io/repos/github/nffdiogosilva/subscription/) [![Python 3](https://pyup.io/repos/github/nffdiogosilva/subscription/python-3-shield.svg)](https://pyup.io/repos/github/nffdiogosilva/subscription/)[![PyPI version fury.io](https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&type=6&v=0.1.4&x2=0)](https://test.pypi.org/project/subscription/0.1.4/) [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


A simple subscription system, wrote entirely with Python 3, with no framework support whatsoever.

## To run project (with docker):

#### Dependencies needed: docker

    $ git clone <repo_url>
    $ cd <project_dir>
    $ docker image build -t subscription-test .
    
    # By default, this docker container run command will run the tests via pytest
    $ docker container run --rm -it subscription-test

## To run project (with local computer):

#### Dependencies needed: python 3 and pipenv.

    $ git clone <repo_url>
    $ cd <project_dir>
    $ pipenv install
    $ pipenv shell

    # To make the tests run
    $ pytest

## Summary

After running the pytest, the code coverage will be generated inside folder "htmlcov". To check results, consult the htmlconv/index.html page.
In this case, this folder is already included in the repository, with the latest results.
Please consult the file htmlcov/index.html to see the code coverage detailed.

## You can use the Visual Studio Code Remote Containers feature!

To run the project inside a container, with Visual Studio Code, just choose the option "Re-Open folder inside container". After that you can launch the tests in the DEBUG tab.

# MIT License

Copyright (c) [2019] [Nuno Diogo da Silva diogosilva.nuno@gmail.com]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
