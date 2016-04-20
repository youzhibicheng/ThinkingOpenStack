#!/usr/bin/env python
# encoding:utf8
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.31.113'))
channel = connection.channel()

# 声明一个名为topic_logs的topic类型的exchange
# topic类型的exchange可通过通配符对message进行匹配从而路由至不同queue
channel.exchange_declare(exchange='topic_logs',
                         type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 1 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

channel.basic_publish(exchange='topic_logs',
                      routing_key=routing_key,
                      body=message)

print " [x] Sent %r:%r" % (routing_key, message)
connection.close()
