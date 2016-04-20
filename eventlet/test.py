from eventlet import hubs  
from eventlet import greenthread  
  
def tellme(secret):  
    print "a secret:",secret  
      
  
hub = hubs.get_hub()  
hub.schedule_call_global(0,tellme,"you are so beautiful")  
hub.switch()  
