import time
from time import gmtime, strftime
from datetime import datetime
while True:
	print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3], " Hello World")
	time.sleep(1)
