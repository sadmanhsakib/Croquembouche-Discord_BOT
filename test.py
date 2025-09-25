import datetime

TIME_FORMAT = "%Y-%m-%d -> %H:%M:%S"
now = datetime.datetime.now().strftime(TIME_FORMAT)
print(now)