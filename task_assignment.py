import json
import requests
from datetime import datetime
import time

url = "https://samples.openweathermap.org/data/2.5/forecast/hourly"
params = {'q':'London'}
code = {'appid':'b6907d289e10d714a6e88b30761fae22'}
api_response = requests.get(url=url, params= params, data=code)

hour_lists = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 21, 22, 23]

if api_response.status_code==200:
    temperature_test = False
    test_weather_id_500 = False
    test_weather_id_800 = False
#     test_hour = False
    response = api_response.json()
    day = set()
    hour = set()
    result = dict()
    for k, v in response.items():
        if k == 'list':
            for each in v:
                for key,value in each.items():
                    if key == 'dt_txt':
                        datetime_object = datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
                        day.add(datetime_object.day)
                        hour.add(datetime_object.hour)
                        for i in hour_lists:  
                            if i in list(hour):
                                hour_test = True                        
                            else:
                                hour_test = False
                    if key == 'main':
                        temp = value['temp']
                        min_temp = value['temp_min']
                        max_temp = value['temp_max']
                        if temp<min_temp and temp>max_temp:
                            temperature_test = False
                        else:
                            temperature_test = True
                    if key == 'weather':
                        for each in value:
                            if each['id'] == 500:
                                required_condition = 'light rain'
                                condition=each['description'].strip()
                                if condition==required_condition:
                                    test_weather_id_500=True
                            if each['id'] == 800:
                                required_condition = 'clear sky'
                                condition=each['description'].strip()
                                if condition==required_condition:
                                    test_weather_id_800=True
    if len(list(day)) == 4:
        result['1.>Is the response contains 4 days of data'] = True
    else:
        result['1.>Is the response contains 4 days of data'] = False
    result['2. Is all the forecast in the hourly interval ( no hour should be missed )'] = hour_test
    result['3.>For all 4 days, the temp should not be less than temp_min and not more than temp_max'] = temperature_test
    result['4.>If the weather id is 500, the description should be light rain'] = test_weather_id_500
    result['5.>If the weather id is 800, the description should be a clear sky '] =test_weather_id_800
else:
    result['api_response'] = api_response.status_code
    result['message']= "Unexpected"
print(json.dumps(result))
