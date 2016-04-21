import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as LOG

# do not use in this example
class TestClient(object):

    def __init__(self, transport):
        target = messaging.Target(topic='test', version='2.0')
        self._client = messaging.RPCClient(transport, target)

    def test(self, ctxt, arg):
        return self._client.call(ctxt, 'test', arg=arg)

    def test2(self, ctxt, arg):
        cctxt = self._client.prepare(version='2.5')
        return cctxt.call(ctxt, 'test', arg=arg)

    def test3(self, ctxt, arg):
        cctxt = self._client.prepare(timeout=10)
        return cctxt.call(ctxt, 'test', arg=arg)

    def test4(self, ctxt, arg):
        transport = messaging.get_transport(cfg.CONF)
        target = messaging.Target(topic='test', version='2.0')
        client = messaging.RPCClient(transport, target)
        client.call(ctxt, 'test', arg=arg)

    def test5(self, ctxt, arg):
        transport = messaging.get_transport(cfg.CONF)
        target = messaging.Target(topic='test', version='2.0')
        client = messaging.RPCClient(transport, target, retry=None)
        client.call(ctxt, 'sync')
        try:
            client.prepare(retry=0).cast(ctxt, 'ping')
        except messaging.MessageDeliveryFailure:
            LOG.error("Failed to send ping message")


transport = messaging.get_transport(cfg.CONF)
# 在构造RPC-client的target时，需要topic参数，其他可选。
target = messaging.Target(topic='test')
client = messaging.RPCClient(transport, target)

# 远程调用时，需要提供一个字典对象来指明调用的上下文，调用方法的名字和传递给调用方法的参数(用字典表示)。
ret = client.call(ctxt = {},
                  method = 'test',
                  arg = 'myarg')

# prepare函数用于修改RPC-client对象的Target对象的属性。
cctxt = client.prepare(namespace='control', version='2.0')
cctxt.cast({}, 'stop')