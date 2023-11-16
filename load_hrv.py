import api.api as api

import gather_keys_oauth2 as Oauth2
import pandas as pd
import datetime
import configparser


config = configparser.ConfigParser()
config.read("load_hrv.ini")

fitbit_client = api.Fitbit(config['DEFAULT']['CLIENT_ID'], config['DEFAULT']['CLIENT_SECRET'], access_token=config['DEFAULT']['ACCESS_TOKEN'], refresh_token=config['DEFAULT']['REFRESH_TOKEN'])


start_date = datetime.date(2023, 2, 16)
days = 16
delta = datetime.timedelta(days=days)
end_date = start_date + delta

index = pd.date_range(start_date, periods=days)

df = pd.DataFrame(index=index, columns=["breathingRate", "hrv", "restingHeartRate"])

print(start_date.strftime("%Y-%m-%d"))
print(end_date.strftime("%Y-%m-%d"))

#restingHR = ''
#try:
#    activity_data = fitbit_client.intraday_time_series('activities/heart', base_date=start_date)
#    restingHR =  activity_data['activities-heart'][0]['value']['restingHeartRate']
#except Exception as e:
#    print(e)

try:
    data = fitbit_client.time_series('activities/heart', base_date=start_date, end_date=end_date)

    for i in range(len(data['activities-heart'])):
        dt = data['activities-heart'][i]['dateTime']
        try:
            df.at[dt,'restingHeartRate'] = data['activities-heart'][i]['value']['restingHeartRate']
        except Exception as e:
            print(e)

except Exception as e:
    print(e)

#hrv = ''
#try:
#    hrv_data = fitbit_client.get_hrv(start_date)
#    hrv = hrv_data['hrv'][0]['value']['dailyRmssd']
#except Exception as e:
#    print(e)

try:
    data = fitbit_client.time_series('hrv', base_date=start_date, end_date=end_date)

    for i in range(len(data['hrv'])):
        dt = data['hrv'][i]['dateTime']
        df.at[dt,'hrv'] = data['hrv'][i]['value']['dailyRmssd']
except Exception as e:
    print(e)

#br = ''
#try:
#    br_data = fitbit_client.get_br(start_date)
#    br = br_data['br'][0]['value']['breathingRate']
#except Exception as e:
#    print(e)

#sleep_data = fitbit_client.get_sleep(start_date)
#print(sleep_data)
#print(sleep_data['sleep'][0]['value']['breathingRate'])

try:
    br_data = fitbit_client.time_series('br', base_date=start_date, end_date=end_date)

    for i in range(len(br_data['br'])):
        dt = br_data['br'][i]['dateTime']
        try:
            df.at[dt,'breathingRate'] = br_data['br'][i]['value']['breathingRate']
        except Exception as e:
            print(e)
except Exception as e:
    print(e)


print(df)
df.to_csv(start_date.strftime("%Y-%m-%d")+'_fitbit.csv', sep=';') 



