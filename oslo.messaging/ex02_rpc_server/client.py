import oslo_messaging as messaging
from oslo_config import cfg
from oslo_log import log as LOG

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
