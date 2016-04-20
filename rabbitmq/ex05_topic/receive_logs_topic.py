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

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# 从命令行获取参数:routing_key
severities = sys.argv[1:]
if not severities:
    print >> sys.stderr, "Usage: %s [info] [warning] [error]" % (sys.argv[0],)
    sys.exit(1)

# exchange和queue之间的binding可接受routing_key参数
# 该参数的意义依赖于exchange的类型
# fanout类型的exchange直接忽略该参数
# direct类型的exchange精确匹配该关键字进行message路由
# 对多个queue使用相同的binding_key是合法的
for severity in severities:
    channel.queue_bind(exchange='topic_logs',
                       queue=queue_name,
                       routing_key=severity)

print ' [*] Waiting for logs. To exit press CTRL+C'


def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
