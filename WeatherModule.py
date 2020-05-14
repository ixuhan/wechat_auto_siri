# -*- coding: UTF-8 -*-
import json
from HttpGetTools import HttpGetTools

class WeatherModule:
    code_dict = {'CLEAR_DAY':   '晴     ', 'CLEAR_NIGHT':   '晴     ', 'PARTLY_CLOUDY_DAY': '多云   ', 'PARTLY_CLOUDY_NIGHT': '多云   ',
                 'CLOUDY':      '阴     ', 'LIGHT_HAZE':    '轻度雾霾', 'MODERATE_HAZE': '中度雾霾', 'HEAVY_HAZE': '重度雾霾',
                 'LIGHT_RAIN':  '小雨   ', 'MODERATE_RAIN':  '中雨   ', 'HEAVY_RAIN': '大雨   ', 'STORM_RAIN': '暴雨   ',
                 'FOG':         '雾     ', 'LIGHT_SNOW':    '小雪   ', 'MODERATE_SNOW': '中雪   ', 'HEAVY_SNOW': '大雪   ',
                 'STORM_SNOW':  '暴雪   ', 'DUST':          '浮尘   ', 'SAND': '沙尘   ', 'WIND': '大风   '}

    def getLocalWeather(self,token_id):
        htmlTest = HttpGetTools.getHttpBodyHtml("https://api.caiyunapp.com/v2.5/" + token_id + "/113.923552,22.528499/hourly.json")
        dict = json.loads(htmlTest)
        if dict['status'] == "ok" and dict['result']['hourly']['status'] == "ok":
            result = "[深圳市南山区]当前天气预报：\n"
            result += dict['result']['hourly']['description']
            result += "\n[深圳市南山区]未来24小时天气：\n"
            skycon = dict['result']['hourly']['skycon']
            count = 0
            hour_count = 0
            for item in skycon:
                count = count + 1
                hour_count = hour_count + 1
                result += item['datetime'].split("T")[1].split("+")[0] + self.code_dict[item['value']]
                if count == 6 and hour_count != 24:
                    result += "\n"
                    count = 0
                if hour_count == 24:
                    break
            return result
        else:
            return ""