import time
t = time.time() + 86400*2
print(time.strftime('%m月%d天%H时%M分%S秒', time.localtime(t)))