#!/usr/bin/env python
# encoding:utf8
import pika
import time

# 默认情况RabbitMQ将message以round-robin方式发送给下一个consumer
# 每个consumer接收到的平均message量是一样的
# 可以同时运行两个或三个该程序进行测试
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

# 仅仅对message进行确认不能保证message不丢失，比如RabbitMQ崩溃了
# 还需使用durable=True声明queue是持久化的，这样即便Rabb崩溃了重启后queue仍然存在其中的message不会丢失
# RabbitMQ中不允许使用不同的参数定义同名queue
channel.queue_declare(queue='task_queue', durable=True)

print ' [*] Waiting for messages. To exit press CTRL+C'


# 回调函数，函数体模拟耗时的任务处理：以message中'.'的数量表示sleep的秒数
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep(body.count('.'))
    print " [x] Done"
    # 对message进行确认
    ch.basic_ack(delivery_tag = method.delivery_tag)

# 若存在多个consumer每个consumer的负载可能不同，有些处理的快有些处理的慢
# RabbitMQ并不管这些，只是简单的以round-robin的方式分配message
# 这可能造成某些consumer积压很多任务处理不完而一些consumer长期处于饥饿状态
# 可以使用prefetch_count=1的basic_qos方法可告知RabbitMQ只有在consumer处理并确认了上一个message后才分配新的message给他
# 否则分给另一个空闲的consumer
channel.basic_qos(prefetch_count=1)

# 这里移除了no_ack=True这个参数，也即需要对message进行确认（默认行为）
# 否则consumer在偶然down后其正在处理和分配到该consumer还未处理的message可能发生丢失
# 因为此时RabbitMQ在发送完message后立即从内存删除该message
# 假如没有设置no_ack=True则consumer在偶然down掉后其正在处理和分配至该consumer但还未来得及处理的message会重新分配到其他consumer
# 没有设置no_ack=True则consumer在收到message后会向RabbitMQ反馈已收到并处理了message告诉RabbitMQ可以删除该message
# RabbitMQ中没有超时的概念，只有在consumer down掉后重新分发message
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()