FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip3 install requests numpy opencv-python scipy pillow

COPY ./app /app
RUN mkdir /var/images/
