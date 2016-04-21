Usage of oslo.messaging
============================================================
http://docs.openstack.org/developer/oslo.messaging/index.html


## 问题
1. 创建amqp服务器
2. 创建amqp客户端
3. 客户端向服务器发送消息, 服务器回复消息
4. 3种rabbitmq消息的体现: direct, topic, fanout


## 示例
### 1. install rabbitmq
    refer to rabbitmq/installation_centos7.sh

### 2. 相关命令语句
    # rabbitmqctl list_vhosts
    # rabbitmqctl list_exchanges
    # rabbitmqctl list_queues
    # rabbitmqctl list_bindings
### 3. 使用oslo.messaging的api重写rabbitmq 中的例子

Concept
==================================================================

### Transport:
    This method will construct a Transport object from transport configuration gleaned from the user’s configuration and, optionally, a transport URL.

    oslo_messaging.get_transport(conf, url=None, allowed_remote_exmods=None, aliases=None)
    oslo_messaging.get_notification_transport(conf, url=None, allowed_remote_exmods=None, aliases=None)
        for notification transport, please refer below chapter Notifier
    url like:
        rabbit://username:password@host:5672/virtual_host
        transport://user:pass@host1:port[,hostN:portN]/virtual_host
    if it's a conf file, what rows should be inserted into conf file???
        rpc_backend = rabbit
        bind_host = 0.0.0.0

### Target
    information like topic, server, namespace and etc ...
    Identifies the destination of messages.

### Endpoint

### Excutore
    Executors are providing the way an incoming message will be dispatched so that the message can be used for meaningful work.
    Different types of executors are supported, each with its own set of restrictions and capabilities.
    blocking / eventlet / threading

### RPC Server
    An RPC server exposes a number of endpoints, each of which contain a set of methods which may be invoked remotely by clients over a given transport.
    To create an RPC server, you supply a transport, target and a list of endpoints.
    RPC servers have start(), stop() and wait() messages to begin handling requests, stop handling requests and wait for all in-process requests to complete.
    server = messaging.get_rpc_server(transport, target, endpoints, executor)
    server.start()
    server.wait()

### RPC Client
    client = messaging.RPCClient(transport, target)
    client.call(...)
    client.cast(...)

### Notifier
    Send notification messages.   
    The Notifier class is used for sending notification messages over a messaging transport or other means.   
    在什么时候发送这些消息呢? 发送这些消息给谁呢? 有什么意义呢?
    Notification messages follow the following format:   
        {'message_id': six.text_type(uuid.uuid4()),
         'publisher_id': 'compute.host1',
         'timestamp': timeutils.utcnow(),
         'priority': 'WARN',
         'event_type': 'compute.create_instance',
         'payload': {'instance_id': 12, ... }}
    A Notifier object can be instantiated with a transport object and a publisher ID:
        notifier = messaging.Notifier(get_notification_transport(CONF), ‘compute’)
    notification通过[oslo_messaging_notifications] section in /etc/neutron/neutron.conf里的配置项来选择driver
    具体的项可以参考文档
    http://docs.openstack.org/developer/oslo.messaging/opts.html
	driver值, 这个值可以是 messaging, messagingv2, routing, log, test, noop (multi valued)
	
    please check the 
    ...
    notifier = messaging.Notifier(transport, topic)
    notifier.error(...)

### Available Notifier Drivers
#### log
Publish notifications via Python logging infrastructure.
#### messaging
Send notifications using the 1.0 message format.
This driver sends notifications over the configured messaging transport, but without any message envelope (also known as message format 1.0).
This driver should only be used in cases where there are existing consumers deployed which do not support the 2.0 message format.
#### messagingv2
Send notifications using the 2.0 message format.
#### noop
#### routing
#### test
Store notifications in memory for test verification.

### Notification Driver
    This driver should only be used in cases where there are existing consumers deployed which do not support the 2.0 message format.
    force to use format 1.0

### Notification Listerner
    A notification listener exposes a number of endpoints, each of which contain a set of methods. Each method corresponds to a notification priority.
    每个endpoint里面要实现一些方法, 比如error, warn之类的
    ex03_notifier中包含了示例程序
    listener = messaging.get_notification_listener(transport, targets, endpoints)
    # take attention to targets, not target
    # endpoint will implements method like error, warn ...
    listener.start()
    listener.wait()
A notifier sends a notification on a topic with a priority,   
the notification listener will receive this notification if the topic of this one have been set in one of the targets   
and if an endpoint implements the method named like the priority   
and if the notification match the NotificationFilter rule set into the filter_rule attribute of the endpoint.  
notifer发送notification, notification listener接收并使用endpoints处理  


### Serializer



Sample Design
==================================================
# design the following samples
## 1. set up server, create client, client send message
## 2. set up server1, create client2 and related server2, client2 send message to server, server process and send back to server2, server2 process it
## 3. publish / subscribe

## ex01_hello_world
    copy from ThinkingMiddleware/rabbitmq, it's implemented using RabbitMQ
## ex01_hello_world_oslo
    re-implement it using oslo.messaging

## ex02_rpc_server
python server.py
    why generate 3 consumers???
    [root@jun python]# rabbitmqctl list_consumers | grep test
    test   <rabbit@jun.2.1231.0>  1       true    0      []
    test.server1   <rabbit@jun.2.1231.0>  2       true    0      []
    test_fanout_1064b7923baf4d4b9e4e56329f079c12    <rabbit@jun.2.1231.0>   3      true    0       []
python client.py


http://blog.csdn.net/juvxiao/article/details/23532617

基本概念
===================================================
    Server: 为各个Client提供RPC接口,它是消息的最终处理者;

    Client: RPC接口的调用端, 我们常见的cast和call方法就是在这端调用;

    Exchange: 理解为一个消息交换机， 把消息分类，告诉何种路由到何种queue;

    Topic: 是一个RPC消息的唯一标识; servers监听这个topic的消息; client负责发出这个topic的消息;

    Namespace: servers可以在一个topic上，提供多种方法集合， 这些方法集合通过namespace来分开管理;

    Method: 这个慨念很简单， 就是函数, 即远程方法调用中的方法;

    API version: 也就是server上提供的RPC api接口集合的版本号，openstack中1.0起步, servers可以一次提供多种api version，client每次请求时只需描述它所需要的最低version就ok;

    Transport: 可以理解为传输载体，这个很好理解, 就是我们使用的消息队列中间件RabbitMQ, Qpid, ZeroMQ等等, 是负责整个消息处理的系统，
    它负责消息传输直到提供给clients返回，
    使用此系统者， 不用了解细节,
    Openstack中实现的主要有这三种， AMQP标准下的rabbitMQ和Qpid， 和非AMQP的ZeroMQ，
    ZeroMQ更底层， 速度更快, 据说快10倍。

    Target这是个很重要的概念， 它描述了信息的处理方式， 该发哪里去(server属性)和消息处理端(server)监听什么信息(topic 属性)。
    以下是Target的属性
    exchange (defaults to CONF.control_exchange)
    topic
    server (optional) 它会使server的标示, 如host or host@backend 等等
    fanout (defaults to False) 这种模式类似于广播， 符合条件的server都要监听并做处理
    namespace (optional)
    API version (optional)

Use Cases [OpenStack中使用场景]
===================================================
### 1.存在多个接口版本的server, 随机选择一个处理远程调用的方法
### 2.存在多个接口版本的server, 特定server处理远程调用的方法
### 3.存在多个接口版本的server, 每个server都要处理远程调用的方法, 即所谓的fanout



http://www.openstack.cn/?p=3514


