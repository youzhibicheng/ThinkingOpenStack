# TaskFlow #
http://docs.openstack.org/developer/taskflow/

TaskFlow is a Python library that helps to make task execution easy, consistent and reliable

## Concept ##
### task ###
    execute()
    revert()
### flow ###
    including tasks
    flow.add(task1, task2, ...)                       
    flow可以嵌套
linear_flow
unordered_flow
gragh_flow
### engine ###
    engines.run(flow, ...)
