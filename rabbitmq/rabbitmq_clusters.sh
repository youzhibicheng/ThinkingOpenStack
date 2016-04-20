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

# 2.读取其中一个节点的cookie，并复制到其他节点（节点间通过cookie确定相互是否可通信）
# 两者之一均可：
# sudo vim /var/lib/rabbitmq/.erlang.cookie
# sudo vim $HOME/.erlang.cookie
# 在每台机器上的/etc/hosts中添加
# vim /etc/hosts
# 192.168.56.101 server
# 192.168.56.102 cluster1
# 192.168.56.103 cluster2

# 3.逐个启动节点
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
sudo rabbitmq-plugins enable rabbitmq_management

# 4.查看各节点中的RabbitMQ brokers
sudo rabbitmqctl cluster_status

# 5.建集群
# 分别在cluster1、cluster2 上执行
sudo rabbitmqctl stop_app
sudo rabbitmqctl join_cluster --ram rabbit@server
sudo rabbitmqctl start_app
sudo rabbitmqctl stop_app
sudo rabbitmqctl join_cluster rabbit@server
sudo rabbitmqctl start_app

#####################################################
RabbitMQ cluster 管理
#####################################################
# 1.查看集群状态
# 可分别在集群中各个节点执行
sudo rabbitmqctl cluster_status

# 2.更改节点类型（内存型或磁盘型）
sudo rabbitmqctl stop_app
sudo rabbitmqctl change_cluster_node_type disc
sudo rabbitmqctl change_cluster_node_type ram
sudo rabbitmqctl start_app

# 3.重启cluster中的节点
# 停止某个节点或者节点down掉剩余节点不受影响
# cluster1
sudo rabbitmqctl stop
# server
sudo rabbitmqctl cluster_status
# cluster2
sudo rabbitmqctl cluster_status
sudo rabbitmqctl stop
# server
sudo rabbitmqctl cluster_status
