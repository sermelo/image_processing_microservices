# Not using alpine because cannot install opencv-python
FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip3 install opencv-python imutils requests

COPY ./app /app
RUN mkdir /var/images/
