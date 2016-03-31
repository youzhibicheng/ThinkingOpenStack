#!/usr/bin/env python
# encoding:utf8
import pika

# 建立到达RabbitMQ Server的connection
# 此处RabbitMQ Server位于本机-localhost
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.31.113'))
channel = connection.channel()

# 声明queue，确认要从中接收message的queue
# queue_declare函数是幂等的，可运行多次，但只会创建一次
# 若可以确信queue是已存在的，则此处可省略该声明，如producer已经生成了该queue
# 但在producer和consumer中重复声明queue是一个好的习惯
# 但是实际的情况确实，我在3.6.1的版本中, 这里如果再declare的话, 会报错
channel.queue_declare(queue='hello')

print ' [*] Waiting for messages. To exit press CTRL+C'

# 定义回调函数
# 一旦从queue中接收到一个message回调函数将被调用
# ch：channel
# method：
# properties：
# body：message
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

# 从queue接收message的参数设置
# 包括从哪个queue接收message，用于处理message的callback，是否要确认message
# 默认情况下是要对消息进行确认的，以防止消息丢失。
# 此处将no_ack明确指明为True，不对消息进行确认。
channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

# 始循环从queue中接收message并使用callback进行处理
channel.start_consuming()
