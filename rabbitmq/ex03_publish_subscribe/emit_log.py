#!/usr/bin/env python
# encoding:utf8

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# producer只能通过exchange将message发给queue
# exchange的类型决定将message路由至哪些queue
# 可用的exchange类型：direct\ex05_topic\headers\fanout
# 此处定义一个名称为'logs'的'fanout'类型的exchange，'fanout'类型的exchange简单的将message广播到它所知道的所有queue
channel.exchange_declare(exchange='logs', type='fanout')

# 请注意, 这里 producer并没有创建queue
# channel.queue_declare(queue='task_queue', durable=True)
# 那么, 当publish的时候, 应该只是publish到了exchange, 并没有publish到queue中, 需要consumer关联exchange和queue之后, 消息才能流入到queue中？？？

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

# 将message publish到名为log的exchange中
# 因为是fanout类型的exchange，这里无需指定routing_key
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

print " [x] Sent %r" % (message,)

connection.close()
