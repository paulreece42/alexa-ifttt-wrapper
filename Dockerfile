FROM centos

MAINTAINER Paul Reece https://github.com/paulreece42

RUN yum -y install python-setuptools python python-devel
RUN easy_install flask
RUN easy_install requests

RUN mkdir /opt/apiwrapper
ADD remoteapc.py /opt/apiwrapper/remoteapc.py
ADD saltAPI.py /opt/apiwrapper/saltAPI.py
RUN chmod 755 /opt/apiwrapper/remoteapc.py

EXPOSE 5000

ENTRYPOINT /opt/apiwrapper/remoteapc.py
