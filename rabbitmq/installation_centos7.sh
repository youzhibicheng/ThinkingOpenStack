#!/bin/bash

# installing erlang
# installing epel
# http://fedoraproject.org/wiki/EPEL
#rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
#yum -y install erlang

# install rabbitmq server
#rpm --import https://www.rabbitmq.com/rabbitmq-signing-key-public.asc
#yum -y install rabbitmq-server-3.5.6-1.noarch.rpm

# or just use this command, but first you need to install epel
rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum -y install rabbitmq-server

# stop firewalld first
systemctl stop firewalld
systemctl disable firewalld

# or set firewalld like this
#firewall-cmd --permanent --add-port=5672/tcp
#firewall-cmd --reload
#setsebool -P nis_enabled 1

# need to configure /etc/hosts correctly
# or when start it will throw error like this
# Failed to start RabbitMQ broker.
#host_nic=enp0s10
#host_ip=$(ifconfig $host_nic | grep 'inet '| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $2}')
#host_name=$(hostname)
#echo "$host_ip $host_name" >> /etc/hosts

# Run RabbitMQ Server
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service

# change password, change to 'guest'
rabbitmqctl change_password guest RABBIT_PASS

# install python and related pip packages
yum -y install python python-devel python-pip gcc
pip install pika
pip install kombu
pip install paste pastedeploy webob eventlet
