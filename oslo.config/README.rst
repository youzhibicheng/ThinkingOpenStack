#-*-coding:utf-8-*-
1. how to debug  
sudo pip install virtualenv  
mkdir .venv  
virtualenv --distribute .venv  
source .venv/bin/active  
pip install oslo.config 
很奇怪,在.venv下执行 from oslo.config import cfg出现错误
# ImportError: No module named oslo.config
pip install oslo.config  
deactive  

