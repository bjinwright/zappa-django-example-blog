FROM python:3.6
RUN mkdir code
WORKDIR code
ADD . /code/bjinwright
ADD ./requirements.txt /code/requirements.txt
RUN pip install virtualenv
RUN virtualenv ve && /code/ve/bin/pip install -U pip
RUN /code/ve/bin/pip install -r /code/requirements.txt
WORKDIR /code/bjinwright