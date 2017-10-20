FROM daocloud.io/python:2-onbuild
MAINTAINER lpj24 "lipenju24@163.com"

WORKDIR /show_log
ADD . /show_log
RUN pip install -r requirements.txt
EXPOSE 5500