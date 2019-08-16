# Subscription System

A simple subscription system, wrote entirely with Python 3, with no framework support whatsoever.

## To run project (with local computer):
    $ cd <project_dir>
    $ pipenv install
    $ pipenv shell
    $ pytest # to make the tests run

#### Dependencies needeed: You need python 3 and pipenv.

After running the pytest, the htmlcov (with the code coverage), will appear.
In this case, this folder is already included in the repository, with the latest results.

## To run project (with docker):
    $ cd <project_dir>
    $ docker image build -t subscription-test .
    $ docker container run --rm -it subscription-test
    $ pytest # to make the tests run

### Dependencies needeed: docker
