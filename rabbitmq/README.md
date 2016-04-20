
** 安装**   
installation_centos7.sh   

**几个关键词**     
exchange   
queue   
routing_key   
type   
    fanout   
    direct   


# 场景1 - hello world  
python producer.py  
python consumer.py  


# 场景2 - work queues  
将耗时的消息处理通过队列分配给多个consumer来处理   
我们称此处的consumer为worker，queue称为Task Queue   
其目的是为了避免资源密集型的task的同步处理，也即立即处理task并等待完成。    
相反，调度task使其稍后被处理。也即把task封装进message并发送到task queue，   
worker进程在后台运行，从task queue取出task并执行job，若运行了多个worker，则task可在多个worker间分配。
task.py   
建立连接，声明队列，发送可以模拟耗时任务的message，断开连接、退出。   
worker.py   
建立连接，声明队列，不断的接收message，处理任务，进行确认。   
python task.py "A very hard task which takes two seconds.."   
python worker.py   


# 场景3 - Publish/Subscribe
在应用场景2中一个message(task)仅被传递给了一个comsumer(worker)。   
现在我们设法将一个message传递给多个consumer。这种模式被称为publish/subscribe   
此处以一个简单的日志系统为例进行说明。该系统包含一个log发送程序和一个log接收并打印的程序。由log发送者发送到queue的消息可以被所有运行的log接收者接收。   
因此，我们可以运行一个log接收者直接在屏幕上显示log，同时运行另一个log接收者将log写入磁盘文件。   
receive_logs.py   
日志消息接收者：建立连接，声明exchange，将exchange与queue进行绑定，开始不停的接收log并打印。   
emit_log.py   
日志消息发送者：建立连接，声明fanout类型的exchange，通过exchage向queue发送日志消息，消息被广播给所有接收者，关闭连接，退出。   
python receive_logs.py   
python emit_log.py "info: This is the log message"   


# 场景4 - Routing    
应用场景3中构建了简单的log系统，可以将log message广播至多个receiver。     
现在我们将考虑只把指定的message类型发送给其subscriber，   
比如，只把error message写到log file而将所有log message显示在控制台。   
receive_logs_direct.py   
log message接收者：建立连接，声明direct类型的exchange，声明queue，使用提供的参数作为routing_key将queue绑定到exchange，开始循环接收log message并打印。   
emit_log_direct.py   
log message发送者：建立连接，声明direct类型的exchange，生成并发送log message到exchange，关闭连接，退出。   
python receive_logs_direct.py info   
python emit_log_direct.py info "The message"   


# 场景5 - topic   
应用场景4中改进的log系统中用direct类型的exchange替换应用场景3中的fanout类型   
exchange实现将不同的log message发送给不同的subscriber   
（也即分别通过不同的routing_key将queue绑定到exchange，这样exchange便可将不同的message根据message内容路由至不同的queue）。   
但仍然存在限制，不能根据多个规则路由消息，比如接收者要么只能收error类型的log message要么只能收info类型的message。   
如果我们不仅想根据log的重要级别如info、warning、error等来进行log message路由    
还想同时根据log message的来源如auth、cron、kern来进行路由。   
为了达到此目的，需要topic类型的exchange。   
topic类型的exchange中routing_key中可以包含两个特殊字符：   
“*”用于替代一个词，     
“#”用于0个或多个词。   
receive_logs_topic.py   
log message接收者：建立连接，声明topic类型的exchange,声明queue，根据程序参数构造routing_key，根据routing_key将queue绑定到exchange，循环接收并处理message。   
emit_log_topic.py   
log message发送者：建立连接、声明topic类型的exchange、根据程序参数构建routing_key和要发送的message，以构建的routing_key将message发送给topic类型的exchange，关闭连接，退出   
python receive_logs_topic.py "*.rabbit"   
python emit_log_topic.py red.rabbit Hello   


# 场景6 - PRC   
在应用场景2中描述了如何使用work queue将耗时的task分配到不同的worker中。   
但是，如果我们task是想在远程的计算机上运行一个函数并等待返回结果呢。   
这根场景2中的描述是一个完全不同的故事。   
这一模式被称为远程过程调用。   
现在，我们将构建一个RPC系统，包含一个client和可扩展的RPC server，通过返回斐波那契数来模拟RPC service。   
rpc_server.py   
RPC server：建立连接，声明queue，   
定义了一个返回指定数字的斐波那契数的函数，   
定义了一个回调函数在接收到包含参数的调用请求后调用自己的返回斐波那契数的函数并将结果发送到与接收到message的queue相关联的queue，并进行确认。   
开始接收调用请求并用回调函数进行请求处理   
rpc_client.py   
RPC client：远程过程调用发起者：定义了一个类，类中初始化到RabbitMQ Server的连接、声明回调queue   
开始在回调queue上等待接收响应、   
定义了在回调queue上接收到响应后的处理函数on_response   
根据响应关联的correlation_id属性作出响应、   
定义了调用函数并在其中向调用queue发送包含correlation_id等属性的调用请求、   
初始化一个client实例，以30为参数发起远程过程调用。   
python rpc_server.py   
python rpc_client.py   


rabbitmq_comands.sh   
    定义了rabbitmq的一些命令行参数   


rabbitmq_clusters.sh   
    如何创建cluster   
    cluster的一些基本操作   


rabbit_high_availability.sh   


rabbitmq_web_stomp.sh   
    与web的整合   

