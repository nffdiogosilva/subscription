FROM python:3.7-stretch

LABEL maintainer="Nuno Diogo da Silva <diogosilva.nuno@gmail.com>"

COPY src /workspace/src/
COPY pytest.ini /workspace/

RUN pip install pytest pytest-cov

WORKDIR /workspace

CMD [ "pytest" ]
