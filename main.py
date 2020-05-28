# -*- coding: UTF-8 -*-
import threading
import time
import json
from CycleService import CycleService

#参数初始化
def wechat_siri_param_init():
    #读取wechat推送地址
    with open('wechar_siri.cfg', 'r', encoding='UTF-8') as f:
        cfg_val = json.loads(f.read())
        return cfg_val['webhook_url'], float(cfg_val['sleep_cycle']), cfg_val['weather_token_id'], cfg_val['food_list']
    print("wechat_siri_param_init")

def cycle_run(callback, sleep_cycle):
    last_timestamp = 0
    while True:
        #获取时间原始数据
        time_data = time.time()
        #转换为时间戳
        timestamp = int(time_data)
        if last_timestamp != timestamp:
            last_timestamp = timestamp
            #转换为时间结构体
            time_struct = time.localtime(time_data)
            callback(time_struct.tm_year, time_struct.tm_mon, time_struct.tm_mday, time_struct.tm_wday + 1, time_struct.tm_hour, time_struct.tm_min, time_struct.tm_sec);
            time.sleep(sleep_cycle)

class runThread (threading.Thread):
    def __init__(self, threadID, name, callback, sleep_cycle):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.callback = callback
        self.sleep_cycle = sleep_cycle
    def run(self):
        cycle_run(self.callback, self.sleep_cycle)

def main():
    webhook_url = ""
    sleep_cycle = 0
    weather_token_id = ""
    food_list_str = ""

    webhook_url, sleep_cycle, weather_token_id, food_list_str = wechat_siri_param_init()
    print("webhook_url=" + webhook_url)
    print("sleep_cycle=" + str(sleep_cycle))
    print("weather_token_id=" + weather_token_id)
    cycleServce = CycleService()
    cycleServce.CycleServiceInit(webhook_url, weather_token_id, food_list_str)
    thread = runThread(1, "cycle_run", cycleServce.CycleServiceCallbck, sleep_cycle)
    thread.start()
    thread.join()

main();