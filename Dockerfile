# Generate Docker image file.

FROM amazonlinux:2 as builder
RUN \
    yum -y update --security && \
    yum -y install openssl && \
    yum clean all

RUN mkdir /ssl
COPY src/ssl/openssl.cnf /ssl/
# Create a cert.
RUN openssl req -x509 -config /ssl/openssl.cnf -newkey rsa:4096 -keyout /ssl/key.pem -out /ssl/cert.pem -days 99999 -nodes

# Run it on latest Amazon Linux 2.
FROM amazonlinux:2
LABEL maintainer="sarah_luo@harvard.edu"


# Python version to install
ENV pythonmajor 3

# Do a bunch of installs, all combined into a single RUN command because it
# dramatically reduces the size of the image file (in this case from 427MB
# down to 128MB).
# 	- run OS security updates.
# 	- add the EPEL yum repo
#		- install python
RUN \
	curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo; \
	yum -y remove unixODBC-utf16 unixODBC-utf16-devel; \
	ACCEPT_EULA=Y yum -y install msodbcsql17; \	
	yum -y update --security; \
	rpm -Uvh http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm; \
	yum -y install python${pythonmajor}; \
	yum -y install python${pythonmajor}-pip; \
	yum -y install shadow-utils; \
	yum clean all; \
	yum -y install gcc-c++ python${pythonmajor}-devel unixODBC-devel; \
	yum clean all

RUN useradd -ms /bin/bash user
RUN mkdir /app
RUN chown -R user /app
USER user

ENV PATH /home/user/.local/bin:${PATH}

# Install the Python modules our API application uses.
COPY src/requirements.txt /tmp/requirements.txt
RUN pip3 install --user -r /tmp/requirements.txt

COPY --from=builder /ssl /ssl

# Install Python application.
COPY --chown=user src /app/src/
COPY --chown=user gunicorn.sh /app/
RUN chmod u+x /app/gunicorn.sh

# Start gunicorn via a shell script in our src folder.
WORKDIR /app
ENTRYPOINT /bin/sh -c ./gunicorn.sh