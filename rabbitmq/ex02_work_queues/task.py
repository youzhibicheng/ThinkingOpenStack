#!/usr/bin/env python
# encoding:utf8
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# 仅仅对message进行确认不能保证message不丢失，比如RabbitMQ崩溃了queue就会丢失
# 因此还需使用durable=True声明queue是持久化的，这样即便Rabbit崩溃了重启后queue仍然存在
channel.queue_declare(queue='task_queue', durable=True)

# 命令行构造将要发送的message
message = ' '.join(sys.argv[1:]) or "Hello World!"

# 除了要声明queue是持久化的外，还需声明message是持久化的
# basic_publish的properties参数指定message的属性
# 此处pika.BasicProperties中的delivery_mode=2指明message为持久的
# 这样一来RabbitMQ崩溃重启后queue仍然存在其中的message也仍然存在
# 需注意的是将message标记为持久的并不能完全保证message不丢失，因为
# 从RabbitMQ接收到message到将其存储到disk仍需一段时间，若此时RabbitMQ崩溃则message会丢失
# 况且RabbitMQ不会对每条message做fsync动作
# 可通过publisher confirms实现更强壮的持久性保证
# delivery_mode=2, # make message persistent
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode=2,
                      ))
print " [x] Sent %r" % (message,)
connection.close()
