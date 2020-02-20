from get_weather import get_weather
from get_weather import get_datetime
from time import sleep

sleep_count = 0
while sleep_count <= 11:
    print("Adding data... Time : %s"%get_datetime())
    get_weather()
    sleep(300)
    sleep_count += 1