import time

def getTime(): 
    local_time = time.gmtime(time.time())
    print(f"The time is {local_time[3]-12 if local_time[3] > 12 else local_time[3]}:{local_time[4]}")
getTime()

print("Hello")
time.sleep(1)
print("Go away")