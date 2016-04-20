#!/usr/bin/env bash

# The Web-Stomp plugin is a simple bridge exposing the STOMP protocol over direct or emulated HTML5 WebSockets.
# Stomp –≠“È
sudo rabbitmq-plugins enable rabbitmq_web_stomp
http://127.0.0.1:15674/stomp
http://www.rabbitmq.com/web-stomp.html

# netcat
yum -y install nc
nc -nvv 192.168.56.101 61613
# throw an error
# Ncat: Connection refused
