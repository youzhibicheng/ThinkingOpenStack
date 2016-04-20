#!/usr/bin/env bash

# http://www.rabbitmq.com/clustering.html

# this create a rabbitmq sample cluster
# base on blog
# http://blog.csdn.net/zyz511919766/article/details/41896747

# prerequisite, have 3 vms
# server
#    192.168.56.101
# cluster1
#    192.168.56.102
# cluster2
#    192.168.56.103

# 1. install rabbitmq-server first
rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum -y install rabbitmq-server

# 2.��ȡ����һ���ڵ��cookie�������Ƶ������ڵ㣨�ڵ��ͨ��cookieȷ���໥�Ƿ��ͨ�ţ�
# ����֮һ���ɣ�
# sudo vim /var/lib/rabbitmq/.erlang.cookie
# sudo vim $HOME/.erlang.cookie
# ��ÿ̨�����ϵ�/etc/hosts�����
# vim /etc/hosts
# 192.168.56.101 server
# 192.168.56.102 cluster1
# 192.168.56.103 cluster2

# 3.��������ڵ�
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
sudo rabbitmq-plugins enable rabbitmq_management

# 4.�鿴���ڵ��е�RabbitMQ brokers
sudo rabbitmqctl cluster_status

# 5.����Ⱥ
# �ֱ���cluster1��cluster2 ��ִ��
sudo rabbitmqctl stop_app
sudo rabbitmqctl join_cluster --ram rabbit@server
sudo rabbitmqctl start_app
sudo rabbitmqctl stop_app
sudo rabbitmqctl join_cluster rabbit@server
sudo rabbitmqctl start_app

#####################################################
RabbitMQ cluster ����
#####################################################
# 1.�鿴��Ⱥ״̬
# �ɷֱ��ڼ�Ⱥ�и����ڵ�ִ��
sudo rabbitmqctl cluster_status

# 2.���Ľڵ����ͣ��ڴ��ͻ�����ͣ�
sudo rabbitmqctl stop_app
sudo rabbitmqctl change_cluster_node_type disc
sudo rabbitmqctl change_cluster_node_type ram
sudo rabbitmqctl start_app

# 3.����cluster�еĽڵ�
# ֹͣĳ���ڵ���߽ڵ�down��ʣ��ڵ㲻��Ӱ��
# cluster1
sudo rabbitmqctl stop
# server
sudo rabbitmqctl cluster_status
# cluster2
sudo rabbitmqctl cluster_status
sudo rabbitmqctl stop
# server
sudo rabbitmqctl cluster_status
