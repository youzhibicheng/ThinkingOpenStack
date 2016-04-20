#!/usr/bin/env bash

# rabbitmqctl
rabbitmqctl list_queues
rabbitmqctl list_exchanges
rabbitmqctl list_bindings

# rabbitmq-management plugin
# 基于HTTP的RabbitMQ server管理和监控工具
# 包含基于浏览器的用户界面和命令行工具rabbitmqadmin.
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
# 访问
# http://server-name:15672/
# http://server-name:15672/api #HTTP API
# http://server-name:15672/cli #rabbitmqadmin
# 可以使用默认用户名 guest / guest 登录
# 提示
# 默认guest账户只能从localhost登录，需先添加用户用赋予相应权限 (验证错误, 可以使用guest远程登录)
# 可通过配置rabbitmq.config改变rabbitmq-management plugin默认行为

# 新增用户
rabbitmqctl  add_user  james  passw0rd
# 删除用户
rabbitmqctl  delete_user  james
# 修改密码
rabbitmqctl  change_password  james  passw0rd
# 查看用户列表
# guest用户的缺省密码是guest
rabbitmqctl  list_users

wget http://server-name:15672/cli/rabbitmqadmin
chmod a+x rabbitmqadmin
./rabbitmqadmin --help

# 用户角色
# 分为五类
# (None)、management、policymaker、monitoring、administrator
# 设置用户角色
# rabbitmqctl set_user_tags User Tag
rabbitmqctl set_user_tags james administrator
# 一次设置多个角色
rabbitmqctl set_user_tags james administrator monitoring
# 参考：
# http://www.rabbitmq.com/management.html


# 用户权限
# 指用户对exchange，queue的操作权限，包括配置权限，读写权限。
# 配置权限会影响到exchange，queue的声明和删除。
# 读写权限影响到从queue里取消息，向exchange发送消息以及queue和exchange的绑定(bind)操作。
# 设置用户权限
rabbitmqctl set_permissions -p VHostPath User ConfP WriteP ReadP
# 查看(指定hostpath)所有用户的权限信息
rabbitmqctl  list_permissions  [-p  VHostPath]
# 查看指定用户的权限信息
rabbitmqctl  list_user_permissions  User
# 清除用户的权限信息
rabbitmqctl  clear_permissions  [-p VHostPath]  User
# 参考
# http://www.rabbitmq.com/access-control.html


