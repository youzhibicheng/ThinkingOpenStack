#!/usr/bin/env python
# encoding:utf8
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# 作为好的习惯，在producer和consumer中分别声明一次以保证所要使用的exchange存在
channel.exchange_declare(exchange='logs', type='fanout')

# 在不同的producer和consumer间共享queue时指明queue的name是重要的
# 但某些时候，比如日志系统，需要接收所有的log message而非一个子集
# 而且仅对当前的message 流感兴趣，对于过时的message不感兴趣，那么
# 可以申请一个临时队列这样，每次连接到RabbitMQ时会以一个随机的名字生成
# 一个新的空的queue，将exclusive置为True，这样在consumer从RabbitMQ断开后会删除该queue
result = channel.queue_declare(exclusive=True)

# 用于获取临时queue的name
queue_name = result.method.queue

# exchange与queue之间的关系成为binding
# binding告诉exchange将message发送该哪些queue
channel.queue_bind(exchange='logs',
                   queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] %r" % (body,)

# 从指定地queue中consume message且不确认
channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
