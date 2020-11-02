import redis
#链接 redis
r = redis.Redis(host='localhost', port=6379, db=0,charset='utf8',decode_responses=True)

# #设置值
# r.set('mobile', '123')

# #持久化
# r.expire("mobile",1)

import time
# time.sleep(1)
#打印值
print(r.get("18082539819"))