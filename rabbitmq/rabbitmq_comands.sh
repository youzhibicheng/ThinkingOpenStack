#!/usr/bin/env bash

# rabbitmqctl
rabbitmqctl list_queues
rabbitmqctl list_exchanges
rabbitmqctl list_bindings

# rabbitmq-management plugin
# ����HTTP��RabbitMQ server����ͼ�ع���
# ����������������û�����������й���rabbitmqadmin.
rabbitmq-plugins enable rabbitmq_management
#The following plugins have been enabled:
#  mochiweb
#  webmachine
#  rabbitmq_web_dispatch
#  amqp_client
#  rabbitmq_management_agent
#  rabbitmq_management
#Plugin configuration has changed. Restart RabbitMQ for changes to take effect.
systemctl restart rabbitmq-server.service
# ����
# http://server-name:15672/
# http://server-name:15672/api #HTTP API
# http://server-name:15672/cli #rabbitmqadmin
# ����ʹ��Ĭ���û��� guest / guest ��¼
# ��ʾ
# Ĭ��guest�˻�ֻ�ܴ�localhost��¼����������û��ø�����ӦȨ�� (��֤����, ����ʹ��guestԶ�̵�¼)
# ��ͨ������rabbitmq.config�ı�rabbitmq-management pluginĬ����Ϊ

# �����û�
rabbitmqctl  add_user  james  passw0rd
# ɾ���û�
rabbitmqctl  delete_user  james
# �޸�����
rabbitmqctl  change_password  james  passw0rd
# �鿴�û��б�
# guest�û���ȱʡ������guest
rabbitmqctl  list_users

wget http://server-name:15672/cli/rabbitmqadmin
chmod a+x rabbitmqadmin
./rabbitmqadmin --help

# �û���ɫ
# ��Ϊ����
# (None)��management��policymaker��monitoring��administrator
# �����û���ɫ
# rabbitmqctl set_user_tags User Tag
rabbitmqctl set_user_tags james administrator
# һ�����ö����ɫ
rabbitmqctl set_user_tags james administrator monitoring
# �ο���
# http://www.rabbitmq.com/management.html


# �û�Ȩ��
# ָ�û���exchange��queue�Ĳ���Ȩ�ޣ���������Ȩ�ޣ���дȨ�ޡ�
# ����Ȩ�޻�Ӱ�쵽exchange��queue��������ɾ����
# ��дȨ��Ӱ�쵽��queue��ȡ��Ϣ����exchange������Ϣ�Լ�queue��exchange�İ�(bind)������
# �����û�Ȩ��
rabbitmqctl set_permissions -p VHostPath User ConfP WriteP ReadP
# �鿴(ָ��hostpath)�����û���Ȩ����Ϣ
rabbitmqctl  list_permissions  [-p  VHostPath]
# �鿴ָ���û���Ȩ����Ϣ
rabbitmqctl  list_user_permissions  User
# ����û���Ȩ����Ϣ
rabbitmqctl  clear_permissions  [-p VHostPath]  User
# �ο�
# http://www.rabbitmq.com/access-control.html


