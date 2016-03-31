========================
Usage of oslo.messaging
http://docs.openstack.org/developer/oslo.messaging/index.html
========================
问题
1. 创建amqp服务器
2. 创建amqp客户端
3. 客户端向服务器发送消息, 服务器回复消息
4. 3种rabbitmq消息的体现: direct, topic, fanout

示例
1. install rabbitmq
    refer to ThinkingMiddleware/rabbitmq/installation_centos7.sh

2. 相关命令语句
    # rabbitmqctl list_vhosts
    # rabbitmqctl list_exchanges
    # rabbitmqctl list_queues
    # rabbitmqctl list_bindings
3. 使用oslo.messaging的api重写 ThinkingMiddleware/rabbitmq 中的例子

Concept
Transport:
    oslo_messaging.get_transport(conf, url=None, allowed_remote_exmods=None, aliases=None)
    url like:
        rabbit://me:passwd@host:5672/virtual_host
        transport://user:pass@host1:port[,hostN:portN]/virtual_host
Target
    information like topic, server, namespace and etc ...
    Identifies the destination of messages.
Endpoint
Excutore
    blocking / eventlet / threading
RPC Server / RPC Client
    server = messaging.get_rpc_server(transport, target, endpoints, executor)
    server.start()
    server.wait()
    ...
    client = messaging.RPCClient(transport, target)
    client.call(...)
    client.cast(...)
Notification Listener / Notifier
    listener = messaging.get_notification_listener(transport, targets, endpoints)
    # take attention to targets, not target
    # endpoint will implements method like error, warn ...
    listener.start()
    listener.wait()
    ...
    notifier = messaging.Notifier(transport, topic)
    notifier.error(...)
Notification Listerner
    A notification listener exposes a number of endpoints, each of which contain a set of methods. Each method corresponds to a notification priority.
Notification Driver
    This driver should only be used in cases where there are existing consumers deployed which do not support the 2.0 message format.
    force to use format 1.0
Serializer

Sample Design
design the following samples
1. set up server, create client, client send message
2. set up server1, create client2 and related server2, client2 send message to server, server process and send back to server2, server2 process it
3. publish / subscribe

sample 01:
ex01_hello_world
    copy from ThinkingMiddleware/rabbitmq, it's implemented using RabbitMQ
ex01_hello_world_oslo
    re-implement it using oslo.messaging


