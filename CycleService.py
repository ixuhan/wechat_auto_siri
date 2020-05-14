# -*- coding: UTF-8 -*-
from WeatherModule import WeatherModule
import json
import requests

class CycleService:
    weather_token_id = ""
    webhook_url = ""
    weatherModule = None
    last_remain_1130_day = 0
    last_remain_1755_day = 0
    last_remain_2100_day = 0

    def CycleServiceInit(self, webhook_url, weather_token_id):
        self.webhook_url = webhook_url
        self.weather_token_id = weather_token_id
        self.weatherModule = WeatherModule()

    def postMsg(self, webhook_url, msg):
        print("post msg")
        result = json.dumps(
            {
                "msgtype": "text",
                "text": {
                    "content": msg
                }
             }, ensure_ascii=False).encode('utf-8')
        requests.post(url=webhook_url, data=result)

    def CycleServiceCallbck(self, year, month, date, week, hour, min, sec):
        if week == 7:
            return

        #11:30提醒点外卖
        if hour == 11 and min == 30 and self.last_remain_1130_day != date:
            print("[%d-%d-%d 星期%d %d:%d:%d]" % (year, month, date, week, hour, min, sec))
            self.last_remain_1130_day = date
            self.postMsg(self.webhook_url, "11:30啦！该点外卖啦！")

        #17:55提醒吃晚饭
        if hour == 17 and min == 55 and self.last_remain_1755_day != date:
            print("[%d-%d-%d 星期%d %d:%d:%d]" % (year, month, date, week, hour, min, sec))
            self.last_remain_1755_day = date
            self.postMsg(self.webhook_url, "17:55啦！准备吃晚饭啦！冲冲冲！")

        #21:00提醒下班+明日天气
        if hour == 21 and min == 00 and self.last_remain_2100_day != date:
            print("[%d-%d-%d 星期%d %d:%d:%d]" % (year, month, date, week, hour, min, sec))
            self.last_remain_2100_day = date
            weather_txt = self.weatherModule.getLocalWeather(self.weather_token_id)
            self.postMsg(self.webhook_url, "下班啦！\n" + weather_txt)
