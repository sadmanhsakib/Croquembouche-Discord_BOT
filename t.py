import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d -> %H:%M:%S")

now_parts = now.split(' ')

print(now_parts[0])
