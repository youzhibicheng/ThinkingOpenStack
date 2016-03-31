import taskflow.engines
from taskflow.patterns import graph_flow as gf
from taskflow.patterns import linear_flow as lf
from taskflow.task import Task


class Adder(Task):
    def execute(self,x, y):
        return x + y

flow = gf.Flow('root').add(
    lf.Flow('nested_linear').add(
        Adder("add2", provides='x2', rebind=['y3', 'y4']),
        Adder("add1", provides='x1', rebind=['y1', 'y2'])
    ),
    Adder("add5", provides='x5', rebind=['x1', 'x3']),
    Adder("add3", provides='x3', rebind=['x1', 'x2']),
    Adder("add4", provides='x4', rebind=['x2', 'y5']),
    Adder("add6", provides='x6', rebind=['x5', 'x4']),
    Adder("add7", provides='x7', rebind=['x6', 'x6'])
)

store = {
    "y1": 1,
    "y2": 3,
    "y3": 5,
    "y4": 7,
    "y5": 9,
}

result = taskflow.engines.run(flow, engine_conf='serial', store=store)
print("Single thread engine result %s" % result)

result = taskflow.engines.run(flow, engine_conf='parallel', store=store)
print("Multi thread engine result %s" % result)
