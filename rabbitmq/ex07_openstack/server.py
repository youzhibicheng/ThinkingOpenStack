# encoding:utf8

import service

srv = service.Service()
srv.start()

# drain_events有什么用途?
while True:
    srv.drain_events()
