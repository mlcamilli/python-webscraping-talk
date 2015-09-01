FROM mlcamilli/headless-browser:latest
ADD requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt
WORKDIR /code/
