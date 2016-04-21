from oslo_config import cfg
import oslo_messaging

class NotificationEndpoint(object):
    #filter_rule = NotificationFilter(publisher_id='^compute.*')

    def warn(self, ctxt, publisher_id, event_type, payload, metadata):
        #do_something(payload)
        pass

class ErrorEndpoint(object):
    #filter_rule = NotificationFilter(event_type='^instance\..*\.start$', context={'ctxt_key': 'regexp'})

    def error(self, ctxt, publisher_id, event_type, payload, metadata):
        #do_something(payload)
        pass

transport = oslo_messaging.get_notification_transport(cfg.CONF)
targets = [
    oslo_messaging.Target(topic='notifications')
    oslo_messaging.Target(topic='notifications_bis')
]
endpoints = [
    NotificationEndpoint(),
    ErrorEndpoint(),
]
# what does poll mean???
pool = "listener-workers"
server = oslo_messaging.get_notification_listener(transport, targets,
                                                  endpoints, pool)
server.start()
server.wait()
