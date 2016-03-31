$ git clone git@github.com:openstack/oslo.policy.git
http://docs.openstack.org/developer/oslo.policy/
The Oslo Policy library provides support for RBAC policy enforcement across all OpenStack services

sample
ceilometer-policy.json
nova-policy.json
    refer to source code in nova project
    nova/nova/compute/api.py
        def resize(...)
    pay attention to decorator
        @wrap_check_policy
http://blog.chinaunix.net/uid-20940095-id-4144300.html
http://blog.csdn.net/zfqiannian/article/details/49306691


负责policy的验证和rules的管理

格式
"<target>": <rule>

rule有2种格式
1. a string written in the new policy language
    preferred
    Conjunction operators 'and', 'or', 'not' are available
    
2. a list of lists.


程序如何读取 policy.json
policy.json 字段意义

@wrap_check_policy