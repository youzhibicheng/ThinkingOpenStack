#!/usr/bin/env bash

# for normal installation, please refer to installation_centos7.sh

# management plugin
# The rabbitmq-management plugin provides an HTTP-based API for management and monitoring of your RabbitMQ server,
# along with a browser-based UI and a command line tool, rabbitmqadmin
# the management plugin is included in the RabbitMQ distribution. To enable it, use rabbitmq-plugins
rabbitmq-plugins enable rabbitmq_management
#The following plugins have been enabled:
#  mochiweb
#  webmachine
#  rabbitmq_web_dispatch
#  amqp_client
# rabbitmq_management_agent
#  rabbitmq_management
#Plugin configuration has changed. Restart RabbitMQ for changes to take effect.
sudo service rabbitmq-server restart

# The web UI is located at: http://server-name:15672/
# The HTTP API and its documentation are both located at: http://server-name:15672/api/
# Download rabbitmqadmin at: http://server-name:15672/cli/ (download it and save it as rabbitmqadmin in this dir)
# username / password = guest / guest
chmod a+x rabbitmqadmin
sudo cp rabbitmqadmin /usr/local/bin
# the document for rabbitmqadmin
# http://www.rabbitmq.com/management-cli.html

# bash completion
sudo sh -c 'rabbitmqadmin --bash-completion > /etc/bash_completion.d/rabbitmqadmin'

# sample
rabbitmqadmin list exchanges
rabbitmqadmin list queues vhost name node messages message_stats.publish_details.rate