# Subscription System

A simple subscription system, wrote entirely with Python 3, with no framework support whatsoever.

## To run project (with docker):

#### Dependencies needeed: docker

    $ git clone <repo_url>
    $ cd <project_dir>
    $ docker image build -t subscription-test .
    
    # By default, this docker container run command will run the tests via pytest
    $ docker container run --rm -it subscription-test

## To run project (with local computer):

#### Dependencies needeed: python 3 and pipenv.

    $ git clone <repo_url>
    $ cd <project_dir>
    $ pipenv install
    $ pipenv shell

    # To make the tests run
    $ pytest

After running the pytest, the htmlcov (with the code coverage), will appear.
In this case, this folder is already included in the repository, with the latest results.
Please consult the file htmlcov/index.html to see the code coverage detailed.

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
