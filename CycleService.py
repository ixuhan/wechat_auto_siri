# -*- coding: UTF-8 -*-
from WeatherModule import WeatherModule
import json
import requests
import random

class CycleService:
    weather_token_id = ""
    webhook_url = ""
    weatherModule = None
    last_remain_1130_day = 0
    last_remain_1755_day = 0
    last_remain_2100_day = 0
    last_remain_0300_day = 0
    food_list = []

    def CycleServiceInit(self, webhook_url, weather_token_id, food_list_str):
        self.webhook_url = webhook_url
        self.weather_token_id = weather_token_id
        self.weatherModule = WeatherModule()
        self.food_list = food_list_str.split("|")

    def postMsg(self, webhook_url, msg, type = 0, phoneNum = ''):
        print("post msg" + msg)
        if type == 0:
            result = json.dumps(
                {
                    "msgtype": "text",
                    "text": {
                        "content": msg
                    }
                 }, ensure_ascii=False).encode('utf-8')
            requests.post(url=webhook_url, data=result)
        elif type == 1:
            result = json.dumps(
                {
                    "msgtype": "text",
                    "text": {
                        "content": msg,
                        "mentioned_mobile_list": [phoneNum],
                    }
                 }, ensure_ascii=False).encode('utf-8')
            requests.post(url=webhook_url, data=result)
        else:
            result = json.dumps(
                {
                    "msgtype": "text",
                    "text": {
                        "content": msg,
                        "mentioned_list": ["@all"],
                    }
                 }, ensure_ascii=False).encode('utf-8')
            requests.post(url=webhook_url, data=result)

    def CycleServiceCallbck(self, year, month, date, week, hour, min, sec):
        #print("[%d-%d-%d 星期%d %d:%d:%d]" % (year, month, date, week, hour, min, sec))

        if week == 7:
            return

        #03:00提醒写blog
        if hour == 3 and min == 0 and self.last_remain_0300_day != date:
            print("[%d-%d-%d 星期%d %d:%d:%d]:提醒写blog" % (year, month, date, week, hour, min, sec))
            self.last_remain_0300_day = date
            self.postMsg(self.webhook_url, "崔明阳起来写blog!\n", 1, "13556858340")

        #11:30提醒点外卖
        if hour == 11 and min == 30 and self.last_remain_1130_day != date:
            print("[%d-%d-%d 星期%d %d:%d:%d]:提醒点外卖" % (year, month, date, week, hour, min, sec))
            self.last_remain_1130_day = date
            weather_txt = self.weatherModule.getLocalWeather(self.weather_token_id, 0)
            self.postMsg(self.webhook_url, "11:30啦！该点外卖啦！\n" + weather_txt + "\n今日推荐中餐：" + random.choice(self.food_list))


        #17:55提醒吃晚饭
        if hour == 17 and min == 55 and self.last_remain_1755_day != date:
            print("[%d-%d-%d 星期%d %d:%d:%d]:提醒吃晚饭" % (year, month, date, week, hour, min, sec))
            self.last_remain_1755_day = date
            weather_txt = self.weatherModule.getLocalWeather(self.weather_token_id, 0)
            self.postMsg(self.webhook_url, "17:55啦！准备吃晚饭啦！冲冲冲！\n" + weather_txt + "\n今日推荐晚餐：" + random.choice(self.food_list))

        #21:00提醒下班+明日天气
        if hour == 21 and min == 00 and self.last_remain_2100_day != date:
            print("[%d-%d-%d 星期%d %d:%d:%d]:提醒下班" % (year, month, date, week, hour, min, sec))
            self.last_remain_2100_day = date
            weather_txt = self.weatherModule.getLocalWeather(self.weather_token_id, 1)
            self.postMsg(self.webhook_url, "下班啦！\n" + weather_txt)
