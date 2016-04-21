#!/usr/bin/python27
# encoding:utf8
import pika

# 与RabbitMQ Server建立连接
# 连接到的broker在本机-localhost上
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# 声明队列以向其发送消息消息
# 向不存在的位置发送消息时RabbitMQ将消息丢弃
# queue='hello'指定队列名字
channel.queue_declare(queue='hello', durable=True)

# message不能直接发送给queue，需经exchange到达queue，此处使用以空字符串标识的默认的exchange
# 使用默认exchange时允许通过routing_key明确指定message将被发送给哪个queue
# body参数指定了要发送的message内容
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')

print " [x] Sent 'Hello World!'"

# 关闭与RabbitMq Server间的连接
connection.close()
