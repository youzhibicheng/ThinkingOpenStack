import rpc
# encoding:utf8
TOPIC = 'sendout_request'

msg = {'method': 'add',
       'args':{'v1':2, 'v2':3}}
rval = rpc.call(TOPIC, msg)
print('Succeed implementing OpenStack RPC call. the return value is %d.\n' % rval)


